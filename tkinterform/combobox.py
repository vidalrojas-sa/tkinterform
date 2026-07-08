import tkinter as tk
from tkinter import ttk
from contextlib import contextmanager
from .input import Input


class Combobox(Input, ttk.Combobox):
    def __init__(self, master, required=False, *args, **kwargs):
        """
        Construct a `tkinterform.Combobox` widget with the parent MASTER.
        """
        self._do_not_trace = False
        self.required = required
        self.text_var = tk.StringVar()

        try:
            self.text_var.trace_add("write", self.on_select)
        except AttributeError:
            # Fallback for Python<=3.6
            self.text_var.trace("w", self.on_select)

        super(Combobox, self).__init__(
            master, readonly=True, textvariable=self.text_var, *args, **kwargs
        )

    @contextmanager
    def _trace_stop(self):
        self._do_not_trace = True
        try:
            yield
        finally:
            self._do_not_trace = False

    def get(self):
        return self.text_var.get().strip()

    def is_valid(self):
        if self.required and not self.get():
            return False

        return True

    def on_select(self, *args):
        if not self._do_not_trace:
            self.master.event_generate("<<TkfInputUpdate>>", when="tail")

    def set(self, string):
        with self._trace_stop():
            if string is not None and string != "":
                self.set(string)
