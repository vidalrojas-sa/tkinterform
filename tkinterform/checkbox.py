import tkinter as tk
from tkinter import ttk
from .input import Input


class Checkbox(Input, ttk.Checkbutton):
    def __init__(self, master, *args, **kwargs):
        """
        Construct a `tkinterform.Checkbox` widget with the parent MASTER.
        """
        self._do_not_trace = False
        self.checkbox_var = tk.BooleanVar()

        super().__init__(master, variable=self.checkbox_var, *args, **kwargs)

    def get(self):
        return self.checkbox_var.get()

    def is_valid(self):
        return True

    def set(self, value):
        if isinstance(value, bool):
            tk.BooleanVar.set(value)
