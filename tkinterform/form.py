from tkinter import ttk
from .hidden import Hidden
from .input import Input
from .sequence import Sequence
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

    def add(self, widget_type, master=None, name=None, **kwargs):
        """Internal function."""
        master = self.tkf_children.get(master) if master else self
        widget = widget_type(master, **kwargs)

        if not isinstance(widget, Hidden):
            widget.pack(fill="x")

        if name is not None:
            if isinstance(widget, Widget):
                widget.tkf_name = name

            self.tkf_children[name] = widget

        return widget

    @property
    def _at_index_in_sequence(self):
        if isinstance(self.master, Sequence):
            try:
                return self.master.fieldsets.index(self)
            except ValueError:
                return None
        return None

    def entry_config(self, name, **kwargs):
        if not self.has(name):
            return

        widget = self.tkf_children.get(name)
        widget.config(**kwargs)

    def get_value(self, name=None):
        if name is None:
            return self._get_all()

        widget = self.tkf_children.get(name)

        return widget.get_value() if isinstance(widget, Input) else None

    def _get_all(self):
        return {
            name: widget.get_value()
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

    def set_value(self, dict_, name=None):
        if name is None:
            self._set_all(dict_)
        elif name in dict_:
            widget = self.tkf_children.get(name)

            if isinstance(widget, Input):
                widget.set_value(dict_[name])

    def _set_all(self, dict_):
        for name, value in dict_.items():
            widget = self.tkf_children.get(name)

            if isinstance(widget, Input):
                widget.set_value(value)

    def values(self):
        return [
            widget.get_value()
            for widget in self.tkf_children.values()
            if isinstance(widget, Input)
        ]
