"""
WinOptimizer Pro - Modern Color Scheme
Fluent Design inspired dark theme with smooth gradients

Author: João Filipe Reis Peixoto
       M.Sc. Student in Critical Computing System Engineering
Copyright (c) 2025 João Filipe Reis Peixoto. All rights reserved.
"""

COLORS = {
    # Background colors - Smooth dark gradients
    "bg_primary": "#0f1419",      # Main background - Deep dark blue-black
    "bg_secondary": "#1a1f2e",    # Secondary panels - Slightly lighter
    "bg_tertiary": "#242b3d",     # Cards and elements - Medium dark
    "bg_elevated": "#2d3548",     # Elevated elements - Lighter for depth
    
    # Accent colors - Smooth, softer blue gradient
    "accent_primary": "#60a5fa",  # Soft primary blue - Gentle and smooth
    "accent_hover": "#93c5fd",    # Lighter soft blue on hover
    "accent_pressed": "#3b82f6",  # Slightly deeper blue when pressed
    "accent_dim": "#1d4ed8",      # Dimmed accent - Deeper blue
    
    # Text colors - High contrast for readability
    "text_primary": "#e8eaed",    # Primary text - Soft white
    "text_secondary": "#9aa0a6",  # Secondary text - Muted gray
    "text_tertiary": "#70757a",   # Tertiary text - Dim gray
    "text_accent": "#8ab4f8",     # Accent text - Light blue
    
    # Success/Warning/Error colors - Smooth, softer tones
    "success": "#4ade80",         # Soft green - Success operations
    "success_dim": "#22c55e",     # Dimmed success
    "warning": "#fbbf24",         # Soft amber - Warnings
    "warning_dim": "#f59e0b",     # Dimmed warning
    "error": "#f87171",           # Soft red - Errors
    "error_dim": "#ef4444",       # Dimmed error
    
    # Impact badge colors - Smooth, softer, muted tones
    "impact_high": "#60a5fa",     # Soft blue - High impact
    "impact_medium": "#93c5fd",   # Light soft blue - Medium impact
    "impact_low": "#6b7280",      # Soft gray - Low impact
    
    # Special colors - Softer, more refined tones
    "recommended": "#4ade80",     # Soft green badge for recommended
    "privacy": "#a78bfa",         # Soft purple for privacy features
    "performance": "#fbbf24",     # Soft amber for performance
    "security": "#f87171",        # Soft red for security (warnings)
    
    # UI elements
    "border": "#3c4043",          # Border color - Subtle
    "border_hover": "#5f6368",    # Hover border - More visible
    "shadow": "#000000",          # Shadow color
    "overlay": "#00000080",       # Overlay background (50% opacity)
    
    # Tab/Button states - Softer, smoother colors
    "tab_active": "#60a5fa",      # Soft blue for active tab
    "tab_inactive": "#6b7280",    # Soft gray for inactive tab
    "button_hover": "#374151",    # Soft hover background
    "button_active": "#60a5fa",   # Soft blue for active state
    
    # Gradients (for use in code) - Softer gradients
    "gradient_header": ["#1a1f2e", "#0f1419"],  # Header gradient
    "gradient_card": ["#242b3d", "#1a1f2e"],    # Card gradient
    "gradient_button": ["#60a5fa", "#3b82f6"],  # Soft button gradient
}

# Font configuration
FONTS = {
    "heading_large": ("Segoe UI", 32, "bold"),
    "heading_medium": ("Segoe UI", 20, "bold"),
    "heading_small": ("Segoe UI", 16, "bold"),
    "body_large": ("Segoe UI", 14),
    "body_medium": ("Segoe UI", 12),
    "body_small": ("Segoe UI", 10),
    "mono": ("Consolas", 11),
}

# Spacing/sizing
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 12,
    "lg": 16,
    "xl": 24,
    "xxl": 32,
}

# Border radius for rounded corners
RADIUS = {
    "small": 4,
    "medium": 8,
    "large": 12,
    "xlarge": 16,
}

# Animation durations (milliseconds)
ANIMATION = {
    "fast": 150,
    "normal": 250,
    "slow": 350,
}
