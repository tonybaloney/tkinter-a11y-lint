#!/usr/bin/env python3
"""
Test integration of WCAG contrast checker with tkinter accessibility linting.

This demonstrates how to use the contrast checker function in the context
of analyzing tkinter widgets for accessibility compliance.
"""

import tkinter as tk

from wcag_contrast_checker import check_wcag_contrast, get_contrast_grade


def analyze_widget_colors(widget: tk.Widget):
    """
    Analyze a tkinter widget's colors for WCAG compliance.

    Args:
        widget: The tkinter widget to analyze
        widget_name: Name of the widget for reporting
    """
    try:
        # Get foreground and background colors
        fg = widget.cget("fg") or widget.cget("foreground") or "#000000"
        bg = widget.cget("bg") or widget.cget("background") or "#FFFFFF"

        # Handle default system colors that might not be hex
        if not fg.startswith("#"):
            # For demo purposes, map common color names
            color_map = {
                "black": "#000000",
                "white": "#FFFFFF",
                "red": "#FF0000",
                "green": "#008000",
                "blue": "#0000FF",
                "gray": "#808080",
                "grey": "#808080",
                "SystemWindowText": "#000000",  # Common Windows default
                "SystemWindow": "#FFFFFF",  # Common Windows default
            }
            fg = color_map.get(fg.lower(), "#000000")

        if not bg.startswith("#"):
            bg = color_map.get(bg.lower(), "#FFFFFF")

        # Check contrast
        result = check_wcag_contrast(fg, bg, large_text=False, level="AA")
        grade = get_contrast_grade(result["contrast_ratio"], large_text=False)

        return result["contrast_ratio"], grade

    except tk.TclError as e:
        print(f"Could not analyze: {e}")
        return None
