# Tkinter Accessibility Lint Plugin

A pylint plugin that inspects tkinter usage in Python to enforce accessibility best practices.

## Features

This plugin provides the following accessibility checks for tkinter applications:

- **UI elements should have text attributes** - Ensures that UI elements like buttons, labels, and entries have appropriate text content for screen readers
- **UI controls should have tab index assignment** - Verifies that interactive controls have proper tab order for keyboard navigation
- **Windows should have descriptive titles** - Ensures top-level windows have titles for screen readers
- **Buttons should have keyboard accelerators** - Important buttons should have Alt+key shortcuts for keyboard users
- **Labels with mnemonics should have underline** - Labels using '&' mnemonics should specify underline position

## Installation

```bash
pip install tkinter-a11y-lint
```

## Usage

### Command Line

Run pylint with the plugin enabled:

```bash
pylint --load-plugins=tkinter_a11y_lint.plugin your_tkinter_app.py
```

### Configuration File

Add to your `.pylintrc` file:

```ini
[MASTER]
load-plugins=tkinter_a11y_lint.plugin
```

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| C9001 | missing-text-attribute | UI element should have text attribute for accessibility |
| C9002 | missing-tab-index | Interactive UI control should have tab index assignment |
| C9003 | missing-window-title | Top-level window should have a descriptive title |
| C9004 | missing-keyboard-accelerator | Button should have keyboard accelerator for accessibility |
| C9005 | missing-mnemonic-underline | Label with mnemonic should have underline parameter |

## Examples

### Missing Text Attribute (C9001)

```python
import tkinter as tk

root = tk.Tk()
# Bad: Button without text
button = tk.Button(root)  # Will trigger C9001

# Good: Button with text
button = tk.Button(root, text="Click me")
```

### Missing Tab Index (C9002)

```python
import tkinter as tk

root = tk.Tk()
# Bad: Entry without tab index
entry = tk.Entry(root)  # Will trigger C9002

# Good: Entry with tab index
entry = tk.Entry(root)
entry.configure(takefocus=True)
# or
entry = tk.Entry(root, takefocus=True)
```

### Missing Window Title (C9003)

```python
import tkinter as tk

# Bad: Window without title
root = tk.Tk()  # Will trigger C9003

# Good: Window with descriptive title
root = tk.Tk()
root.title("My Application")
```

### Missing Keyboard Accelerator (C9004)

```python
import tkinter as tk

root = tk.Tk()
# Bad: Button without keyboard accelerator
button = tk.Button(root, text="Save")  # Will trigger C9004

# Good: Button with keyboard accelerator
button = tk.Button(root, text="&Save", underline=0)  # Alt+S
```

### Missing Mnemonic Underline (C9005)

```python
import tkinter as tk

root = tk.Tk()
# Bad: Label with mnemonic but no underline
label = tk.Label(root, text="&Name:")  # Will trigger C9005

# Good: Label with mnemonic and underline
label = tk.Label(root, text="&Name:", underline=0)  # Alt+N
```
