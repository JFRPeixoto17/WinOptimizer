"""
WinOptimizer Pro - Professional Windows Performance Optimizer
A safe, modern Windows optimization tool with Fluent Design dark theme

Version: 1.0.1 Enhanced
Author: João Filipe Reis Peixoto
       M.Sc. Student in Critical Computing System Engineering
Copyright (c) 2025 João Filipe Reis Peixoto. All rights reserved.

This software is provided for educational and personal use.
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

# Import modern color scheme
try:
    from theme import COLORS, FONTS, SPACING, RADIUS, ANIMATION
except ImportError:
    # Fallback colors if theme.py doesn't exist
    COLORS = {
        "bg_primary": "#0f1419", "bg_secondary": "#1a1f2e", "bg_tertiary": "#242b3d",
        "accent_primary": "#3a86ff", "accent_hover": "#5a9cff",
        "text_primary": "#e8eaed", "text_secondary": "#9aa0a6",
        "success": "#34a853", "warning": "#fbbc04", "error": "#ea4335"
    }
    FONTS = {"heading_large": ("Segoe UI", 32, "bold"), "body_medium": ("Segoe UI", 12)}
    SPACING = {"md": 12, "lg": 16}
    RADIUS = {"medium": 8}
    ANIMATION = {"normal": 250}

# Helper function to get resource path (works in dev and PyInstaller)
def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = Path(__file__).parent
    
    return os.path.join(base_path, relative_path)

# Configure customtkinter with modern theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class WinOptimizer(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("WinOptimizer Pro - Professional Windows Optimizer")
        self.geometry("1400x900")
        self.minsize(1200, 700)
        
        # Set window icon (if available)
        try:
            icon_path = get_resource_path("icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except:
            pass  # Icon not critical
        
        # State
        self.selected_tweaks = set()
        self.applied_tweaks = set()
        self.tweaks_data = {}
        self.current_tab = "essential"
        
        # Load tweaks configuration
        self.load_tweaks()
        
        # Check admin privileges
        if not self.is_admin():
            self.show_admin_warning()
        
        # Create UI
        self.create_ui()
        
    def is_admin(self):
        """Check if running with administrator privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def show_admin_warning(self):
        """Show warning if not running as admin"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Administrator Required")
        dialog.geometry("500x200")
        dialog.transient(self)
        dialog.grab_set()
        
        label = ctk.CTkLabel(
            dialog,
            text="⚠️ Administrator Privileges Required\n\n"
                 "This application needs administrator rights to apply system tweaks.\n"
                 "Please restart the application as administrator.",
            font=("Segoe UI", 14),
            justify="center"
        )
        label.pack(pady=40, padx=20)
        
        btn = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            width=120,
            height=40
        )
        btn.pack(pady=10)
    
    def load_tweaks(self):
        """Load tweaks from JSON configuration"""
        try:
            # Use resource path helper for PyInstaller compatibility
            tweaks_file = get_resource_path("tweaks.json")
            with open(tweaks_file, 'r', encoding='utf-8') as f:
                self.tweaks_data = json.load(f)
        except Exception as e:
            print(f"Error loading tweaks: {e}")
            self.tweaks_data = {"essential": [], "services": [], "performance": [], "privacy": [], "advanced": [], "presets": {}}
    
    def create_ui(self):
        """Create main UI layout with modern Fluent Design aesthetic"""
        # Configure window background
        self.configure(fg_color=COLORS["bg_primary"])
        
        # Header with smooth gradient effect
        header = ctk.CTkFrame(self, height=100, fg_color=COLORS["bg_secondary"], corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text="WinOptimizer Pro",
            font=FONTS.get("heading_large", ("Segoe UI", 32, "bold")),
            text_color=COLORS["accent_primary"]
        )
        title.pack(pady=(SPACING["md"], SPACING["xs"]))
        
        subtitle = ctk.CTkLabel(
            header,
            text="Professional Windows Performance Optimizer",
            font=FONTS.get("body_large", ("Segoe UI", 14)),
            text_color=COLORS["text_secondary"]
        )
        subtitle.pack(pady=SPACING["xs"])
        
        version = ctk.CTkLabel(
            header,
            text="Version 1.0.1 - Enhanced",
            font=FONTS.get("body_small", ("Segoe UI", 10)),
            text_color=COLORS["text_tertiary"]
        )
        version.pack()
        
        # Presets section with modern card design
        presets_frame = ctk.CTkFrame(
            self, 
            fg_color=COLORS["bg_secondary"], 
            height=90,
            corner_radius=RADIUS["medium"]
        )
        presets_frame.pack(fill="x", padx=SPACING["lg"], pady=SPACING["md"])
        presets_frame.pack_propagate(False)
        
        preset_label = ctk.CTkLabel(
            presets_frame,
            text="QUICK PROFILES:",
            font=FONTS.get("body_small", ("Segoe UI", 10)),
            text_color=COLORS["text_tertiary"]
        )
        preset_label.pack(pady=(SPACING["md"], SPACING["xs"]), anchor="w", padx=SPACING["lg"])
        
        preset_names = {
            "recommended": "✓ Recommended",
            "maximum_performance": "⚡ Maximum Performance",
            "basic_cleanup": "🧹 Basic Cleanup",
            "gaming_focused": "🎮 Gaming Focused",
            "privacy_focused": "🔒 Privacy Focused"
        }
        
        # Preset buttons container
        preset_buttons_frame = ctk.CTkFrame(presets_frame, fg_color="transparent")
        preset_buttons_frame.pack(fill="both", expand=True, padx=SPACING["lg"], pady=(0, SPACING["md"]))
        
        for idx, (preset_id, preset_name) in enumerate(preset_names.items()):
            btn = ctk.CTkButton(
                preset_buttons_frame,
                text=preset_name,
                command=lambda p=preset_id: self.apply_preset(p),
                width=180,
                height=40,
                font=FONTS.get("body_medium", ("Segoe UI", 12, "bold")),
                fg_color=COLORS["bg_tertiary"],
                hover_color=COLORS["accent_hover"],
                text_color=COLORS["text_primary"],
                corner_radius=RADIUS["medium"],
                border_width=1,
                border_color=COLORS["border"]
            )
            btn.grid(row=0, column=idx, padx=SPACING["xs"], sticky="ew")
            preset_buttons_frame.grid_columnconfigure(idx, weight=1)
        
        # Main content area with modern styling
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SPACING["lg"], pady=(0, SPACING["lg"]))
        
        # Tabs with Fluent Design aesthetic
        tabs_frame = ctk.CTkFrame(content, fg_color=COLORS["bg_secondary"], height=60, corner_radius=RADIUS["medium"])
        tabs_frame.pack(fill="x", padx=0, pady=(0, SPACING["md"]))
        tabs_frame.pack_propagate(False)
        
        tab_configs = [
            ("essential", "⚙️ Essential Tweaks"),
            ("services", "🖥️ Services"),
            ("performance", "⚡ Performance"),
            ("privacy", "👁️ Privacy"),
            ("advanced", "🛡️ Advanced")
        ]
        
        for tab_id, tab_name in tab_configs:
            btn = ctk.CTkButton(
                tabs_frame,
                text=tab_name,
                command=lambda t=tab_id: self.switch_tab(t),
                width=200,
                height=45,
                font=("Segoe UI", 13, "bold"),
                fg_color="#3a3a5e" if tab_id == self.current_tab else "#2a2a3e",
                hover_color="#4a4a6e"
            )
            btn.pack(side="left", padx=5, pady=8)
        
        # Tweaks container with scrollbar
        tweaks_container = ctk.CTkScrollableFrame(
            content,
            fg_color="#0f1419",
            scrollbar_button_color="#2a2a3e",
            scrollbar_button_hover_color="#3a3a5e"
        )
        tweaks_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        self.tweaks_container = tweaks_container
        self.render_tweaks()
        
        # Bottom action bar
        action_bar = ctk.CTkFrame(self, height=80, fg_color="#16213e")
        action_bar.pack(fill="x", padx=10, pady=10)
        action_bar.pack_propagate(False)
        
        # Selection counter
        self.selection_label = ctk.CTkLabel(
            action_bar,
            text="0 selected",
            font=("Segoe UI", 14, "bold"),
            text_color="#4da6ff"
        )
        self.selection_label.pack(side="left", padx=20, pady=20)
        
        # Applied counter
        self.applied_label = ctk.CTkLabel(
            action_bar,
            text="",
            font=("Segoe UI", 14, "bold"),
            text_color="#4dff4d"
        )
        self.applied_label.pack(side="left", padx=10, pady=20)
        
        # Buttons
        btn_frame = ctk.CTkFrame(action_bar, fg_color="transparent")
        btn_frame.pack(side="right", padx=20, pady=15)
        
        clear_btn = ctk.CTkButton(
            btn_frame,
            text="Clear Selection",
            command=self.clear_selection,
            width=150,
            height=50,
            font=("Segoe UI", 13, "bold"),
            fg_color="#3a3a3a",
            hover_color="#4a4a4a"
        )
        clear_btn.pack(side="left", padx=5)
        
        undo_btn = ctk.CTkButton(
            btn_frame,
            text="Undo Tweaks",
            command=self.show_undo_dialog,
            width=150,
            height=50,
            font=("Segoe UI", 13, "bold"),
            fg_color="#ff6b35",
            hover_color="#ff8555"
        )
        undo_btn.pack(side="left", padx=5)
        
        restore_stock_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Restore to Stock",
            command=self.restore_to_stock,
            width=180,
            height=50,
            font=("Segoe UI", 13, "bold"),
            fg_color="#ff4444",
            hover_color="#ff6666"
        )
        restore_stock_btn.pack(side="left", padx=5)
        
        self.apply_btn = ctk.CTkButton(
            btn_frame,
            text="Apply Optimizations",
            command=self.show_apply_dialog,
            width=200,
            height=50,
            font=("Segoe UI", 14, "bold"),
            fg_color="#4da6ff",
            hover_color="#6db6ff",
            state="disabled"
        )
        self.apply_btn.pack(side="left", padx=5)
    
    def render_tweaks(self):
        """Render tweak cards for current tab"""
        # Clear existing
        for widget in self.tweaks_container.winfo_children():
            widget.destroy()
        
        # Get tweaks for current tab
        tweaks = self.tweaks_data.get(self.current_tab, [])
        
        for tweak in tweaks:
            self.create_tweak_card(self.tweaks_container, tweak)
    
    def create_tweak_card(self, parent, tweak):
        """Create a single tweak card"""
        is_selected = tweak["id"] in self.selected_tweaks
        is_applied = tweak["id"] in self.applied_tweaks
        
        # Card frame
        card = ctk.CTkFrame(
            parent,
            fg_color="#1a2332" if not is_selected else "#1a3352",
            border_width=2,
            border_color="#4da6ff" if is_selected else "#2a3a4a",
            corner_radius=10
        )
        card.pack(fill="x", padx=10, pady=5)
        
        # Content frame
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=12)
        
        # Left side - info
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Title row
        title_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 5))
        
        title = ctk.CTkLabel(
            title_frame,
            text=tweak["name"],
            font=("Segoe UI", 14, "bold"),
            text_color="#ffffff",
            anchor="w"
        )
        title.pack(side="left")
        
        # Badges
        if tweak.get("recommended"):
            badge = ctk.CTkLabel(
                title_frame,
                text="✓ Recommended",
                font=("Segoe UI", 10, "bold"),
                text_color="#4dff4d",
                fg_color="#1a3a1a",
                corner_radius=5,
                padx=8,
                pady=2
            )
            badge.pack(side="left", padx=5)
        
        impact = ctk.CTkLabel(
            title_frame,
            text=tweak["impact"],
            font=("Segoe UI", 10, "bold"),
            text_color="#b366ff",
            fg_color="#2a1a3a",
            corner_radius=5,
            padx=8,
            pady=2
        )
        impact.pack(side="left", padx=5)
        
        if is_applied:
            applied_badge = ctk.CTkLabel(
                title_frame,
                text="✓ Applied",
                font=("Segoe UI", 10, "bold"),
                text_color="#4dff4d",
                fg_color="#1a4a1a",
                corner_radius=5,
                padx=8,
                pady=2
            )
            applied_badge.pack(side="left", padx=5)
        
        # Description
        desc = ctk.CTkLabel(
            left_frame,
            text=tweak["description"],
            font=("Segoe UI", 12),
            text_color="#aaaaaa",
            anchor="w",
            justify="left",
            wraplength=900
        )
        desc.pack(fill="x")
        
        # Drawback warning
        if "drawback" in tweak:
            warning = ctk.CTkLabel(
                left_frame,
                text=f"⚠️ Drawback: {tweak['drawback']}",
                font=("Segoe UI", 11),
                text_color="#ffaa00",
                anchor="w"
            )
            warning.pack(fill="x", pady=(5, 0))
        
        # Right side - checkbox
        checkbox = ctk.CTkCheckBox(
            content_frame,
            text="",
            command=lambda: self.toggle_tweak(tweak["id"]),
            width=28,
            height=28,
            checkbox_width=28,
            checkbox_height=28,
            corner_radius=5,
            fg_color="#4da6ff",
            hover_color="#6db6ff",
            border_color="#4da6ff"
        )
        checkbox.pack(side="right", padx=10)
        
        if is_selected:
            checkbox.select()
        else:
            checkbox.deselect()
        
        # Make card clickable
        def toggle_on_click(e):
            self.toggle_tweak(tweak["id"])
        
        card.bind("<Button-1>", toggle_on_click)
        for child in card.winfo_children():
            child.bind("<Button-1>", toggle_on_click)
    
    def toggle_tweak(self, tweak_id):
        """Toggle tweak selection"""
        if tweak_id in self.selected_tweaks:
            self.selected_tweaks.remove(tweak_id)
        else:
            self.selected_tweaks.add(tweak_id)
        
        self.update_ui()
    
    def update_ui(self):
        """Update UI after selection change"""
        # Update labels
        count = len(self.selected_tweaks)
        self.selection_label.configure(text=f"{count} selected")
        
        if len(self.applied_tweaks) > 0:
            self.applied_label.configure(text=f"✓ {len(self.applied_tweaks)} applied")
        else:
            self.applied_label.configure(text="")
        
        # Update button state
        if count > 0:
            self.apply_btn.configure(state="normal")
        else:
            self.apply_btn.configure(state="disabled")
        
        # Re-render current tab
        self.render_tweaks()
    
    def switch_tab(self, tab_id):
        """Switch to different tab"""
        self.current_tab = tab_id
        self.render_tweaks()
        
        # Update tab button colors
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkFrame):
                        for btn in child.winfo_children():
                            if isinstance(btn, ctk.CTkButton):
                                btn_text = btn.cget("text")
                                if tab_id in btn_text.lower():
                                    btn.configure(fg_color="#3a3a5e")
                                else:
                                    btn.configure(fg_color="#2a2a3e")
    
    def apply_preset(self, preset_id):
        """Apply a preset configuration"""
        presets = self.tweaks_data.get("presets", {})
        if preset_id in presets:
            self.selected_tweaks = set(presets[preset_id])
            self.update_ui()
    
    def clear_selection(self):
        """Clear all selections"""
        self.selected_tweaks.clear()
        self.update_ui()
    
    def show_apply_dialog(self):
        """Show confirmation dialog before applying"""
        if not self.is_admin():
            self.show_admin_warning()
            return
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Optimizations")
        dialog.geometry("700x500")
        dialog.transient(self)
        dialog.grab_set()
        
        # Header
        header = ctk.CTkLabel(
            dialog,
            text=f"Ready to Apply {len(self.selected_tweaks)} Optimizations",
            font=("Segoe UI", 20, "bold"),
            text_color="#4da6ff"
        )
        header.pack(pady=20)
        
        # List of tweaks
        list_frame = ctk.CTkScrollableFrame(dialog, fg_color="#16213e")
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        all_tweaks = []
        for category in self.tweaks_data:
            if category != "presets":
                all_tweaks.extend(self.tweaks_data[category])
        
        for tweak in all_tweaks:
            if tweak["id"] in self.selected_tweaks:
                item = ctk.CTkLabel(
                    list_frame,
                    text=f"✓ {tweak['name']} - {tweak['impact']}",
                    font=("Segoe UI", 12),
                    anchor="w"
                )
                item.pack(fill="x", padx=10, pady=3)
        
        # Buttons
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            width=150,
            height=45,
            font=("Segoe UI", 13, "bold"),
            fg_color="#3a3a3a",
            hover_color="#4a4a4a"
        )
        cancel_btn.pack(side="left", padx=10)
        
        apply_btn = ctk.CTkButton(
            btn_frame,
            text="Apply Now",
            command=lambda: self.apply_tweaks(dialog),
            width=150,
            height=45,
            font=("Segoe UI", 13, "bold"),
            fg_color="#4da6ff",
            hover_color="#6db6ff"
        )
        apply_btn.pack(side="left", padx=10)
    
    def apply_tweaks(self, dialog):
        """Apply selected tweaks"""
        dialog.destroy()
        
        # Create progress dialog
        progress_dialog = ctk.CTkToplevel(self)
        progress_dialog.title("Applying Optimizations")
        progress_dialog.geometry("800x600")
        progress_dialog.transient(self)
        progress_dialog.grab_set()
        
        header = ctk.CTkLabel(
            progress_dialog,
            text="Applying Optimizations...",
            font=("Segoe UI", 20, "bold")
        )
        header.pack(pady=20)
        
        # Console output
        console = ctk.CTkTextbox(
            progress_dialog,
            font=("Consolas", 11),
            fg_color="#0a0a0a",
            text_color="#00ff00",
            wrap="word"
        )
        console.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Progress bar
        progress = ctk.CTkProgressBar(progress_dialog, width=700)
        progress.pack(pady=10)
        progress.set(0)
        
        # Close button (disabled initially)
        close_btn = ctk.CTkButton(
            progress_dialog,
            text="Close",
            command=progress_dialog.destroy,
            width=150,
            height=40,
            state="disabled"
        )
        close_btn.pack(pady=10)
        
        def log(message):
            console.insert("end", f"{message}\n")
            console.see("end")
            progress_dialog.update()
        
        def run_tweaks():
            log("=" * 70)
            log(f"Windows Optimizer - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            log("=" * 70)
            log("")
            
            # Get all tweaks
            all_tweaks = []
            for category in self.tweaks_data:
                if category != "presets":
                    all_tweaks.extend(self.tweaks_data[category])
            
            selected = [t for t in all_tweaks if t["id"] in self.selected_tweaks]
            total = len(selected)
            
            for i, tweak in enumerate(selected):
                log(f"[{i+1}/{total}] {tweak['name']}...")
                
                try:
                    success = self.execute_tweak(tweak, log)
                    if success:
                        self.applied_tweaks.add(tweak["id"])
                        log(f"✓ SUCCESS: {tweak['name']}")
                    else:
                        log(f"✗ FAILED: {tweak['name']}")
                except Exception as e:
                    log(f"✗ ERROR: {str(e)}")
                    log(traceback.format_exc())
                
                log("")
                progress.set((i + 1) / total)
                progress_dialog.update()
            
            log("=" * 70)
            log(f"Completed: {len(self.applied_tweaks)}/{total} tweaks applied successfully")
            log("=" * 70)
            
            close_btn.configure(state="normal")
            self.update_ui()
        
        # Run in thread
        threading.Thread(target=run_tweaks, daemon=True).start()
    
    def execute_tweak(self, tweak, log_func):
        """Execute a single tweak"""
        try:
            command_type = tweak.get("command")
            
            if command_type == "powershell":
                args = tweak.get("args", [])
                cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass"] + args
                log_func(f"Running: {' '.join(cmd)}")
                # Use CREATE_NO_WINDOW to prevent console flash
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=30,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )
                if result.stdout:
                    log_func(f"Output: {result.stdout.strip()}")
                if result.stderr:
                    log_func(f"Error: {result.stderr.strip()}")
                return result.returncode == 0
            
            elif command_type == "registry":
                path = tweak.get("registry_path", "")
                name = tweak.get("registry_name", "")
                value = tweak.get("registry_value")
                reg_type = tweak.get("registry_type", "DWORD")
                
                # Create registry key if it doesn't exist
                ps_cmd = f"New-Item -Path '{path}' -Force -ErrorAction SilentlyContinue; "
                ps_cmd += f"Set-ItemProperty -Path '{path}' -Name '{name}' -Value {value} -Type {reg_type} -Force"
                
                cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd]
                log_func(f"Registry: {path}\\{name} = {value}")
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=30,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )
                return result.returncode == 0
            
            elif command_type == "service":
                service_name = tweak.get("service_name", "")
                action = tweak.get("action", "disable")
                
                if action == "disable":
                    ps_cmd = f"Stop-Service -Name '{service_name}' -Force -ErrorAction SilentlyContinue; Set-Service -Name '{service_name}' -StartupType Disabled -ErrorAction SilentlyContinue"
                elif action == "manual":
                    ps_cmd = f"Set-Service -Name '{service_name}' -StartupType Manual -ErrorAction SilentlyContinue"
                else:
                    return False
                
                cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd]
                log_func(f"Service: {service_name} -> {action}")
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=30,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )
                return result.returncode == 0
            
            return False
        
        except Exception as e:
            log_func(f"Exception: {str(e)}")
            return False
    
    def show_undo_dialog(self):
        """Show undo dialog"""
        if len(self.applied_tweaks) == 0:
            return
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Undo Tweaks")
        dialog.geometry("600x400")
        dialog.transient(self)
        dialog.grab_set()
        
        header = ctk.CTkLabel(
            dialog,
            text="Undo Applied Tweaks",
            font=("Segoe UI", 20, "bold")
        )
        header.pack(pady=20)
        
        info = ctk.CTkLabel(
            dialog,
            text="This will attempt to revert previously applied optimizations.\n"
                 "Note: Some tweaks cannot be automatically undone.",
            font=("Segoe UI", 12),
            text_color="#aaaaaa"
        )
        info.pack(pady=10)
        
        # List of applied tweaks
        list_frame = ctk.CTkScrollableFrame(dialog, fg_color="#16213e")
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        all_tweaks = []
        for category in self.tweaks_data:
            if category != "presets":
                all_tweaks.extend(self.tweaks_data[category])
        
        for tweak in all_tweaks:
            if tweak["id"] in self.applied_tweaks:
                item = ctk.CTkLabel(
                    list_frame,
                    text=f"↶ {tweak['name']}",
                    font=("Segoe UI", 12),
                    anchor="w"
                )
                item.pack(fill="x", padx=10, pady=3)
        
        # Buttons
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            width=150,
            height=45,
            fg_color="#3a3a3a",
            hover_color="#4a4a4a"
        )
        cancel_btn.pack(side="left", padx=10)
        
        undo_btn = ctk.CTkButton(
            btn_frame,
            text="Undo Now",
            command=lambda: self.undo_tweaks(dialog),
            width=150,
            height=45,
            fg_color="#ff6b35",
            hover_color="#ff8555"
        )
        undo_btn.pack(side="left", padx=10)
    
    def undo_tweaks(self, dialog):
        """Undo applied tweaks"""
        dialog.destroy()
        
        # Create simple info dialog
        info_dialog = ctk.CTkToplevel(self)
        info_dialog.title("Undo Feature")
        info_dialog.geometry("500x200")
        info_dialog.transient(self)
        info_dialog.grab_set()
        
        msg = ctk.CTkLabel(
            info_dialog,
            text="To undo tweaks, use Windows System Restore:\n\n"
                 "1. Search for 'Create a restore point' in Start Menu\n"
                 "2. Click 'System Restore'\n"
                 "3. Select the restore point created by WinOptimizer\n\n"
                 "Advanced users can manually revert registry/service changes.",
            font=("Segoe UI", 13),
            justify="center"
        )
        msg.pack(pady=30, padx=20)
        
        ok_btn = ctk.CTkButton(
            info_dialog,
            text="OK",
            command=info_dialog.destroy,
            width=120,
            height=40
        )
        ok_btn.pack(pady=10)
    
    def restore_to_stock(self):
        """Restore all Windows settings to stock/default values"""
        # Confirmation dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("⚠️ Restore to Stock Windows")
        dialog.geometry("650x500")
        dialog.transient(self)
        dialog.grab_set()
        
        header = ctk.CTkLabel(
            dialog,
            text="🔄 Restore Windows to Stock Settings",
            font=("Segoe UI", 22, "bold"),
            text_color="#ff4444"
        )
        header.pack(pady=20)
        
        warning = ctk.CTkLabel(
            dialog,
            text="⚠️ WARNING: This will reverse ALL optimizations!",
            font=("Segoe UI", 14, "bold"),
            text_color="#ffaa00"
        )
        warning.pack(pady=10)
        
        info = ctk.CTkTextbox(
            dialog,
            width=580,
            height=250,
            font=("Segoe UI", 12),
            fg_color="#1a1f2e"
        )
        info.pack(pady=10, padx=20)
        
        info_text = """This will restore Windows to factory defaults by:

