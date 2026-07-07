from tkinter import ttk
from .input import Input


class Sequence(Input, ttk.Frame):
    def __init__(self, master, form, form_padding=None, *args, **kwargs):
        """
        Construct a `tkinterform.Sequence` widget with the parent MASTER.
        """
        self.form = form
        self.form_padding = form_padding
        self.fieldsets = []

        super(Sequence, self).__init__(master, *args, **kwargs)

    def add(self, **kwargs):
        form = self.form(self, **kwargs)
        form.pack(fill="x", pady=self.form_padding)

        self.fieldsets.append(form)

        self._go_update_fieldsets()

        return form

    def clear(self):
        for form in self.fieldsets:
            form.destroy()

        del self.fieldsets[:]
        self.collapse()

    def collapse(self):
        self.config(width=1, height=1)

    def delete(self, index):
        self.fieldsets.pop(index).destroy()
        self._go_update_fieldsets()

        if not self.fieldsets:
            self.collapse()

    def get(self, index=None):
        if index is None:
            return [form.get() for form in self.fieldsets]

        return self.fieldsets[index].get()

    def _get_all(self):
        return [form.get() for form in self.fieldsets]

    def _go_update_fieldsets(self):
        for form in self.fieldsets:
            form.event_generate("<<TkfSequenceUpdate>>", when="tail")

    def is_valid(self):
        return all(form.is_valid() for form in self.fieldsets)

    def set(self, value, index=None):
        if index is None:
            self._set_all(value)
        else:
            self.fieldsets[index].set(value)

    def _set_all(self, values):
        self.clear()

        for value in values:
            self.add().set(value)

        self._go_update_fieldsets()
