import tkinter as tk
from tkinter import ttk
from contextlib import contextmanager
from .input import Input


class Combobox(Input, ttk.Combobox):
    def __init__(self, master, required=False, *args, **kwargs):
        """
        Construct a `tkinterform.Combobox` widget with the parent MASTER.
        """
        self.default = None
        self._do_not_trace = False
        self.required = required
        self.text_var = tk.StringVar()
        self.values = {}

        try:
            self.text_var.trace_add("write", self.on_select)
        except AttributeError:
            # Fallback for Python<=3.6
            self.text_var.trace("w", self.on_select)

        super(Combobox, self).__init__(
            master,
            state="readonly",
            textvariable=self.text_var,
            *args,
            **kwargs
        )

    def add_option(self, name, value, default=False):
        if default or self.default is None:
            self.default = name

        self.values[name] = value
        self["values"] = self.keys()

        if default or not self.text_var.get():
            self.set_value(self.get_value())

    def delete_option(self, name):
        if self.default == name:
            self.default = self.keys()[0] if self.keys() else None

        del self.values[name]
        self["values"] = self.keys()

        if self.text_var.get() == name:
            self.set_value(None)

    def get_value(self):
        return self.values.get(self.text_var.get(), "")

    def get_name_at_value(self, value):
        for name, _value in self.values.items():
            if _value == value:
                return name
        return None

    def has(self, name):
        return name in self.values

    def is_valid(self):
        if self.required and not self.get_value():
            return False

        return True

    def keys(self):
        """
        Returns a list of all keys contained in the Form instance.
        The keys are strings.
        """
        return list(self.values)

    def on_select(self, *args):
        if not self._do_not_trace:
            self.master.event_generate("<<TkfInputUpdate>>", when="tail")

    def set_value(self, name):
        name = self.get_name_at_value(name)

        with self._trace_stop():
            if name is not None:
                self.set(name)
            else:
                self.set(self.default if self.default else "")

    @contextmanager
    def _trace_stop(self):
        self._do_not_trace = True
        try:
            yield
        finally:
            self._do_not_trace = False
