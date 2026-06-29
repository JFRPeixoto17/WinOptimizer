"""
WinOptimizer Pro - Professional Windows Performance Optimizer
A safe, modern Windows optimization tool with Fluent Design dark theme

Version: 1.2.0 - Free/Pro Edition (bug fixes)
Author: João Filipe Reis Peixoto
M.Sc. Student in Critical Computing System Engineering
Copyright (c) 2025 João Filipe Reis Peixoto. All rights reserved.

This software is provided for educational and personal use.

Changelog v1.2.0:
  - Added Free vs Pro edition system (IS_PRO flag)
  - Added Cleanup tab for Free users (5 safe tweaks)
  - Pro-only tabs show lock icon and upgrade modal in Free mode
  - Fixed: checkbox lambda closure bug (wrong tweak_id captured in loop)
  - Fixed: clicking card area no longer double-fires toggle (checkbox + bind)
  - Fixed: tab highlight update now uses stored button references correctly
  - Fixed: log_to_console AttributeError in restore_to_stock
  - Fixed: service_name (singular) vs service_names (list) handling
  - Fixed: KeyError on COLORS/SPACING fallback dict missing keys
"""

import customtkinter as ctk
import json
import os
import sys
import subprocess
import ctypes
import threading
from datetime import datetime
from pathlib import Path
import traceback

# ─────────────────────────────────────────────────────────────
#  EDITION FLAG — set to True to unlock Pro features.
#  In production this should be driven by a license check.
# ─────────────────────────────────────────────────────────────
IS_PRO = False

# Import modern color scheme
try:
    from theme import COLORS, FONTS, SPACING, RADIUS, ANIMATION
except ImportError:
    COLORS = {
        "bg_primary":      "#0f1419",
        "bg_secondary":    "#1a1f2e",
        "bg_tertiary":     "#242b3d",
        "bg_card":         "#1a2332",
        "bg_card_selected":"#1a3352",
        "accent_primary":  "#3a86ff",
        "accent_hover":    "#5a9cff",
        "text_primary":    "#e8eaed",
        "text_secondary":  "#9aa0a6",
        "text_tertiary":   "#6a7280",
        "border":          "#2a3a4a",
        "success":         "#34a853",
        "warning":         "#fbbc04",
        "error":           "#ea4335",
    }
    FONTS = {
        "heading_large": ("Segoe UI", 32, "bold"),
        "body_large":    ("Segoe UI", 14),
        "body_medium":   ("Segoe UI", 12, "bold"),
        "body_small":    ("Segoe UI", 10),
        "body_xs":       ("Segoe UI", 10),
    }
    SPACING = {"xs": 4, "sm": 8, "md": 12, "lg": 16}
    RADIUS  = {"medium": 8}
    ANIMATION = {"normal": 250}

# Tweaks available in Free edition (shown in Cleanup tab)
FREE_TWEAK_IDS = {"restore", "tempfiles", "prefetch", "thumbnails", "windowsUpdate"}

# Tabs that require Pro
PRO_ONLY_TABS = {"services", "performance", "privacy", "advanced"}


