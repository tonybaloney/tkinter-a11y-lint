"""Bad example - This file contains accessibility issues that will be caught by the plugin."""

import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# A1001: Button without text attribute - screen readers won't know what this button does
bad_button = tk.Button(root)

# A1001: Label without text - provides no information to users
empty_label = tk.Label(root)

# A1002: Entry without tab index - keyboard users can't navigate to this field
bad_entry = tk.Entry(root)

# A1001 & A1002: Checkbutton with both issues
bad_checkbutton = tk.Checkbutton(root)

# A1002: Text widget without proper focus management
bad_text = tk.Text(root)

# A1002: Listbox without tab order
bad_listbox = tk.Listbox(root)

# Frame is not checked as it's not an interactive or text-displaying widget
frame = tk.Frame(root)

root.mainloop()