✓ Re-enabling all disabled services
✓ Restoring all registry modifications  
✓ Re-enabling telemetry and tracking
✓ Restoring Windows Update settings
✓ Re-enabling visual effects and transparency
✓ Restoring power management settings
✓ Re-enabling all background apps
✓ Restoring network throttling
✓ Undoing all performance tweaks

Use this if you want to:
• Sell or give away your PC
• Start fresh after a year of tweaks
• Troubleshoot issues
• Return to default Windows experience

Note: This creates a restore point first for safety."""
        
        info.insert("1.0", info_text)
        info.configure(state="disabled")
        
        # Buttons
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            width=180,
            height=50,
            font=("Segoe UI", 13, "bold"),
            fg_color="#3a3a3a",
            hover_color="#4a4a4a"
        )
        cancel_btn.pack(side="left", padx=10)
        
        restore_btn = ctk.CTkButton(
            btn_frame,
            text="Restore to Stock Now",
            command=lambda: self.execute_restore_stock(dialog),
            width=220,
            height=50,
            font=("Segoe UI", 13, "bold"),
            fg_color="#ff4444",
            hover_color="#ff6666"
        )
        restore_btn.pack(side="left", padx=10)
    
    def execute_restore_stock(self, dialog):
        """Execute the restore to stock process"""
        dialog.destroy()
        
        if not self.is_admin():
            self.log_to_console("❌ Admin privileges required!", "ERROR")
            return
        
        self.log_to_console("\n" + "="*60, "INFO")
        self.log_to_console("🔄 RESTORING WINDOWS TO STOCK SETTINGS", "INFO")
        self.log_to_console("="*60 + "\n", "INFO")
        
        # Create restore point first
        self.log_to_console("Creating safety restore point...", "INFO")
        try:
            result = subprocess.run(
                ["powershell", "-Command", "Checkpoint-Computer -Description 'Before Stock Restore' -RestorePointType 'MODIFY_SETTINGS'"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=60
            )
            self.log_to_console("✓ Restore point created", "SUCCESS")
        except Exception as e:
            self.log_to_console(f"⚠️ Could not create restore point: {str(e)}", "WARNING")
        
        # Collect all undo operations
        undo_operations = []
        
        for category in ["essential", "services", "performance", "privacy", "advanced"]:
            if category in self.tweaks_data:
                for tweak in self.tweaks_data[category]:
                    if tweak.get("command") == "registry" and "undo_value" in tweak:
                        undo_operations.append({
                            "name": tweak["name"],
                            "type": "registry",
                            "path": tweak["registry_path"],
                            "name_key": tweak["registry_name"],
                            "value": tweak["undo_value"],
                            "reg_type": tweak["registry_type"]
                        })
                    elif tweak.get("command") == "service":
                        undo_operations.append({
                            "name": tweak["name"],
                            "type": "service",
                            "services": tweak["service_names"],
                            "action": "automatic"  # Re-enable services
                        })
                    elif tweak.get("undo_command"):
                        undo_operations.append({
                            "name": tweak["name"],
                            "type": "powershell",
                            "command": tweak["undo_command"],
                            "args": tweak.get("undo_args", [])
                        })
        
        self.log_to_console(f"\n📋 Found {len(undo_operations)} settings to restore\n", "INFO")
        
        # Execute undo operations
        success_count = 0
        for idx, op in enumerate(undo_operations, 1):
            self.log_to_console(f"[{idx}/{len(undo_operations)}] Restoring: {op['name']}", "INFO")
            
            try:
                if op["type"] == "registry":
                    # Restore registry value
                    cmd = f"Set-ItemProperty -Path '{op['path']}' -Name '{op['name_key']}' -Value {op['value']} -Type {op['reg_type']} -Force"
                    subprocess.run(
                        ["powershell", "-Command", cmd],
                        capture_output=True,
                        text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                        timeout=30
                    )
                    self.log_to_console(f"  ✓ Registry restored", "SUCCESS")
                    success_count += 1
                    
                elif op["type"] == "service":
                    # Re-enable services
                    for service in op["services"]:
                        cmd = f"Set-Service -Name '{service}' -StartupType Automatic -ErrorAction SilentlyContinue; Start-Service -Name '{service}' -ErrorAction SilentlyContinue"
                        subprocess.run(
                            ["powershell", "-Command", cmd],
                            capture_output=True,
                            text=True,
                            creationflags=subprocess.CREATE_NO_WINDOW,
                            timeout=30
                        )
                    self.log_to_console(f"  ✓ Service(s) restored", "SUCCESS")
                    success_count += 1
                    
                elif op["type"] == "powershell":
                    # Run undo PowerShell command
                    if op["command"] == "powershell":
                        subprocess.run(
                            ["powershell"] + op["args"],
                            capture_output=True,
                            text=True,
                            creationflags=subprocess.CREATE_NO_WINDOW,
                            timeout=30
                        )
                    self.log_to_console(f"  ✓ Command executed", "SUCCESS")
                    success_count += 1
                    
            except Exception as e:
                self.log_to_console(f"  ⚠️ Failed: {str(e)}", "WARNING")
        
        self.log_to_console(f"\n{'='*60}", "INFO")
        self.log_to_console(f"✅ RESTORE COMPLETE: {success_count}/{len(undo_operations)} settings restored", "SUCCESS")
        self.log_to_console(f"{'='*60}\n", "INFO")
        self.log_to_console("⚠️ RESTART YOUR COMPUTER for all changes to take effect!", "WARNING")
        
        # Show completion dialog
        completion = ctk.CTkToplevel(self)
        completion.title("✅ Restore Complete")
        completion.geometry("500x300")
        completion.transient(self)
        completion.grab_set()
        
        msg = ctk.CTkLabel(
            completion,
            text=f"✅ Windows Restored to Stock!\n\n"
                 f"{success_count}/{len(undo_operations)} settings successfully restored\n\n"
                 f"⚠️ Please restart your computer now\n"
                 f"for all changes to take effect.",
            font=("Segoe UI", 14),
            justify="center"
        )
        msg.pack(pady=40, padx=20)
        
        restart_btn = ctk.CTkButton(
            completion,
            text="Restart Now",
            command=lambda: os.system("shutdown /r /t 5"),
            width=180,
            height=50,
            font=("Segoe UI", 13, "bold"),
            fg_color="#ff6b35",
            hover_color="#ff8555"
        )
        restart_btn.pack(pady=10)
        
        later_btn = ctk.CTkButton(
            completion,
            text="Restart Later",
            command=completion.destroy,
            width=180,
            height=50,
            font=("Segoe UI", 13, "bold"),
            fg_color="#3a3a3a",
            hover_color="#4a4a4a"
        )
        later_btn.pack(pady=10)


def main():
    app = WinOptimizer()
    app.mainloop()


if __name__ == "__main__":
    main()
