from tkinter import ttk
from .input import Input


class Sequence(Input, ttk.Frame):
    def __init__(self, master, of_form, *args, **kwargs):
        """
        Construct a `tkinterform.Sequence` widget with the parent MASTER.

        It should be registered via `tkinterform.Form.add()`.
        """
        self.form = of_form
        self.fieldsets = []

        super(Sequence, self).__init__(master, *args, **kwargs)

    def _refresh_children(self):
        for form in self.fieldsets:
            form.on_master_update()

    def add(self, refresh_children=True):
        form = self.form(self)
        self.append(form)

        if refresh_children:
            self._refresh_children()

        return form

    def append(self, form):
        form.pack(fill="x")
        self.fieldsets.append(form)

    def clear(self):
        for form in self.fieldsets:
            form.destroy()

        del self.fieldsets[:]

    def delete(self, index, refresh_children=True):
        if 0 <= index < len(self.fieldsets):
            self.fieldsets.pop(index).destroy()

            if refresh_children:
                self._refresh_children()

    def get(self):
        return [form.get() for form in self.fieldsets]

    def is_valid(self):
        return all(form.is_valid() for form in self.fieldsets)

    def set(self, list_):
        self.clear()

        for element in list_:
            self.add(refresh_children=False).set(element)

        self._refresh_children()
