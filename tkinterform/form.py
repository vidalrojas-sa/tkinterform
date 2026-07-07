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

    def __init__(self, master, description=None, *args, **kwargs):
        """
        Construct a `tkinterform.Form` widget with the parent MASTER.
        """
        self.description = description
        self.tkf_children = {}

        super(Form, self).__init__(master, *args, **kwargs)

    def add(self, widget, master=None, name=None, **kwargs):
        target_master = master if master else self

        if isinstance(target_master, str) and self.has(master):
            target_master = self.tkf_children.get(master)

        self.append(widget(target_master, **kwargs), name)

    def append(self, widget, name=None):
        widget.pack(fill="x")

        if name is not None:
            if isinstance(widget, Widget):
                widget.tkf_name = name

            self.tkf_children[name] = widget

    @property
    def current_position(self):
        if hasattr(self.master, "fieldsets"):
            try:
                return self.master.fieldsets.index(self)
            except ValueError:
                return None
        return None

    def get(self):
        return {
            name: widget.get()
            for name, widget in self.tkf_children.items()
            if isinstance(widget, Input)
        }

    def has(self, name):
        return name in self.tkf_children

    def is_valid(self):
        return all(
            widget.is_valid()
            for widget in self.tkf_children.values()
            if isinstance(widget, Input)
        )

    def keys(self):
        """
        Returns a list of all keys contained in the Form instance.
        The keys are strings.
        """
        return list(self.tkf_children)

    def set(self, dict_):
        for key, value in dict_.items():
            widget = self.tkf_children.get(key)

            if widget and isinstance(widget, Input):
                widget.set(value)

    def values(self):
        return [
            widget.get()
            for widget in self.tkf_children.values()
            if isinstance(widget, Input)
        ]
