import tkinter as tk
from tkinter import scrolledtext
from contextlib import contextmanager
from .input import Input


class Textarea(Input, scrolledtext.ScrolledText):
    def __init__(
        self, master, columns=22, required=False, rows=2, *args, **kwargs
    ):
        """
        Construct a `tkinterform.TextArea` widget with the parent MASTER.
        """
        self._do_not_trace = False
        self.required = required

        kwargs.setdefault("borderwidth", 0)
        kwargs.setdefault("highlightbackground", "#CCCCCC")
        kwargs.setdefault("highlightcolor", "#4A90E2")
        kwargs.setdefault("highlightthickness", 1)

        super(Textarea, self).__init__(
            master, height=rows, width=columns, wrap=tk.WORD, *args, **kwargs
        )

        self.bind("<<Modified>>", self.on_write)

    def get_value(self):
        return self.get("1.0", "end-1c").strip()

    def is_valid(self):
        if self.required and not self.get_value():
            return False
        return True

    def on_write(self, event=None):
        if self.edit_modified() and not self._do_not_trace:
            self.master.event_generate("<<TkfInputUpdate>>", when="tail")

        self.edit_modified(False)

    def set_value(self, string):
        with self._trace_stop():
            self.delete("1.0", tk.END)
            if string is not None and string != "":
                self.insert("1.0", string)

    @contextmanager
    def _trace_stop(self):
        self._do_not_trace = True
        try:
            yield
        finally:
            self._do_not_trace = False
