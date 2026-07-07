from tkinterform.form import Form
from tkinterform.input import Input
from tkinterform.sequence import Sequence
from tkinterform.text import Text

__version__ = "0.1.0"

import tkinter as tk
from tkinter import ttk


class _FormElement(Form):
    def __init__(self, master, *args, **kwargs):
        super(_FormElement, self).__init__(
            master, description="Element", *args, **kwargs
        )

        self.add(ttk.Label, name="title", text="")
        self.add(ttk.Button, command=self._delete_self, text="Delete")
        self.add(ttk.Label, text="Text")
        self.add(Text, name="text")

    def _delete_self(self):
        index = self.current_position
        if index is not None:
            self.master.delete(index)

    def on_master_update(self):
        index = self.current_position
        if index is not None:
            self.tkf_children.get("title").config(
                text="%s %s" % (self.description, (index + 1))
            )


def _test():
    root = tk.Tk()
    form = Form(root)
    text = "This is Tkinterform %s" % __version__
    form.add(ttk.Label, anchor="center", text=text)
    form.add(ttk.Label, text="Text")
    form.add(Text, name="text")
    form.add(ttk.Label, text="Sequence")
    form.add(
        ttk.Button,
        command=lambda: form.tkf_children.get("sequence").add(),
        text="Create element",
    )
    form.add(Sequence, of_form=_FormElement, name="sequence")
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
