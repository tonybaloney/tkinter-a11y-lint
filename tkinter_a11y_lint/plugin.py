"""Main pylint plugin module for tkinter accessibility checks."""

import astroid
from pylint.checkers import BaseChecker


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
        "C9003": (
            "Top-level window should have a descriptive title",
            "missing-window-title",
            "Windows should have titles that describe their purpose for screen readers",
        ),
        "C9004": (
            "Button '%s' should have keyboard accelerator for accessibility",
            "missing-keyboard-accelerator",
            "Important buttons should have keyboard shortcuts (Alt+key) "
            "for accessibility",
        ),
        "C9005": (
            "Label '%s' with mnemonic should have underline parameter",
            "missing-mnemonic-underline",
            "Labels with '&' mnemonic should specify underline parameter",
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

    # Top-level window widgets
    WINDOW_WIDGETS = {"Tk", "Toplevel"}

    # Widgets that commonly use keyboard accelerators
    ACCELERATOR_WIDGETS = {"Button", "Menubutton"}

    def __init__(self, linter=None):
        super().__init__(linter)
        self.tkinter_imports = set()
        self.created_windows = set()  # Track window variables
        self.titled_windows = set()  # Track windows with titles set

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

        self._check_text_attribute(node, widget_name)
        self._check_tab_index(node, widget_name)
        self._check_keyboard_accelerator(node, widget_name)
        self._check_window_title(node, widget_name)
        self._check_mnemonic_underline(node, widget_name)

    def _check_text_attribute(self, node: astroid.Call, widget_name: str) -> None:
        """Check for missing text attribute."""
        if widget_name in self.TEXT_REQUIRED_WIDGETS:
            if not self._has_text_attribute(node):
                self.add_message(
                    "missing-text-attribute", node=node, args=(widget_name,)
                )

    def _check_tab_index(self, node: astroid.Call, widget_name: str) -> None:
        """Check for missing tab index."""
        if widget_name in self.TAB_INDEX_WIDGETS:
            if not self._has_tab_index(node):
                self.add_message("missing-tab-index", node=node, args=(widget_name,))

    def _check_keyboard_accelerator(self, node: astroid.Call, widget_name: str) -> None:
        """Check for missing keyboard accelerator on buttons."""
        if widget_name in self.ACCELERATOR_WIDGETS:
            if self._has_text_but_no_accelerator(node):
                self.add_message(
                    "missing-keyboard-accelerator", node=node, args=(widget_name,)
                )

    def _check_window_title(self, node: astroid.Call, widget_name: str) -> None:
        """Check for window creation without title."""
        if widget_name in self.WINDOW_WIDGETS:
            self.add_message("missing-window-title", node=node)

    def _check_mnemonic_underline(self, node: astroid.Call, widget_name: str) -> None:
        """Check for labels with mnemonic but no underline."""
        if widget_name == "Label":
            if self._has_mnemonic_but_no_underline(node):
                self.add_message(
                    "missing-mnemonic-underline", node=node, args=(widget_name,)
                )

    def visit_assign(self, node: astroid.Assign) -> None:
        """Track window creation and other assignments."""
        # Track window variable assignments
        if isinstance(node.value, astroid.Call) and self._is_tkinter_widget_call(
            node.value
        ):
            widget_name = self._get_widget_name(node.value)
            if widget_name in self.WINDOW_WIDGETS:
                # Store window variable name for title tracking
                if node.targets and isinstance(node.targets[0], astroid.AssignName):
                    window_var = node.targets[0].name
                    self.created_windows.add(window_var)

    def visit_attribute(self, node: astroid.Attribute) -> None:
        """Track method calls like .title() on windows."""
        # Check for .title() method calls on windows
        if (
            hasattr(node, "attrname")
            and node.attrname == "title"
            and hasattr(node, "expr")
            and isinstance(node.expr, astroid.Name)
        ):
            # Mark window as having title set
            window_var = node.expr.name
            if window_var in self.created_windows:
                self.titled_windows.add(window_var)

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

    def _has_text_but_no_accelerator(self, node: astroid.Call) -> bool:
        """Check if button has text but no keyboard accelerator."""
        has_text = False
        has_underline = False
        text_has_ampersand = False

        if node.keywords:
            for keyword in node.keywords:
                if keyword.arg == "text":
                    has_text = True
                    # Check if text contains '&' for mnemonic
                    if (
                        isinstance(keyword.value, astroid.Const)
                        and isinstance(keyword.value.value, str)
                        and "&" in keyword.value.value
                    ):
                        text_has_ampersand = True
                elif keyword.arg == "underline":
                    has_underline = True

        # Only flag buttons with text that could benefit from accelerators
        # but don't have proper mnemonic setup
        return has_text and not (text_has_ampersand and has_underline)

    def _has_mnemonic_but_no_underline(self, node: astroid.Call) -> bool:
        """Check if label has '&' mnemonic but no underline parameter."""
        has_mnemonic = False
        has_underline = False

        if node.keywords:
            for keyword in node.keywords:
                if keyword.arg == "text":
                    # Check if text contains '&' for mnemonic
                    if (
                        isinstance(keyword.value, astroid.Const)
                        and isinstance(keyword.value.value, str)
                        and "&" in keyword.value.value
                    ):
                        has_mnemonic = True
                elif keyword.arg == "underline":
                    has_underline = True

        return has_mnemonic and not has_underline


def register(linter) -> None:
    """Register the checker with pylint."""
    linter.register_checker(TkinterA11yChecker(linter))
