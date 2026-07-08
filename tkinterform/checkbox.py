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

        try:
            self.text_var.trace_add("write", self.on_toggle)
        except AttributeError:
            # Fallback for Python<=3.6
            self.text_var.trace("w", self.on_toggle)

        super().__init__(master, variable=self.checkbox_var, *args, **kwargs)

    def get(self):
        return self.checkbox_var.get()

    def is_valid(self):
        return True

    def on_toggle(self, *args):
        if not self._do_not_trace:
            self.master.event_generate("<<TkfInputUpdate>>", when="tail")

    def set(self, value):
        with self._trace_stop():
            if isinstance(value, bool):
                tk.BooleanVar.set(value)
