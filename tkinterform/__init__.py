from tkinterform.checkbutton import Checkbutton
from tkinterform.combobox import Combobox
from tkinterform.form import Form
from tkinterform.hidden import Hidden
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

        self._set_up_bind()

    def _set_up_bind(self):
        self.bind("<<TkfSequenceUpdate>>", self.on_sequence_update)

    def _delete_self(self):
        index = self._at_index_in_sequence
        if index is not None:
            self.master.delete(index)

    def on_sequence_update(self, event):
        index = self._at_index_in_sequence

        title_text = "%s %s" % (self.description, (index + 1))

        if index is not None:
            self.entry_config("title", text=title_text)


def _test():
    root = tk.Tk()
    form = Form(root)
    text = "This is Tkinterform %s" % __version__
    form.add(ttk.Label, anchor="center", text=text)
    form.add(ttk.Label, text="Text")
    form.add(Text, name="text")
    form.add(Checkbutton, name="checkbutton", text="Checkbutton")
    form.add(ttk.Label, text="Sequence")
    form.add(
        ttk.Button,
        command=lambda: form.tkf_children.get("sequence").add(),
        text="Create element",
    )
    form.add(Sequence, form=_FormElement, name="sequence")
    form.add(ttk.Label, text="Combobox")
    form.add(Combobox, name="combobox")
    form.tkf_children.get("combobox").add_option("Option 1", 1)
    form.tkf_children.get("combobox").add_option("Option 2", 2)
    form.add(Hidden, name="hidden")
    form_values = {
        "text": "Hello, world!",
        "checkbutton": True,
        "sequence": [
            {"text": "I am an element from a sequence!"},
            {"text": "I am another element from a sequence!"},
        ],
        "hidden": "I am a hidden value...",
    }
    form.set_value(form_values)
    form.add(ttk.Button, command=lambda: print(form.get_value()), text="Print")
    form.add(ttk.Button, command=root.destroy, text="Quit")
    form.pack(fill="x", padx=8, pady=8)
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
