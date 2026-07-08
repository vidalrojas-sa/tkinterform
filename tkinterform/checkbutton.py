import tkinter as tk
from tkinter import ttk
from contextlib import contextmanager
from .input import Input


class Checkbutton(Input, ttk.Checkbutton):
    def __init__(self, master, *args, **kwargs):
        """
        Construct a `tkinterform.Checkbutton` widget with the parent MASTER.
        """
        self._do_not_trace = False
        self.checkbutton_var = tk.BooleanVar()

        try:
            self.checkbutton_var.trace_add("write", self.on_toggle)
        except AttributeError:
            # Fallback for Python<=3.6
            self.checkbutton_var.trace("w", self.on_toggle)

        super(Checkbutton, self).__init__(
            master, variable=self.checkbutton_var, *args, **kwargs
        )

    def get_value(self):
        return self.checkbutton_var.get()

    def is_valid(self):
        return True

    def on_toggle(self, *args):
        if not self._do_not_trace:
            self.master.event_generate("<<TkfInputUpdate>>", when="tail")

    def set_value(self, value=None):
        with self._trace_stop():
            self.checkbutton_var.set(
                bool(value) if value is not None else False
            )

    @contextmanager
    def _trace_stop(self):
        self._do_not_trace = True
        try:
            yield
        finally:
            self._do_not_trace = False
