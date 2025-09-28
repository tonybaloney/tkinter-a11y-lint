# Tkinter Accessibility Lint Plugin

A pylint plugin that inspects tkinter usage in Python to enforce accessibility best practices.

## Features

This plugin provides the following accessibility checks for tkinter applications:

- **UI elements should have text attributes** - Ensures that UI elements like buttons, labels, and entries have appropriate text content for screen readers
- **UI controls should have tab index assignment** - Verifies that interactive controls have proper tab order for keyboard navigation

## Installation

```bash
pip install tkinter-a11y-lint
```

Or install from source:

```bash
git clone https://github.com/yourusername/tkinter-a11y-lint.git
cd tkinter-a11y-lint
pip install -e .
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

## Development

### Setup Development Environment

```bash
git clone https://github.com/yourusername/tkinter-a11y-lint.git
cd tkinter-a11y-lint
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black tkinter_a11y_lint/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.