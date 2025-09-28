# WCAG 2.1 Contrast Checker for Tkinter Accessibility

This Python module provides functions to check color contrast according to the **WCAG 2.1 Web Accessibility Guidelines**. It's perfect for integrating into your tkinter accessibility linter to ensure UI components meet accessibility standards.

## Features

- ✅ **WCAG 2.1 Compliant**: Uses the exact formulas from the official WCAG 2.1 specification
- ✅ **Level AA and AAA Support**: Checks both AA (minimum) and AAA (enhanced) conformance levels  
- ✅ **Large Text Handling**: Automatically adjusts requirements for large text (18pt+ or 14pt+ bold)
- ✅ **Flexible Input**: Accepts hex colors (#FFFFFF) or RGB tuples (255, 255, 255)
- ✅ **Detailed Results**: Returns comprehensive analysis with ratios, grades, and pass/fail status

## Requirements

Based on WCAG 2.1 Success Criterion 1.4.3 (Contrast Minimum):

| Text Size | Level AA | Level AAA |
|-----------|----------|-----------|
| Normal text | 4.5:1 | 7:1 |
| Large text* | 3:1 | 4.5:1 |

*Large text = 18pt+ (24px+) or 14pt+ (18.5px+) bold

## Quick Start

```python
from wcag_contrast_checker import check_wcag_contrast

# Check contrast between black text on white background
result = check_wcag_contrast('#000000', '#FFFFFF')
print(f"Contrast ratio: {result['contrast_ratio']}:1")
print(f"Passes AA: {result['passes_aa']}")  # True
print(f"Passes AAA: {result['passes_aaa']}")  # True

# Check poor contrast
result = check_wcag_contrast('#CCCCCC', '#FFFFFF')
print(f"Passes AA: {result['passes_aa']}")  # False - only 1.61:1 ratio
```

## Core Functions

### `check_wcag_contrast(foreground, background, large_text=False, level='AA')`

Main function to check if colors meet WCAG requirements.

**Parameters:**
- `foreground`: Foreground color (hex string or RGB tuple)
- `background`: Background color (hex string or RGB tuple)  
- `large_text`: True if text is large (18pt+ or 14pt+ bold)
- `level`: 'AA' or 'AAA' conformance level

**Returns:**
```python
{
    'contrast_ratio': 4.54,        # Calculated ratio
    'passes_aa': True,             # Meets Level AA
    'passes_aaa': False,           # Meets Level AAA  
    'required_ratio': 4.5,         # Required for this level
    'meets_requirement': True,     # Meets requested level
    'level_tested': 'AA',          # Level that was tested
    'text_size': 'normal'          # 'normal' or 'large'
}
```

### `calculate_contrast_ratio(color1, color2)`

Calculate the contrast ratio between two colors (1.0 to 21.0).

### `get_contrast_grade(contrast_ratio, large_text=False)`

Get a letter grade ('AAA', 'AA', or 'FAIL') for a contrast ratio.

## Integration with Your Tkinter Linter

Here's how to add contrast checking to your existing accessibility linter:

```python
from wcag_contrast_checker import check_wcag_contrast

def check_widget_contrast(widget):
    """Add this to your existing widget checking functions."""
    try:
        # Get widget colors
        fg = widget.cget('fg') or '#000000'  # Default to black
        bg = widget.cget('bg') or '#FFFFFF'  # Default to white
        
        # Check contrast
        result = check_wcag_contrast(fg, bg, large_text=False, level='AA')
        
        if not result['passes_aa']:
            return {
                'type': 'insufficient-color-contrast',
                'message': f'Insufficient contrast ({result["contrast_ratio"]}:1, '
                          f'requires {result["required_ratio"]}:1)',
                'severity': 'error',
                'wcag_guideline': '1.4.3'
            }
    except Exception as e:
        return {
            'type': 'contrast-check-error', 
            'message': f'Could not check contrast: {e}',
            'severity': 'warning'
        }
    
    return None  # No issues found
```

## Example Test Cases

```python
# Perfect contrast (21:1)
check_wcag_contrast('#000000', '#FFFFFF')  # Black on white -> AAA

# Good contrast (5.57:1)  
check_wcag_contrast('#FFFFFF', '#0066CC')  # White on blue -> AA

# Borderline contrast (4.54:1)
check_wcag_contrast('#767676', '#FFFFFF')  # Gray on white -> AA (just passes)

# Poor contrast (1.61:1)
check_wcag_contrast('#CCCCCC', '#FFFFFF')  # Light gray on white -> FAIL

# Large text exception (2.85:1)
check_wcag_contrast('#999999', '#FFFFFF', large_text=True)  # FAIL even for large
```

## Error Handling

The functions handle common issues gracefully:

- **Invalid hex colors**: Raises `ValueError` with descriptive message
- **System color names**: Use `normalize_color()` helper or extend color mapping
- **Missing colors**: Default to black text on white background
- **Widget errors**: Wrap in try/catch and report as warnings

## Adding to Your Plugin

To integrate with your existing `tkinter_a11y_lint` plugin:

1. **Import the checker:**
   ```python
   from wcag_contrast_checker import check_wcag_contrast
   ```

2. **Add to your checker class:**
   ```python
   def check_color_contrast(self, node):
       """New checker method for color contrast."""
       # Your implementation using the examples above
   ```

3. **Register the checker:**
   Add to your plugin's checker registration alongside `missing-text-attribute` and `missing-tab-index`.

## WCAG 2.1 Compliance

This implementation follows the exact WCAG 2.1 specification:

- **Relative Luminance Formula**: Uses the precise sRGB linearization from WCAG
- **Contrast Ratio Formula**: (L1 + 0.05) / (L2 + 0.05) where L1 > L2
- **Thresholds**: Exact values from Success Criteria 1.4.3 and 1.4.6
- **Large Text Definition**: 18pt/24px or 14pt/18.5px bold per WCAG

## Testing

Run the included test script to verify functionality:

```bash
python wcag_contrast_checker.py
python test_contrast_integration.py  
python example_linter_integration.py
```

This will show test results for various color combinations and demonstrate integration with tkinter widgets.

---

**Ready to improve accessibility!** 🎯 Your tkinter applications will now meet WCAG color contrast standards, making them usable by people with visual impairments and low vision.