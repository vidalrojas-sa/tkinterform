import tkinter as tk
from tkinter import ttk
from contextlib import contextmanager
from .input import Input


class Text(Input, ttk.Entry):
    def __init__(self, master, required=False, *args, **kwargs):
        """
        Construct a `tkinterform.Text` widget with the parent MASTER.
        """
        self._do_not_trace = False
        self.required = required
        self.text_var = tk.StringVar()

        try:
            self.text_var.trace_add("write", self.on_write)
        except AttributeError:
            # Fallback for Python<=3.6
            self.text_var.trace("w", self.on_write)

        super(Text, self).__init__(
            master, textvariable=self.text_var, *args, **kwargs
        )

    def get_value(self):
        return self.get().strip()

    def is_valid(self):
        if self.required and not self.get_value():
            return False

        return True

    def on_write(self, *args):
        if not self._do_not_trace:
            self.master.event_generate("<<TkfInputUpdate>>", when="tail")

    def set_value(self, string):
        with self._trace_stop():
            self.delete(0, tk.END)
            if string is not None and string != "":
                self.insert(0, string)

    @contextmanager
    def _trace_stop(self):
        self._do_not_trace = True
        try:
            yield
        finally:
            self._do_not_trace = False
