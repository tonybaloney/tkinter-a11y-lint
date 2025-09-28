"""Good example - This file shows proper accessibility practices."""

import tkinter as tk

root = tk.Tk()
root.title("Accessible Tkinter Application")

# Good: Button with clear text
good_button = tk.Button(root, text="Submit Form", takefocus=True)

# Good: Label with descriptive text
description_label = tk.Label(root, text="Enter your name below:")

# Good: Entry with proper focus management
name_entry = tk.Entry(root, takefocus=True)

# Good: Checkbutton with text and focus
agree_checkbox = tk.Checkbutton(
    root, text="I agree to the terms and conditions", takefocus=True
)

# Good: Text widget with proper focus
comments_text = tk.Text(root, takefocus=True)

# Good: Listbox with tab order
options_listbox = tk.Listbox(root, takefocus=True)
options_listbox.insert(0, "Option 1")
options_listbox.insert(1, "Option 2")

# Good: Radiobuttons with proper accessibility
radio_var = tk.StringVar()
radio1 = tk.Radiobutton(
    root, text="Yes", variable=radio_var, value="yes", takefocus=True
)
radio2 = tk.Radiobutton(root, text="No", variable=radio_var, value="no", takefocus=True)

# Layout widgets (Frame, etc.) don't need accessibility attributes
main_frame = tk.Frame(root)

# Pack everything
description_label.pack(pady=5)
name_entry.pack(pady=5)
agree_checkbox.pack(pady=5)
comments_text.pack(pady=5)
options_listbox.pack(pady=5)
radio1.pack(pady=2)
radio2.pack(pady=2)
good_button.pack(pady=10)

root.mainloop()
