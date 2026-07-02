from tkinter import ttk
from .input import Input
from .widget import Widget


class Form(Input, ttk.Frame):
    """
    A `tkinterform.Form` widget is a container, used to group
    `tkinterform.Input` or `tkinterform.Widget` widgets together.

    A form may contain `Input` or `Widget` instances. This leads to interesting
    behavior, since `Form` implements `Input`: a `Form` can also contain
    instances of itself.

    Forms automatically propagate values to all of its children, for
    example: `Form.get()` collects values from all child `Input` instances, and
    `Form.set()` distributes values to all child `Input` instances.
    """

    def __init__(self, master, id=None, name=None, **kwargs):
        """
        Construct a `tkinterform.Form` widget with the parent MASTER.
        """
        self.children_ = {}
        self.name = name

        super(Form, self).__init__(id=id, master=master, **kwargs)

    def _update_form(self):
        pass

    def add(self, widget, **kwargs):
        self.append(widget(self, **kwargs))

    def append(self, widget):
        widget.pack(fill="x")

        if isinstance(widget, Widget) and widget.id:
            self.children_[widget.id] = widget

    def get(self):
        return {
            id: wdgt.get()
            for id, wdgt in self.children_.items()
            if isinstance(wdgt, Input)
        }

    def has(self, id):
        return id in self.children_

    def is_valid(self):
        return all(
            wdgt.is_valid()
            for wdgt in self.children_.values()
            if isinstance(wdgt, Input)
        )

    def keys(self):
        """
        Returns a list of all keys contained in the Form instance.
        The keys are strings.
        """
        return list(self.children_)

    def set(self, dict_):
        for id, value in dict_.items():
            wdgt = self.children_.get(id)
            if wdgt and isinstance(wdgt, Input):
                wdgt.set(value)

    def set_id(self, id):
        self.id = id

    def values(self):
        return [
            wdgt.get()
            for wdgt in self.children_.values()
            if isinstance(wdgt, Input)
        ]
