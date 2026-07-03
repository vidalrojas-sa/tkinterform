from tkinter import ttk
from .input import Input


class Sequence(Input, ttk.Frame):
    def __init__(self, master, of_form, id=None, **kwargs):
        """
        Construct a `tkinterform.Sequence` widget with the parent MASTER.

        It should be registered via `tkinterform.Form.add()`.
        """
        self.children_ = []
        self.form_cls = of_form

        super(Sequence, self).__init__(id=id, master=master, **kwargs)

    def add(self, update_index=True):
        form = self.form_cls(self)
        self.append(form)

        if update_index:
            self._update_index()

        return form

    def append(self, form):
        form.pack(fill="x")
        self.children_.append(form)

    def clear(self):
        for form in self.children_:
            form.destroy()

        del self.children_[:]

    def delete(self, index, update_index=True):
        if 0 <= index < len(self.children_):
            self.children_.pop(index).destroy()

            if update_index:
                self._update_index()

    def get(self):
        return [form.get() for form in self.children_]

    def is_valid(self):
        return all(form.is_valid() for form in self.children_)

    def set(self, list_):
        self.clear()

        for element in list_:
            form = self.add(update_index=False)
            form.set(element)

        self._update_index()

    def _update_index(self):
        for idx, form in enumerate(self.children_):
            form.set_id(idx)
            form._update_form()
