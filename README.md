# WinOptimizer Pro

**Professional Windows Performance Optimizer**  
A safe, modern Windows optimization tool with beautiful UI and 60+ tested tweaks.

**Latest: v1.3.0** — real license system, working per-tweak Undo, cross-session state, in-app activation, tweak search, and an Inno Setup installer.

**Author:** João Filipe Reis Peixoto  
**M.Sc. Student in Critical Computing System Engineering**  
**Copyright © 2025 João Filipe Reis Peixoto. All rights reserved.**

---

## 🎯 Features

- ✅ **60 Tested Optimizations** - Safe and reversible
- ✅ **Modern UI** - Smooth colors and Fluent Design
- ✅ **5 Quick Presets** - One-click optimization
- ✅ **Restore to Stock** - Undo ALL changes anytime
- ✅ **Gaming Tweaks** - Special performance boosts
- ✅ **No Dependencies** - Standalone executable

---

## 🚀 For End Users

### Installation

**See the installer folder for complete instructions!**

Quick steps:
1. Open PowerShell as Admin
2. cd installer
3. .\Install.ps1
4. Done!

**Or use directly:** Run dist\WinOptimizerPro.exe as administrator

---

## 👨‍💻 For Developers

### Project Structure

`
WinOptimizer/
├── main.py              # Main application
├── theme.py             # UI colors (smooth & refined)
├── license_manager.py   # Offline license validation (HMAC keys)
├── keygen.py            # DEV tool: mint Pro keys (do not ship)
├── tweaks.json          # All 60 optimizations (Win11-audited)
├── requirements.txt     # Python dependencies
├── build_professional.ps1  # Build .exe
├── dist/
│   └── WinOptimizerPro.exe  # Ready to use (19.34 MB)
└── installer/
    ├── Install.ps1      # PowerShell installer
    ├── WinOptimizer.iss # Inno Setup installer script
    └── README.md        # Installation guide
`

### Build from Source

`powershell
# Install dependencies
pip install -r requirements.txt

# Run from source
python main.py

# Build executable
.\build_professional.ps1
`

---

## 📖 Documentation

- **For Users:** See installer/README.md
- **License:** See LICENSE.txt

---

## ⚠️ Important

1. **Requires Administrator Rights** - To modify system settings
2. **Creates Restore Point** - Automatic backup before changes
3. **Restart Required** - For changes to take effect
4. **Windows 10/11** - Tested on modern Windows versions

---

## 🔧 Categories

- **Essential** - Basic optimizations for everyone
- **Services** - Disable unnecessary services
- **Performance** - Speed and responsiveness
- **Privacy** - Disable telemetry and tracking
- **Advanced** - Power-user tweaks (including gaming)

---

## 🎮 Gaming Features

- Memory compression control
- LAPIC timer optimization
- Dynamic tick management
- GPU hardware scheduling
- Game mode enhancements

---

## 🔑 Licensing (Free vs Pro)

WinOptimizer ships as **Free** by default. Pro unlocks the Services, Performance,
Privacy and Advanced tabs plus Quick Presets.

**For users:** open *Upgrade to Pro → Activate*, then paste your name and key.
The key is validated fully offline and stored in `%APPDATA%\\WinOptimizer\\license.json`.

**For the author (issuing keys):**

```powershell
python keygen.py "customer@email.com"
# -> prints: WO-XXXXX-XXXXX-XXXXX-XXXXX
```

Keys are name-bound and signed with HMAC-SHA256. Change the `_SECRET` in
`license_manager.py` once before issuing real keys, then keep it private.
`keygen.py` is a developer tool and must **not** be included in the public build.

---

## 🆕 What's new in 1.3.0

- **Real license system** — offline, name-bound keys; `IS_PRO` now reflects an actual check.
- **Working Undo** — reverts registry/service/PowerShell tweaks using each tweak's
  defined undo, with a per-service default-startup map (no more forcing everything to Automatic).
- **State persistence** — applied tweaks are remembered between sessions.
- **In-app activation**, **tweak search**, and a **Select Recommended** button.
- **Inno Setup installer** (`installer/WinOptimizer.iss`).
- **Win11 command audit (v1.2.1)** — fixed location tracking, background apps, mouse
  acceleration, and an `autoBackup` bug that wrongly disabled System Restore.

---

## 📝 License

Copyright © 2025 João Filipe Reis Peixoto. All rights reserved.

This software is provided "as is" without warranty.  
For personal and educational use. See LICENSE.txt for details.

---

**Made with ❤️ for Windows optimization enthusiasts!**
