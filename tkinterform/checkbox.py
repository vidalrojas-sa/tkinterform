import tkinter as tk
from tkinter import ttk
from .input import Input


class Checkbutton(Input, ttk.Checkbutton):
    def __init__(self, master, *args, **kwargs):
        """
        Construct a `tkinterform.Checkbox` widget with the parent MASTER.
        """
        self._do_not_trace = False
        self.checkbutton_var = tk.BooleanVar()

        try:
            self.checkbutton_var.trace_add("write", self.on_toggle)
        except AttributeError:
            # Fallback for Python<=3.6
            self.checkbutton_var.trace("w", self.on_toggle)

        super().__init__(master, variable=self.checkbutton_var, *args, **kwargs)

    def get(self):
        return self.checkbutton_var.get()

    def is_valid(self):
        return True

    def on_toggle(self, *args):
        if not self._do_not_trace:
            self.master.event_generate("<<TkfInputUpdate>>", when="tail")

    def set(self, value):
        with self._trace_stop():
            if isinstance(value, bool):
                tk.BooleanVar.set(value)
