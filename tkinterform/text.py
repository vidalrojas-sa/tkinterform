import tkinter as tk
from tkinter import ttk
from contextlib import contextmanager
from .input import Input


class Text(Input, ttk.Entry):
    def __init__(self, master, observe=True, required=False, *args, **kwargs):
        """
        Construct a `tkinterform.Text` widget with the parent MASTER.

        It should be registered via `tkinterform.Form.add()`.
        """
        self._stop_observe = False
        self.observe = observe
        self.required = required
        self.text_var = tk.StringVar()

        try:
            self.text_var.trace_add("write", self.on_text_write)
        except AttributeError:
            # Fallback for Python<=3.6
            self.text_var.trace("w", self.on_text_write)

        super(Text, self).__init__(
            master=master, textvariable=self.text_var, *args, **kwargs
        )

    @contextmanager
    def _stop_observer(self):
        self._stop_observe = True
        try:
            yield
        finally:
            self._stop_observe = False

    def get(self):
        return ttk.Entry.get(self).strip()

    def is_valid(self):
        if self.required and not self.get():
            return False

        return True

    def on_text_write(self, *args):
        if self.observe and not self._stop_observe:
            self.on_update(*args)

    def set(self, string):
        with self._stop_observer():
            self.delete(0, tk.END)
            if string is not None and string != "":
                self.insert(0, string)
