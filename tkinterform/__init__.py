from tkinterform.form import Form
from tkinterform.input import Input
from tkinterform.label import Label
from tkinterform.sequence import Sequence
from tkinterform.text import Text

__version__ = "0.1.0"

import tkinter as tk
from tkinter import ttk


class _FormElement(Form):
    def __init__(self, master, *args, **kwargs):
        super(_FormElement, self).__init__(master, *args, **kwargs)

        self.number = None

        self.add(
            Label,
            id="title",
            text=("%s %s" % (self.name, self.number)),
        )
        self.add(ttk.Button, command=self._delete_self, text="Delete")
        self.add(Label, text="Text")
        self.add(Text, id="text")

    def _delete_self(self):
        self.master.delete(self.id)

    def _update_form(self):
        self.number = self.id + 1 if isinstance(self.id, int) else None
        self.children_.get("title").config(
            text=("%s %s" % (self.name, self.number))
        )


def _test():
    root = tk.Tk()
    form = Form(root)
    text = "This is Tkinterform %s" % __version__
    form.add(ttk.Label, anchor="center", text=text)
    form.add(ttk.Label, text="Text")
    form.add(Text, id="text")
    form.add(ttk.Label, text="Sequence")
    form.add(
        ttk.Button,
        command=lambda: form.children_.get("sequence").add(),
        text="Create element",
    )
    form.add(
        Sequence,
        form_cls=_FormElement,
        form_name="Element",
        id="sequence",
    )
    form_values = {
        "text": "Hello, world!",
        "sequence": [
            {"text": "I am an element from a sequence!"},
            {"text": "I am another element from a sequence!"},
        ],
    }
    form.set(form_values)
    form.add(ttk.Button, command=lambda: print(form.get()), text="Print")
    form.add(ttk.Button, command=root.destroy, text="Quit")
    form.pack(fill="x", padx=8, pady=8)

    def _on_input_update(event):
        print("TkfInputUpdate event received")

    root.bind("<<TkfInputUpdate>>", _on_input_update)
    root.iconify()
    root.update()
    root.deiconify()
    root.mainloop()


import types

__all__ = [
    name
    for name, obj in globals().items()
    if not name.startswith("_")
    and not isinstance(obj, types.ModuleType)
    and name not in {"wantobjects"}
]

if __name__ == "__main__":
    _test()
