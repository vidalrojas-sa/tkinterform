import tkinter as tk
from tkinter import ttk
from .input import Input


class Text(Input, ttk.Entry):
    def __init__(self, master, id=None, observe=True, required=False, **kwargs):
        """
        Construct a `tkinterform.Text` widget with the parent MASTER.

        It should be registered via `tkinterform.Form.add()`.
        """
        self.entry_var = tk.StringVar()
        try:
            self.entry_var.trace_add("write", self.on_text_write)
        except AttributeError:
            # Fallback for Python<=3.6
            self.entry_var.trace("w", self.on_text_write)
        self.observe = observe
        self.required = required

        super(Text, self).__init__(
            id=id, master=master, textvariable=self.entry_var, **kwargs
        )

    def get(self):
        return ttk.Entry.get(self).strip()

    def is_valid(self):
        if self.required and not self.get():
            return False

        return True

    def on_text_write(self, *args):
        if self.observe:
            self.on_update(*args)

    def set(self, string):
        self.observe = False
        self.delete(0, tk.END)

        if string is not None and string != "":
            self.insert(0, string)

        self.observe = True
