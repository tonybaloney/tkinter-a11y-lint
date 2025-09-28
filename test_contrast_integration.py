#!/usr/bin/env python3
"""
Test integration of WCAG contrast checker with tkinter accessibility linting.

This demonstrates how to use the contrast checker function in the context
of analyzing tkinter widgets for accessibility compliance.
"""

import tkinter as tk

from wcag_contrast_checker import check_wcag_contrast, get_contrast_grade


def analyze_widget_colors(widget, widget_name="Widget"):
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

        print(f"\n{widget_name} Analysis:")
        print(f"  Foreground: {fg}")
        print(f"  Background: {bg}")
        print(f"  Contrast ratio: {result['contrast_ratio']}:1")
        print(f"  Grade: {grade}")
        print(f"  Passes WCAG AA: {result['passes_aa']}")
        print(
            f"  Recommendation: {'✓ Good' if result['passes_aa'] else '⚠ Improve contrast'}"
        )

        return result

    except tk.TclError as e:
        print(f"Could not analyze {widget_name}: {e}")
        return None


def demo_contrast_analysis():
    """Demonstrate contrast analysis on various tkinter widgets."""
    root = tk.Tk()
    root.title("WCAG Contrast Analysis Demo")

    print("WCAG 2.1 Contrast Analysis for Tkinter Widgets")
    print("=" * 50)

    # Create widgets with different color combinations
    widgets_to_test = [
        # Good contrast examples
        tk.Label(root, text="Good contrast", fg="#000000", bg="#FFFFFF"),
        tk.Button(root, text="Good button", fg="#FFFFFF", bg="#0066CC"),
        # Poor contrast examples
        tk.Label(root, text="Poor contrast", fg="#CCCCCC", bg="#FFFFFF"),
        tk.Button(root, text="Poor button", fg="#999999", bg="#AAAAAA"),
        # Borderline cases
        tk.Label(root, text="Borderline", fg="#767676", bg="#FFFFFF"),
    ]

    # Analyze each widget
    for i, widget in enumerate(widgets_to_test):
        analyze_widget_colors(widget, f"Widget {i + 1}")

    # Don't actually show the GUI, just destroy it
    root.destroy()


if __name__ == "__main__":
    demo_contrast_analysis()

    print("\n" + "=" * 50)
    print("Integration test complete!")
    print("\nTo use in your tkinter accessibility linter:")
    print("1. Import: from wcag_contrast_checker import check_wcag_contrast")
    print("2. Get widget colors using widget.cget('fg') and widget.cget('bg')")
    print("3. Call check_wcag_contrast(fg_color, bg_color) to get compliance info")
    print("4. Report violations with recommended improvements")
