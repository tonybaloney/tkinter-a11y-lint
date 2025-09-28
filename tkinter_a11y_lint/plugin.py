"""Main pylint plugin module for tkinter accessibility checks."""

from pylint.checkers import BaseChecker
import astroid


class TkinterA11yChecker(BaseChecker):
    """Checker for tkinter accessibility issues."""

    name = "tkinter-a11y"
    priority = -1
    msgs = {
        "C9001": (
            "UI element '%s' should have text attribute for accessibility",
            "missing-text-attribute",
            "UI elements should have text attributes to be accessible to "
            "screen readers",
        ),
        "C9002": (
            "Interactive UI control '%s' should have tab index assignment",
            "missing-tab-index",
            "Interactive controls should have proper tab order for keyboard navigation",
        ),
    }

    # Tkinter widgets that should have text attributes
    TEXT_REQUIRED_WIDGETS = {
        "Button",
        "Label",
        "Checkbutton",
        "Radiobutton",
        "Menubutton",
    }

    # Interactive widgets that should have tab index
    TAB_INDEX_WIDGETS = {
        "Button",
        "Entry",
        "Text",
        "Listbox",
        "Scrollbar",
        "Scale",
        "Checkbutton",
        "Radiobutton",
        "Menubutton",
        "Canvas",
    }

    def __init__(self, linter=None):
        super().__init__(linter)
        self.tkinter_imports = set()

    def visit_importfrom(self, node: astroid.ImportFrom) -> None:
        """Track tkinter imports."""
        if node.modname == "tkinter":
            for name, alias in node.names:
                self.tkinter_imports.add(alias or name)

    def visit_import(self, node: astroid.Import) -> None:
        """Track tkinter imports."""
        for name, alias in node.names:
            if name == "tkinter":
                self.tkinter_imports.add(alias or "tkinter")

    def visit_call(self, node: astroid.Call) -> None:
        """Check tkinter widget instantiation for accessibility issues."""
        if not self._is_tkinter_widget_call(node):
            return

        widget_name = self._get_widget_name(node)
        if not widget_name:
            return

        # Check for missing text attribute
        if widget_name in self.TEXT_REQUIRED_WIDGETS:
            if not self._has_text_attribute(node):
                self.add_message(
                    "missing-text-attribute", node=node, args=(widget_name,)
                )

        # Check for missing tab index
        if widget_name in self.TAB_INDEX_WIDGETS:
            if not self._has_tab_index(node):
                self.add_message("missing-tab-index", node=node, args=(widget_name,))

    def visit_assign(self, node: astroid.Assign) -> None:
        """Check for configure() calls that might add missing attributes."""
        # This will be enhanced to track configure() calls
        pass

    def _is_tkinter_widget_call(self, node: astroid.Call) -> bool:
        """Check if the call is for a tkinter widget."""
        if isinstance(node.func, astroid.Attribute):
            # Handle cases like tk.Button()
            if hasattr(node.func, "expr") and isinstance(node.func.expr, astroid.Name):
                return node.func.expr.name in self.tkinter_imports
        elif isinstance(node.func, astroid.Name):
            # Handle direct imports like Button()
            return node.func.name in self.tkinter_imports
        return False

    def _get_widget_name(self, node: astroid.Call) -> str:
        """Extract the widget name from the call."""
        if isinstance(node.func, astroid.Attribute):
            return node.func.attrname
        elif isinstance(node.func, astroid.Name):
            return node.func.name
        return ""

    def _has_text_attribute(self, node: astroid.Call) -> bool:
        """Check if the widget has a text-related attribute."""
        text_attrs = {"text", "title", "label"}

        if node.keywords:
            for keyword in node.keywords:
                if keyword.arg in text_attrs:
                    return True
        return False

    def _has_tab_index(self, node: astroid.Call) -> bool:
        """Check if the widget has tab index related attributes."""
        tab_attrs = {"takefocus", "tabindex"}

        if node.keywords:
            for keyword in node.keywords:
                if keyword.arg in tab_attrs:
                    return True
        return False


def register(linter) -> None:
    """Register the checker with pylint."""
    linter.register_checker(TkinterA11yChecker(linter))
