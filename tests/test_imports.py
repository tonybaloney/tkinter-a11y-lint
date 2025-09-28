"""Test file for different import styles."""

# Test 1: Standard import with alias
import tkinter as tk

root1 = tk.Tk()
button1 = tk.Button(root1)  # Should trigger C9001 and C9002

# Test 2: Direct import
from tkinter import Button, Entry, Label

button2 = Button(None)  # Should trigger C9001 and C9002
entry2 = Entry(None)  # Should trigger C9002
label2 = Label(None)  # Should trigger C9001

# Test 3: Import with different alias
import tkinter as tkinter_module

button3 = tkinter_module.Button(None)  # Should trigger C9001 and C9002

# Test 4: Proper accessibility (no issues)
good_button = tk.Button(root1, text="Submit", takefocus=True)
good_label = Label(None, text="Name:")
good_entry = Entry(None, takefocus=True)
