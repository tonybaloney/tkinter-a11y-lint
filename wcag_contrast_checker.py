"""
WCAG 2.1 Contrast Luminance Checker

This module provides functions to check color contrast according to the Web Content
Accessibility Guidelines (WCAG) 2.1 standards.

Based on the WCAG 2.1 specification:
https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html

Requirements:
- Normal text: 4.5:1 contrast ratio (Level AA)
- Large text: 3:1 contrast ratio (Level AA)
- Enhanced contrast: 7:1 for normal text, 4.5:1 for large text (Level AAA)

Large text is defined as:
- 18pt (24px) and larger, or
- 14pt (18.5px) and larger if bold
"""

from typing import Tuple, Union


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Convert hex color to RGB values.

    Args:
        hex_color: Hex color string (e.g., '#FF0000' or 'FF0000')

    Returns:
        Tuple of (R, G, B) values (0-255)

    Raises:
        ValueError: If hex_color is not a valid hex color
    """
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")

    try:
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        raise ValueError(f"Invalid hex color: {hex_color}")


def calculate_relative_luminance(r: int, g: int, b: int) -> float:
    """
    Calculate the relative luminance of a color according to WCAG 2.1.

    The relative luminance is the relative brightness of any point in a colorspace,
    normalized to 0 for darkest black and 1 for lightest white.

    Formula from WCAG 2.1:
    L = 0.2126 * R + 0.7152 * G + 0.0722 * B

    Where R, G and B are defined as:
    - if RsRGB <= 0.04045 then R = RsRGB/12.92 else R = ((RsRGB+0.055)/1.055) ^ 2.4
    - if GsRGB <= 0.04045 then G = GsRGB/12.92 else G = ((GsRGB+0.055)/1.055) ^ 2.4
    - if BsRGB <= 0.04045 then B = BsRGB/12.92 else B = ((BsRGB+0.055)/1.055) ^ 2.4

    And RsRGB, GsRGB, and BsRGB are defined as:
    - RsRGB = R8bit/255
    - GsRGB = G8bit/255
    - BsRGB = B8bit/255

    Args:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)

    Returns:
        Relative luminance value (0.0-1.0)
    """

    def linearize_rgb_component(component: int) -> float:
        """Convert 8-bit RGB component to linear RGB value."""
        # Normalize to 0-1 range
        s_rgb = component / 255.0

        # Apply gamma correction
        if s_rgb <= 0.04045:
            return s_rgb / 12.92
        else:
            return pow((s_rgb + 0.055) / 1.055, 2.4)

    # Convert each RGB component to linear values
    linear_r = linearize_rgb_component(r)
    linear_g = linearize_rgb_component(g)
    linear_b = linearize_rgb_component(b)

    # Calculate relative luminance using WCAG formula
    return 0.2126 * linear_r + 0.7152 * linear_g + 0.0722 * linear_b


def calculate_contrast_ratio(
    color1: Union[str, Tuple[int, int, int]], color2: Union[str, Tuple[int, int, int]]
) -> float:
    """
    Calculate the contrast ratio between two colors according to WCAG 2.1.

    Formula: (L1 + 0.05) / (L2 + 0.05)
    Where L1 is the relative luminance of the lighter color and
    L2 is the relative luminance of the darker color.

    Args:
        color1: First color as hex string or RGB tuple
        color2: Second color as hex string or RGB tuple

    Returns:
        Contrast ratio (1.0 to 21.0)
    """
    # Convert colors to RGB if they're hex strings
    if isinstance(color1, str):
        color1 = hex_to_rgb(color1)
    if isinstance(color2, str):
        color2 = hex_to_rgb(color2)

    # Calculate relative luminance for each color
    lum1 = calculate_relative_luminance(*color1)
    lum2 = calculate_relative_luminance(*color2)

    # Ensure L1 is the lighter color (higher luminance)
    l1 = max(lum1, lum2)
    l2 = min(lum1, lum2)

    # Calculate contrast ratio
    return (l1 + 0.05) / (l2 + 0.05)


def check_wcag_contrast(
    foreground: Union[str, Tuple[int, int, int]],
    background: Union[str, Tuple[int, int, int]],
    large_text: bool = False,
    level: str = "AA",
) -> dict:
    """
    Check if colors meet WCAG contrast requirements.

    Args:
        foreground: Foreground color as hex string or RGB tuple
        background: Background color as hex string or RGB tuple
        large_text: True if text is large (18pt+ or 14pt+ bold)
        level: WCAG conformance level ('AA' or 'AAA')

    Returns:
        Dictionary with contrast analysis results:
        {
            'contrast_ratio': float,
            'passes_aa': bool,
            'passes_aaa': bool,
            'required_ratio': float,
            'meets_requirement': bool,
            'level_tested': str
        }
    """
    contrast_ratio = calculate_contrast_ratio(foreground, background)

    # WCAG 2.1 Requirements
    if large_text:
        aa_requirement = 3.0
        aaa_requirement = 4.5
    else:
        aa_requirement = 4.5
        aaa_requirement = 7.0

    passes_aa = contrast_ratio >= aa_requirement
    passes_aaa = contrast_ratio >= aaa_requirement

    if level.upper() == "AAA":
        required_ratio = aaa_requirement
        meets_requirement = passes_aaa
    else:  # Default to AA
        required_ratio = aa_requirement
        meets_requirement = passes_aa

    return {
        "contrast_ratio": round(contrast_ratio, 2),
        "passes_aa": passes_aa,
        "passes_aaa": passes_aaa,
        "required_ratio": required_ratio,
        "meets_requirement": meets_requirement,
        "level_tested": level.upper(),
        "text_size": "large" if large_text else "normal",
    }


def get_contrast_grade(contrast_ratio: float, large_text: bool = False) -> str:
    """
    Get a letter grade for the contrast ratio.

    Args:
        contrast_ratio: The calculated contrast ratio
        large_text: True if text is large

    Returns:
        Grade string ('AAA', 'AA', 'FAIL')
    """
    if large_text:
        if contrast_ratio >= 4.5:
            return "AAA"
        elif contrast_ratio >= 3.0:
            return "AA"
        else:
            return "FAIL"
    else:  # Normal text
        if contrast_ratio >= 7.0:
            return "AAA"
        elif contrast_ratio >= 4.5:
            return "AA"
        else:
            return "FAIL"
