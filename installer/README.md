# WinOptimizer Pro - Installation Package

**Professional Windows Performance Optimizer**  
**Version:** 1.0.1  
**Author:** João Filipe Reis Peixoto

---

## 📦 What's Included

This package contains everything you need to install and use WinOptimizer Pro:

- **WinOptimizerPro.exe** - The application (located in ../dist/)
- **Install.ps1** - Simple PowerShell installer
- **This README** - Installation instructions

---

## 🚀 Quick Installation (2 Steps)

### Step 1: Open PowerShell as Administrator
- Press `Windows + X`
- Click "Windows PowerShell (Admin)" or "Terminal (Admin)"

### Step 2: Run the installer
```powershell
cd "path\to\this\folder"
.\Install.ps1
```

**Example:**
```powershell
cd "C:\Users\YourName\Downloads\WinOptimizer\installer"
.\Install.ps1
```

### Step 3: Follow the prompts
- The installer will ask if you want a desktop shortcut (Y/N)
- That's it! Installation takes ~5 seconds

---

## 📍 After Installation

**Where to find it:**
- **Start Menu:** Search "WinOptimizer Pro"
- **Desktop:** Shortcut (if you chose yes)
- **Installed at:** `C:\Program Files\WinOptimizer Pro\`

**How to use:**
1. Launch WinOptimizer Pro
2. Select the tweaks you want to apply
3. Click "Apply Optimizations"
4. Restart your PC when done

---

## ❓ Features

- **60 Performance Optimizations** - Tested and safe
- **5 Quick Presets** - One-click optimization profiles
- **Restore to Stock** - Revert ALL changes anytime
- **Gaming Tweaks** - Special optimizations for gamers
- **Modern UI** - Beautiful dark theme

---

## 🗑️ How to Uninstall

**Start Menu** → Search "Uninstall WinOptimizer Pro" → Click it

OR

**Windows Settings** → Apps → WinOptimizer Pro → Uninstall

---

## ⚠️ Requirements

- **OS:** Windows 10 or Windows 11
- **Privileges:** Administrator rights required
- **Space:** ~20 MB

---

## 💡 Alternative: No Installation

Don't want to install? Just run the .exe directly:

1. Go to the `dist` folder
2. Right-click `WinOptimizerPro.exe`
3. Click "Run as administrator"

---

## 📝 License

Copyright © 2025 João Filipe Reis Peixoto. All rights reserved.

This software is provided for personal and educational use.  
See LICENSE.txt for full terms.

---

## 🆘 Troubleshooting

**"Cannot run scripts"**
- Run PowerShell as Administrator
- Type: `Set-ExecutionPolicy Bypass -Scope Process`
- Then run the installer again

**".exe not found"**
- Make sure the `dist` folder is in the parent directory
- The structure should be:
  ```
  WinOptimizer/
  ├── dist/WinOptimizerPro.exe
  └── installer/Install.ps1
  ```

---

**Need help?** Check the main README.md in the parent folder.

**Ready to optimize your Windows? Let's go! 🚀**
