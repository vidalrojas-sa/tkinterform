import tkinter as tk
from tkinter import font
from tkinter import ttk
from .input import Input


class TableInput(tk.Entry):
    def __init__(self, master, column, iid, min_width, text, **kwargs):
        super(TableInput, self).__init__(master, **kwargs)

        self.master = master
        self.min_width = min_width
        self.column = column
        self.iid = iid

        style_font = ttk.Style().lookup(
            self.master.cget("style") or "Treeview", "font"
        )

        if style_font:
            self.tk_font = font.Font(font=style_font)
        else:
            self.tk_font = font.nametofont("TkDefaultFont")

        self.configure(font=self.tk_font)
        self.insert(0, text)
        self["exportselection"] = False

    def place_at(self, x, y, h):
        self.current_x = x
        self.current_y = y
        w = max(self.tk_font.measure(self.get()) + 12, self.min_width)
        self.current_h = h
        self.place(x=x, y=y, width=w, height=h)

        self._initial_y = self.master.winfo_rooty()

        self.focus_set()
        self.selection_range(0, "end")
        self._set_up_bind()

        self._observe_on_y_change()

    def _observe_on_y_change(self):
        if not self.winfo_exists() or not self.master.winfo_exists():
            return

        current_y = self.master.winfo_rooty()
        if hasattr(self, "_initial_y") and current_y != self._initial_y:
            self.destroy()
            return

        self.after(64, self._observe_on_y_change)

    def _on_key_press(self, event):
        if not self.winfo_exists():
            return
        w = max(self.tk_font.measure(self.get()) + 12, self.min_width)
        self.place(
            x=self.current_x, y=self.current_y, width=w, height=self.current_h
        )

    def on_return(self, event):
        if not self.winfo_exists():
            return
        values = list(self.master.item(self.iid, "values"))
        values[self.column] = self.get()
        self.master.item(self.iid, values=tuple(values))
        self.destroy()

    def _set_up_bind(self):
        self.bind("<Escape>", lambda event: self.destroy())
        self.bind("<FocusOut>", lambda event: self.destroy())
        self.bind("<KeyRelease>", self._on_key_press)
        self.bind("<Return>", self.on_return)


class Table(Input, ttk.Treeview):
    def __init__(self, master, columns, **kwargs):
        self.columns = columns

        super(Table, self).__init__(
            master, columns=columns, show="headings", **kwargs
        )

        self.bind("<Double-1>", self.on_double_click)

    def add_heading(self, name, text):
        self.heading(name=name, text=text)

    def _break_column_resize(self, event):
        if self.identify_region(event.x, event.y) == "separator":
            return "break"

    def clear(self):
        self.delete(*self.get_children())

    def column_config(self, name, **kwargs):
        self.column(name, **kwargs)

    def get_value(self):
        return [
            dict(zip(self.columns, self.item(row_id)["values"]))
            for row_id in self.get_children()
        ]

    def insert_row(self, dict_):
        values = []

        for column in self.columns:
            values.append(dict_[column] if column in dict_ else "")

        self.insert("", "end", values=tuple(values))

    def is_valid(self):
        return super().is_valid()

    def on_double_click(self, event):
        if hasattr(self, "input_pop_up") and self.input_pop_up.winfo_exists():
            self.input_pop_up.destroy()

        iid = self.identify_row(event.y)
        column_id = self.identify_column(event.x)

        if not iid or not column_id or column_id == "#0":
            return

        column_name = self.column(column_id, "id")

        try:
            column = self.columns.index(column_name)
        except ValueError:
            return

        bbox = self.bbox(iid, column_id)
        if not bbox:
            return

        x, y, w, h = bbox
        row_values = self.item(iid, "values")
        cell_text = row_values[column] if column < len(row_values) else ""

        self.input_pop_up = TableInput(self, column, iid, w, cell_text)
        self.input_pop_up.place_at(x, y, h)

    def remove_row(self, id):
        self.delete(id)

    def set_value(self, list_):
        if not list_:
            return

        for row in list_:
            if isinstance(row, dict):
                self.insert_row(row)