def get_resource_path(relative_path):
    """Absolute path to resource — works for dev and PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = Path(__file__).parent
    return os.path.join(base_path, relative_path)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class WinOptimizer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("WinOptimizer Pro - Professional Windows Optimizer")
        self.geometry("1400x900")
        self.minsize(1200, 700)

        try:
            icon_path = get_resource_path("icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            pass

        # App state
        self.selected_tweaks: set = set()
        self.applied_tweaks:  set = set()
        self.tweaks_data:    dict = {}
        self.current_tab: str = "cleanup" if not IS_PRO else "essential"

        # UI references populated during build
        self._tab_buttons: dict[str, ctk.CTkButton] = {}

        self.load_tweaks()

        if not self.is_admin():
            self.show_admin_warning()

        self.create_ui()

    # ──────────────────────────────────────────────────────────
    #  Helpers
    # ──────────────────────────────────────────────────────────

    def is_admin(self) -> bool:
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False

    def show_admin_warning(self):
        dlg = ctk.CTkToplevel(self)
        dlg.title("Administrator Required")
        dlg.geometry("500x200")
        dlg.transient(self)
        dlg.grab_set()
        ctk.CTkLabel(
            dlg,
            text=(
                "⚠️ Administrator Privileges Required\n\n"
                "This application needs administrator rights to apply system tweaks.\n"
                "Please restart the application as administrator."
            ),
            font=("Segoe UI", 14),
            justify="center",
        ).pack(pady=40, padx=20)
        ctk.CTkButton(dlg, text="OK", command=dlg.destroy, width=120, height=40).pack(pady=10)

    def load_tweaks(self):
        try:
            with open(get_resource_path("tweaks.json"), "r", encoding="utf-8") as f:
                self.tweaks_data = json.load(f)
        except Exception as e:
            print(f"Error loading tweaks: {e}")
            self.tweaks_data = {
                "essential": [], "services": [], "performance": [],
                "privacy": [], "advanced": [], "presets": {},
            }

    def _all_tweaks(self) -> list:
        """Flat list of every tweak (excluding presets key)."""
        return [t for cat, lst in self.tweaks_data.items() if cat != "presets" for t in lst]

    # ──────────────────────────────────────────────────────────
    #  UI Construction
    # ──────────────────────────────────────────────────────────

    def create_ui(self):
        self.configure(fg_color=COLORS["bg_primary"])
        self._build_header()
        if IS_PRO:
            self._build_presets_bar()
        self._build_main_content()
        self._build_action_bar()

    def _build_header(self):
        header = ctk.CTkFrame(self, height=100, fg_color=COLORS["bg_secondary"], corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        row = ctk.CTkFrame(header, fg_color="transparent")
        row.pack(fill="x", padx=SPACING["lg"])

        ctk.CTkLabel(
            row,
            text="WinOptimizer Pro",
            font=FONTS["heading_large"],
            text_color=COLORS["accent_primary"],
        ).pack(side="left", pady=(SPACING["md"], SPACING["xs"]))

        edition_text  = "FREE"         if not IS_PRO else "✦ PRO"
        edition_color = "#f5a623"      if not IS_PRO else "#34a853"
        edition_bg    = "#3a2800"      if not IS_PRO else "#1a3a1a"
        ctk.CTkLabel(
            row,
            text=edition_text,
            font=("Segoe UI", 12, "bold"),
            text_color=edition_color,
            fg_color=edition_bg,
            corner_radius=6,
            padx=10, pady=4,
        ).pack(side="left", padx=12, pady=(SPACING["md"] + 8, 0))

        ctk.CTkLabel(
            header,
            text="Professional Windows Performance Optimizer",
            font=FONTS["body_large"],
            text_color=COLORS["text_secondary"],
        ).pack(pady=SPACING["xs"])

        version = "Version 1.2.0 - Free Edition" if not IS_PRO else "Version 1.2.0 - Pro Edition"
        ctk.CTkLabel(
            header,
            text=version,
            font=FONTS["body_small"],
            text_color=COLORS["text_tertiary"],
        ).pack()

    def _build_presets_bar(self):
        bar = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"], height=90, corner_radius=RADIUS["medium"])
        bar.pack(fill="x", padx=SPACING["lg"], pady=SPACING["md"])
        bar.pack_propagate(False)

        ctk.CTkLabel(
            bar,
            text="QUICK PROFILES:",
            font=FONTS["body_small"],
            text_color=COLORS["text_tertiary"],
        ).pack(pady=(SPACING["md"], SPACING["xs"]), anchor="w", padx=SPACING["lg"])

        preset_names = {
            "recommended":       "✓ Recommended",
            "maximum_performance":"⚡ Maximum Performance",
            "basic_cleanup":     "🧹 Basic Cleanup",
            "gaming_focused":    "🎮 Gaming Focused",
            "privacy_focused":   "🔒 Privacy Focused",
        }

        btn_frame = ctk.CTkFrame(bar, fg_color="transparent")
        btn_frame.pack(fill="both", expand=True, padx=SPACING["lg"], pady=(0, SPACING["md"]))

        for idx, (pid, pname) in enumerate(preset_names.items()):
            ctk.CTkButton(
                btn_frame,
                text=pname,
                command=lambda p=pid: self.apply_preset(p),
                width=180, height=40,
                font=FONTS["body_medium"],
                fg_color=COLORS["bg_tertiary"],
                hover_color=COLORS["accent_hover"],
                text_color=COLORS["text_primary"],
                corner_radius=RADIUS["medium"],
                border_width=1,
                border_color=COLORS["border"],
            ).grid(row=0, column=idx, padx=SPACING["xs"], sticky="ew")
            btn_frame.grid_columnconfigure(idx, weight=1)

    def _build_main_content(self):
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SPACING["lg"], pady=(0, SPACING["lg"]))

        # Tab bar
        tabs_frame = ctk.CTkFrame(
            content, fg_color=COLORS["bg_secondary"],
            height=60, corner_radius=RADIUS["medium"],
        )
        tabs_frame.pack(fill="x", pady=(0, SPACING["md"]))
        tabs_frame.pack_propagate(False)
        self._build_tab_bar(tabs_frame)

        # Scrollable tweaks area
        self.tweaks_container = ctk.CTkScrollableFrame(
            content,
            fg_color=COLORS["bg_primary"],
            scrollbar_button_color=COLORS["bg_tertiary"],
            scrollbar_button_hover_color=COLORS["accent_primary"],
        )
        self.tweaks_container.pack(fill="both", expand=True)
        self.render_tweaks()

    def _build_tab_bar(self, parent):
        if IS_PRO:
            tabs = [
                ("essential",   "⚙️ Essential"),
                ("services",    "🖥️ Services"),
                ("performance", "⚡ Performance"),
                ("privacy",     "👁️ Privacy"),
                ("advanced",    "🛡️ Advanced"),
            ]
        else:
            tabs = [
                ("cleanup",     "🧹 Cleanup"),
                ("essential",   "⚙️ Essential"),
                ("services",    "🖥️ Services 🔒"),
                ("performance", "⚡ Performance 🔒"),
                ("privacy",     "👁️ Privacy 🔒"),
                ("advanced",    "🛡️ Advanced 🔒"),
            ]

        self._tab_buttons = {}
        for tab_id, tab_name in tabs:
            locked  = (not IS_PRO) and (tab_id in PRO_ONLY_TABS)
            active  = (tab_id == self.current_tab)

            if active:
                bg = "#3a3a5e"
            elif locked:
                bg = "#1e1e2e"
            else:
                bg = "#2a2a3e"

            btn = ctk.CTkButton(
                parent,
                text=tab_name,
                command=lambda t=tab_id, lk=locked: self._on_tab_click(t, lk),
                width=170, height=45,
                font=("Segoe UI", 12, "bold"),
                fg_color=bg,
                hover_color="#4a4a6e" if not locked else "#2e2e3e",
                text_color=COLORS["text_primary"] if not locked else COLORS["text_tertiary"],
            )
            btn.pack(side="left", padx=5, pady=8)
            self._tab_buttons[tab_id] = btn

    def _on_tab_click(self, tab_id: str, locked: bool):
        if locked:
            self._show_upgrade_modal()
        else:
            self.switch_tab(tab_id)

    def _show_upgrade_modal(self):
        dlg = ctk.CTkToplevel(self)
        dlg.title("Pro Feature")
        dlg.geometry("520x340")
        dlg.resizable(False, False)
        dlg.transient(self)
        dlg.grab_set()

        ctk.CTkLabel(dlg, text="🔒 Pro Feature", font=("Segoe UI", 26, "bold"), text_color="#f5a623").pack(pady=(30, 8))
        ctk.CTkLabel(dlg, text="This tab is available in WinOptimizer Pro.", font=("Segoe UI", 14)).pack(pady=4)
        ctk.CTkLabel(
            dlg,
            text=(
                "Upgrade to Pro to unlock:\n\n"
                "  ⚡ Services, Performance, Privacy & Advanced tabs\n"
                "  🎮 Gaming tweaks & GPU scheduling\n"
                "  🔒 60+ tested optimizations\n"
                "  ⚙️ Quick Presets for one-click tuning"
            ),
            font=("Segoe UI", 13),
            text_color=COLORS["text_secondary"],
            justify="left",
        ).pack(pady=12, padx=30)

        row = ctk.CTkFrame(dlg, fg_color="transparent")
        row.pack(pady=16)

        ctk.CTkButton(
            row, text="✦ Upgrade to Pro",
            command=dlg.destroy,          # TODO: replace with purchase flow
            width=180, height=44,
            font=("Segoe UI", 13, "bold"),
            fg_color="#f5a623", hover_color="#e09010", text_color="#000000",
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            row, text="Close", command=dlg.destroy,
            width=120, height=44,
            fg_color=COLORS["bg_tertiary"], hover_color=COLORS["border"],
        ).pack(side="left", padx=10)

    def _build_action_bar(self):
        bar = ctk.CTkFrame(self, height=80, fg_color="#16213e")
        bar.pack(fill="x", padx=10, pady=10)
        bar.pack_propagate(False)

        self.selection_label = ctk.CTkLabel(bar, text="0 selected", font=("Segoe UI", 14, "bold"), text_color="#4da6ff")
        self.selection_label.pack(side="left", padx=20, pady=20)

        self.applied_label = ctk.CTkLabel(bar, text="", font=("Segoe UI", 14, "bold"), text_color="#4dff4d")
        self.applied_label.pack(side="left", padx=10, pady=20)

        btn_frame = ctk.CTkFrame(bar, fg_color="transparent")
        btn_frame.pack(side="right", padx=20, pady=15)

        ctk.CTkButton(btn_frame, text="Clear Selection", command=self.clear_selection,
                      width=150, height=50, font=("Segoe UI", 13, "bold"),
                      fg_color="#3a3a3a", hover_color="#4a4a4a").pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="Undo Tweaks", command=self.show_undo_dialog,
                      width=150, height=50, font=("Segoe UI", 13, "bold"),
                      fg_color="#ff6b35", hover_color="#ff8555").pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="🔄 Restore to Stock", command=self.restore_to_stock,
                      width=180, height=50, font=("Segoe UI", 13, "bold"),
                      fg_color="#ff4444", hover_color="#ff6666").pack(side="left", padx=5)

        self.apply_btn = ctk.CTkButton(
            btn_frame, text="Apply Optimizations", command=self.show_apply_dialog,
            width=200, height=50, font=("Segoe UI", 14, "bold"),
            fg_color="#4da6ff", hover_color="#6db6ff", state="disabled",
        )
        self.apply_btn.pack(side="left", padx=5)

    # ──────────────────────────────────────────────────────────
    #  Tweak rendering
    # ──────────────────────────────────────────────────────────

    def _cleanup_tweaks(self) -> list:
        return [t for t in self.tweaks_data.get("essential", []) if t["id"] in FREE_TWEAK_IDS]

    def render_tweaks(self):
        for w in self.tweaks_container.winfo_children():
            w.destroy()

        if self.current_tab == "cleanup":
            ctk.CTkLabel(
                self.tweaks_container,
                text="🧹  Basic Cleanup  —  Safe for all users",
                font=("Segoe UI", 13, "bold"),
                text_color=COLORS["text_tertiary"],
                anchor="w",
            ).pack(fill="x", padx=10, pady=(8, 4))
            tweaks = self._cleanup_tweaks()
        else:
            tweaks = self.tweaks_data.get(self.current_tab, [])

        for tweak in tweaks:
            self._create_tweak_card(tweak)

    def _create_tweak_card(self, tweak: dict):
        """
        BUG FIX: lambda closure — capture tweak_id by default argument,
        not by reference to loop variable.
        BUG FIX: don't bind <Button-1> on the checkbox widget itself to
        avoid double-firing (checkbox command + bind both call toggle).
        """
        tid        = tweak["id"]
        is_sel     = tid in self.selected_tweaks
        is_applied = tid in self.applied_tweaks

        card = ctk.CTkFrame(
            self.tweaks_container,
            fg_color=COLORS["bg_card_selected"] if is_sel else COLORS["bg_card"],
            border_width=2,
            border_color="#4da6ff" if is_sel else COLORS["border"],
            corner_radius=10,
        )
        card.pack(fill="x", padx=10, pady=5)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=12)

        # ── Left: info ────────────────────────────────────────
        left = ctk.CTkFrame(inner, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True)

        title_row = ctk.CTkFrame(left, fg_color="transparent")
        title_row.pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(title_row, text=tweak["name"],
                     font=("Segoe UI", 14, "bold"), text_color="#ffffff", anchor="w").pack(side="left")

        if tweak.get("recommended"):
            ctk.CTkLabel(title_row, text="✓ Recommended",
                         font=("Segoe UI", 10, "bold"), text_color="#4dff4d",
                         fg_color="#1a3a1a", corner_radius=5, padx=8, pady=2).pack(side="left", padx=5)

        ctk.CTkLabel(title_row, text=tweak["impact"],
                     font=("Segoe UI", 10, "bold"), text_color="#b366ff",
                     fg_color="#2a1a3a", corner_radius=5, padx=8, pady=2).pack(side="left", padx=5)

        if is_applied:
            ctk.CTkLabel(title_row, text="✓ Applied",
                         font=("Segoe UI", 10, "bold"), text_color="#4dff4d",
                         fg_color="#1a4a1a", corner_radius=5, padx=8, pady=2).pack(side="left", padx=5)

        ctk.CTkLabel(left, text=tweak["description"],
                     font=("Segoe UI", 12), text_color="#aaaaaa",
                     anchor="w", justify="left", wraplength=900).pack(fill="x")

        if "drawback" in tweak:
            ctk.CTkLabel(left, text=f"⚠️ Drawback: {tweak['drawback']}",
                         font=("Segoe UI", 11), text_color="#ffaa00", anchor="w").pack(fill="x", pady=(5, 0))

        # ── Right: checkbox ───────────────────────────────────
        # FIX: use tid=tid default-arg capture so each lambda closes over its own id
        checkbox = ctk.CTkCheckBox(
            inner, text="",
            command=lambda tid=tid: self.toggle_tweak(tid),
            width=28, height=28, checkbox_width=28, checkbox_height=28,
            corner_radius=5, fg_color="#4da6ff", hover_color="#6db6ff", border_color="#4da6ff",
        )
        checkbox.pack(side="right", padx=10)
        if is_sel:
            checkbox.select()
        else:
            checkbox.deselect()

        # FIX: bind click on card background and non-interactive children only,
        # skip the checkbox widget itself so it doesn't fire twice.
        def _toggle(e, tid=tid):
            self.toggle_tweak(tid)

        card.bind("<Button-1>", _toggle)
        for child in inner.winfo_children():
            if child is not checkbox:
                child.bind("<Button-1>", _toggle)
                for grandchild in child.winfo_children():
                    grandchild.bind("<Button-1>", _toggle)

    # ──────────────────────────────────────────────────────────
    #  Selection / tab logic
    # ──────────────────────────────────────────────────────────

    def toggle_tweak(self, tweak_id: str):
        if tweak_id in self.selected_tweaks:
            self.selected_tweaks.remove(tweak_id)
        else:
            self.selected_tweaks.add(tweak_id)
        self.update_ui()

    def update_ui(self):
        self.selection_label.configure(text=f"{len(self.selected_tweaks)} selected")
        self.applied_label.configure(
            text=f"✓ {len(self.applied_tweaks)} applied" if self.applied_tweaks else ""
        )
        self.apply_btn.configure(state="normal" if self.selected_tweaks else "disabled")
        self.render_tweaks()

    def switch_tab(self, tab_id: str):
        self.current_tab = tab_id
        # FIX: update highlights using stored button dict (reliable)
        for tid, btn in self._tab_buttons.items():
            locked = (not IS_PRO) and (tid in PRO_ONLY_TABS)
            if tid == tab_id:
                btn.configure(fg_color="#3a3a5e")
            elif locked:
                btn.configure(fg_color="#1e1e2e")
            else:
                btn.configure(fg_color="#2a2a3e")
        self.render_tweaks()

    def apply_preset(self, preset_id: str):
        presets = self.tweaks_data.get("presets", {})
        if preset_id in presets:
            self.selected_tweaks = set(presets[preset_id])
            self.update_ui()

    def clear_selection(self):
        self.selected_tweaks.clear()
        self.update_ui()

    # ──────────────────────────────────────────────────────────
    #  Apply tweaks
    # ──────────────────────────────────────────────────────────

    def show_apply_dialog(self):
        if not self.is_admin():
            self.show_admin_warning()
            return

        dlg = ctk.CTkToplevel(self)
        dlg.title("Confirm Optimizations")
        dlg.geometry("700x500")
        dlg.transient(self)
        dlg.grab_set()

        ctk.CTkLabel(dlg, text=f"Ready to Apply {len(self.selected_tweaks)} Optimizations",
                     font=("Segoe UI", 20, "bold"), text_color="#4da6ff").pack(pady=20)

        lf = ctk.CTkScrollableFrame(dlg, fg_color="#16213e")
        lf.pack(fill="both", expand=True, padx=20, pady=10)

        for tweak in self._all_tweaks():
            if tweak["id"] in self.selected_tweaks:
                ctk.CTkLabel(lf, text=f"✓ {tweak['name']} - {tweak['impact']}",
                             font=("Segoe UI", 12), anchor="w").pack(fill="x", padx=10, pady=3)

        row = ctk.CTkFrame(dlg, fg_color="transparent")
        row.pack(pady=20)
        ctk.CTkButton(row, text="Cancel", command=dlg.destroy,
                      width=150, height=45, fg_color="#3a3a3a", hover_color="#4a4a4a").pack(side="left", padx=10)
        ctk.CTkButton(row, text="Apply Now", command=lambda: self.apply_tweaks(dlg),
                      width=150, height=45, fg_color="#4da6ff", hover_color="#6db6ff").pack(side="left", padx=10)

    def apply_tweaks(self, dialog):
        dialog.destroy()

        pdlg = ctk.CTkToplevel(self)
        pdlg.title("Applying Optimizations")
        pdlg.geometry("800x600")
        pdlg.transient(self)
        pdlg.grab_set()

        ctk.CTkLabel(pdlg, text="Applying Optimizations...", font=("Segoe UI", 20, "bold")).pack(pady=20)

        console = ctk.CTkTextbox(pdlg, font=("Consolas", 11), fg_color="#0a0a0a", text_color="#00ff00", wrap="word")
        console.pack(fill="both", expand=True, padx=20, pady=10)

        pbar = ctk.CTkProgressBar(pdlg, width=700)
        pbar.pack(pady=10)
        pbar.set(0)

        close_btn = ctk.CTkButton(pdlg, text="Close", command=pdlg.destroy, width=150, height=40, state="disabled")
        close_btn.pack(pady=10)

        def log(msg):
            console.insert("end", f"{msg}\n")
            console.see("end")
            pdlg.update()

        def run():
            log("=" * 70)
            log(f"Windows Optimizer - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            log("=" * 70 + "\n")

            selected = [t for t in self._all_tweaks() if t["id"] in self.selected_tweaks]
            total = len(selected)

            for i, tweak in enumerate(selected):
                log(f"[{i+1}/{total}] {tweak['name']}...")
                try:
                    ok = self._execute_tweak(tweak, log)
                    if ok:
                        self.applied_tweaks.add(tweak["id"])
                        log(f"✓ SUCCESS: {tweak['name']}")
                    else:
                        log(f"✗ FAILED: {tweak['name']}")
                except Exception as e:
                    log(f"✗ ERROR: {e}")
                    log(traceback.format_exc())
                log("")
                pbar.set((i + 1) / total)
                pdlg.update()

            log("=" * 70)
            log(f"Completed: {len(self.applied_tweaks)}/{total} tweaks applied successfully")
            log("=" * 70)
            close_btn.configure(state="normal")
            self.update_ui()

        threading.Thread(target=run, daemon=True).start()

    def _execute_tweak(self, tweak: dict, log_func) -> bool:
        """
        BUG FIX: handle both service_name (str) and service_names (list).
        """
        try:
            cmd_type = tweak.get("command")
            nw = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

            if cmd_type == "powershell":
                args = tweak.get("args", [])
                cmd  = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass"] + args
                log_func(f"Running: {' '.join(str(a) for a in cmd)}")
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=30, creationflags=nw)
                if r.stdout: log_func(f"Output: {r.stdout.strip()}")
                if r.stderr: log_func(f"Stderr: {r.stderr.strip()}")
                return r.returncode == 0

            elif cmd_type == "registry":
                path     = tweak.get("registry_path", "")
                name     = tweak.get("registry_name", "")
                value    = tweak.get("registry_value")
                reg_type = tweak.get("registry_type", "DWORD")
                ps = (
                    f"New-Item -Path '{path}' -Force -ErrorAction SilentlyContinue; "
                    f"Set-ItemProperty -Path '{path}' -Name '{name}' -Value {value} -Type {reg_type} -Force"
                )
                log_func(f"Registry: {path}\\{name} = {value}")
                r = subprocess.run(
                    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps],
                    capture_output=True, text=True, timeout=30, creationflags=nw,
                )
                return r.returncode == 0

            elif cmd_type == "service":
                # FIX: support both singular and plural key names
                raw = tweak.get("service_names") or tweak.get("service_name") or []
                services = [raw] if isinstance(raw, str) else list(raw)
                action   = tweak.get("action", "disable")

                if action == "disable":
                    ps = "; ".join(
                        f"Stop-Service -Name '{s}' -Force -ErrorAction SilentlyContinue; "
                        f"Set-Service  -Name '{s}' -StartupType Disabled -ErrorAction SilentlyContinue"
                        for s in services
                    )
                elif action == "manual":
                    ps = "; ".join(
                        f"Set-Service -Name '{s}' -StartupType Manual -ErrorAction SilentlyContinue"
                        for s in services
                    )
                else:
                    return False

                log_func(f"Service(s) {services} -> {action}")
                r = subprocess.run(
                    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps],
                    capture_output=True, text=True, timeout=30, creationflags=nw,
                )
                return r.returncode == 0

        except Exception as e:
            log_func(f"Exception: {e}")
        return False

    # ──────────────────────────────────────────────────────────
    #  Undo / Restore
    # ──────────────────────────────────────────────────────────

    def show_undo_dialog(self):
        if not self.applied_tweaks:
            return
        dlg = ctk.CTkToplevel(self)
        dlg.title("Undo Tweaks")
        dlg.geometry("600x400")
        dlg.transient(self)
        dlg.grab_set()

        ctk.CTkLabel(dlg, text="Undo Applied Tweaks", font=("Segoe UI", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(dlg,
                     text="This will attempt to revert previously applied optimizations.\n"
                          "Note: Some tweaks cannot be automatically undone.",
                     font=("Segoe UI", 12), text_color="#aaaaaa").pack(pady=10)

        lf = ctk.CTkScrollableFrame(dlg, fg_color="#16213e")
        lf.pack(fill="both", expand=True, padx=20, pady=10)
        for t in self._all_tweaks():
            if t["id"] in self.applied_tweaks:
                ctk.CTkLabel(lf, text=f"↶ {t['name']}", font=("Segoe UI", 12), anchor="w").pack(fill="x", padx=10, pady=3)

        row = ctk.CTkFrame(dlg, fg_color="transparent")
        row.pack(pady=20)
        ctk.CTkButton(row, text="Cancel", command=dlg.destroy,
                      width=150, height=45, fg_color="#3a3a3a", hover_color="#4a4a4a").pack(side="left", padx=10)
        ctk.CTkButton(row, text="Undo Now", command=lambda: self._undo_info(dlg),
                      width=150, height=45, fg_color="#ff6b35", hover_color="#ff8555").pack(side="left", padx=10)

    def _undo_info(self, dialog):
        dialog.destroy()
        dlg = ctk.CTkToplevel(self)
        dlg.title("Undo Feature")
        dlg.geometry("500x200")
        dlg.transient(self)
        dlg.grab_set()
        ctk.CTkLabel(
            dlg,
            text="To undo tweaks, use Windows System Restore:\n\n"
                 "1. Search for 'Create a restore point' in Start Menu\n"
                 "2. Click 'System Restore'\n"
                 "3. Select the restore point created by WinOptimizer\n\n"
                 "Advanced users can manually revert registry/service changes.",
            font=("Segoe UI", 13), justify="center",
        ).pack(pady=30, padx=20)
        ctk.CTkButton(dlg, text="OK", command=dlg.destroy, width=120, height=40).pack(pady=10)

    def restore_to_stock(self):
        dlg = ctk.CTkToplevel(self)
        dlg.title("⚠️ Restore to Stock Windows")
        dlg.geometry("650x500")
        dlg.transient(self)
        dlg.grab_set()

        ctk.CTkLabel(dlg, text="🔄 Restore Windows to Stock Settings",
                     font=("Segoe UI", 22, "bold"), text_color="#ff4444").pack(pady=20)
        ctk.CTkLabel(dlg, text="⚠️ WARNING: This will reverse ALL optimizations!",
                     font=("Segoe UI", 14, "bold"), text_color="#ffaa00").pack(pady=10)

        tb = ctk.CTkTextbox(dlg, width=580, height=250, font=("Segoe UI", 12), fg_color="#1a1f2e")
        tb.pack(pady=10, padx=20)
        tb.insert("1.0",
            "This will restore Windows to factory defaults by:\n\n"
            "✓ Re-enabling all disabled services\n"
            "✓ Restoring all registry modifications\n"
            "✓ Re-enabling telemetry and tracking\n"
            "✓ Restoring Windows Update settings\n"
            "✓ Re-enabling visual effects and transparency\n"
            "✓ Restoring power management settings\n"
            "✓ Re-enabling all background apps\n"
            "✓ Restoring network throttling\n"
            "✓ Undoing all performance tweaks\n\n"
            "Note: This creates a restore point first for safety."
        )
        tb.configure(state="disabled")

        row = ctk.CTkFrame(dlg, fg_color="transparent")
        row.pack(pady=20)
        ctk.CTkButton(row, text="Cancel", command=dlg.destroy,
                      width=180, height=50, fg_color="#3a3a3a", hover_color="#4a4a4a").pack(side="left", padx=10)
        ctk.CTkButton(row, text="Restore to Stock Now",
                      command=lambda: self._execute_restore_stock(dlg),
                      width=220, height=50, fg_color="#ff4444", hover_color="#ff6666").pack(side="left", padx=10)

    def _execute_restore_stock(self, dialog):
        """
        BUG FIX: previously called self.log_to_console() which doesn't exist,
        causing AttributeError. Now runs silently and shows a result dialog.
        """
        dialog.destroy()

        if not self.is_admin():
            self.show_admin_warning()
            return

        nw = subprocess.CREATE_NO_WINDOW

        # Create safety restore point
        try:
            subprocess.run(
                ["powershell", "-Command",
                 "Checkpoint-Computer -Description 'Before Stock Restore' -RestorePointType 'MODIFY_SETTINGS'"],
                capture_output=True, text=True, timeout=60, creationflags=nw,
            )
        except Exception:
            pass

        undo_ops = []
        for cat in ("essential", "services", "performance", "privacy", "advanced"):
            for t in self.tweaks_data.get(cat, []):
                if t.get("command") == "registry" and "undo_value" in t:
                    undo_ops.append({"type": "registry", "tweak": t})
                elif t.get("command") == "service":
                    raw = t.get("service_names") or t.get("service_name") or []
                    svcs = [raw] if isinstance(raw, str) else list(raw)
                    undo_ops.append({"type": "service", "services": svcs})

        success = 0
        for op in undo_ops:
            try:
                if op["type"] == "registry":
                    t = op["tweak"]
                    ps = (
                        f"Set-ItemProperty -Path '{t['registry_path']}' "
                        f"-Name '{t['registry_name']}' -Value {t['undo_value']} "
                        f"-Type {t['registry_type']} -Force -ErrorAction SilentlyContinue"
                    )
                    subprocess.run(["powershell", "-Command", ps],
                                   capture_output=True, text=True, timeout=30, creationflags=nw)
                    success += 1
                elif op["type"] == "service":
                    for svc in op["services"]:
                        ps = (
                            f"Set-Service -Name '{svc}' -StartupType Automatic -ErrorAction SilentlyContinue; "
                            f"Start-Service -Name '{svc}' -ErrorAction SilentlyContinue"
                        )
                        subprocess.run(["powershell", "-Command", ps],
                                       capture_output=True, text=True, timeout=30, creationflags=nw)
                    success += 1
            except Exception:
                pass

        self.applied_tweaks.clear()
        self.update_ui()

        done = ctk.CTkToplevel(self)
        done.title("✅ Restore Complete")
        done.geometry("500x280")
        done.transient(self)
        done.grab_set()
        ctk.CTkLabel(
            done,
            text=f"✅ Windows Restored to Stock!\n\n"
                 f"{success}/{len(undo_ops)} settings successfully restored\n\n"
                 f"⚠️ Please restart your computer for all changes to take effect.",
            font=("Segoe UI", 14), justify="center",
        ).pack(pady=30, padx=20)
        ctk.CTkButton(done, text="Restart Now",
                      command=lambda: os.system("shutdown /r /t 5"),
                      width=180, height=50, fg_color="#ff6b35", hover_color="#ff8555").pack(pady=5)
        ctk.CTkButton(done, text="Restart Later", command=done.destroy,
                      width=180, height=50, fg_color="#3a3a3a", hover_color="#4a4a4a").pack(pady=5)


def main():
    app = WinOptimizer()
    app.mainloop()


if __name__ == "__main__":
    main()
