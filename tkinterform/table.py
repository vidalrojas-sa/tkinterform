import tkinter as tk
from tkinter import font
from tkinter import ttk
from .input import Input


class TableContextMenu(tk.Menu):
    pass


class TableInput(tk.Entry):
    def __init__(self, master, column, iid, minimum_width, text, **kwargs):
        self.column = column
        self.iid = iid
        self.master = master
        self.minimum_width = minimum_width

        super(TableInput, self).__init__(master, **kwargs)

        self.font = font.Font(font=ttk.Style().lookup("Treeview", "font"))

        self.configure(font=self.font)
        self.insert(0, text)
        self["exportselection"] = False

    def _calculate_width(self):
        return max(self.font.measure(self.get()) + 12, self.minimum_width)

    def place_at(self, x, y, h):
        self.x = x
        self.y = y
        self.h = h
        self.place(x=x, y=y, width=self._calculate_width(), height=h)

        self.focus_set()
        self.selection_range(0, "end")

        self._set_up_bind()

    def on_key_release(self, event):
        if not self.winfo_exists():
            return

        self.place(
            x=self.x, y=self.y, width=self._calculate_width(), height=self.h
        )

    def on_return(self, event):
        if not self.winfo_exists():
            return

        values = list(self.master.item(self.iid, "values"))
        values[self.column] = self.get().strip()

        self.master.master.update_row(self.iid, values=tuple(values))

        self.destroy()

    def _set_up_bind(self):
        self.bind("<Escape>", lambda event: self.destroy())
        self.bind("<FocusOut>", lambda event: self.destroy())
        self.bind("<KeyRelease>", self.on_key_release)
        self.bind("<Return>", self.on_return)


class Table(Input, ttk.Frame):
    def __init__(
        self,
        master,
        columns,
        content_editable=True,
        inline_editable=True,
        height=5,
        zebra_striped=True,
        zebra_stripe_color="#f6f6f6",
        **kwargs
    ):
        self.columns = columns
        self.content_editable = content_editable
        self.inline_editable = inline_editable if content_editable else False
        self.zebra_striped = zebra_striped

        super(Table, self).__init__(master, **kwargs)

        self.tree_view = ttk.Treeview(
            self, columns=columns, height=height, show="headings"
        )
        self.tree_view.pack(side="left")
        self.tree_view_scroll_bar = ttk.Scrollbar(
            self, orient="vertical", command=self._on_scroll_bar_scroll
        )
        self.tree_view_scroll_bar.pack(fill="y", side="left")
        self.tree_view.configure(yscrollcommand=self._on_mousewheel_scroll)

        self.tree_view.tag_configure("evenrow", background="white")
        self.tree_view.tag_configure("oddrow", background=zebra_stripe_color)

        if inline_editable:
            self.tree_view.bind("<Double-1>", self._on_double_click)

    def add_heading(self, column, text):
        self.tree_view.heading(column=column, text=text)

    def clear(self):
        self.tree_view.delete(*self.tree_view.get_children())

    def column_config(self, name, **kwargs):
        self.tree_view.column(name, **kwargs)

    def _destroy_input_pop_up(self):
        if (
            getattr(self, "input_pop_up", None)
            and self.input_pop_up.winfo_exists()
        ):
            self.input_pop_up.destroy()

    def get_value(self):
        result = []

        for row_id in self.tree_view.get_children():
            row = self.tree_view.item(row_id)
            row_values = row["values"]

            row_dictionary = {}

            for index, _ in enumerate(self.columns):
                row_value = row_values[index] if index < len(row_values) else ""
                row_dictionary[self.columns[index]] = row_value

            result.append(row_dictionary)

        return result

    def insert_row(self, dict_):
        table_length = len(self.tree_view.get_children())
        values = []

        for column in self.columns:
            values.append(dict_[column] if column in dict_ else "")

        tag = "evenrow" if table_length % 2 == 0 else "oddrow"

        self.tree_view.insert(
            "",
            "end",
            values=tuple(values),
            tags=(tag,) if self.zebra_striped else (),
        )
        self.master.event_generate("<<TkfInputUpdate>>", when="tail")

    def is_valid(self):
        return super().is_valid()

    def _on_double_click(self, event):
        self._destroy_input_pop_up()

        column_id = self.tree_view.identify_column(event.x)
        iid = self.tree_view.identify_row(event.y)
        bounding_box = self.tree_view.bbox(iid, column_id)

        if not (iid and column_id and bounding_box):
            return

        column_name = self.tree_view.column(column_id, "id")
        if column_name not in self.columns:
            return

        column_index = self.columns.index(column_name)
        values = self.tree_view.item(iid, "values") or []
        text = values[column_index] if column_index < len(values) else ""

        x, y, w, h = bounding_box
        self.input_pop_up = TableInput(
            self.tree_view, column_index, iid, text=text, minimum_width=w
        )
        self.input_pop_up.place_at(x, y, h)

    def _on_mousewheel_scroll(self, *args):
        self._destroy_input_pop_up()
        self.tree_view_scroll_bar.set(*args)

    def _on_scroll_bar_scroll(self, *args):
        self._destroy_input_pop_up()
        self.tree_view.yview(*args)

    def remove_row(self, id):
        self.tree_view.delete(id)
        self.master.event_generate("<<TkfInputUpdate>>", when="tail")

    def set_value(self, list_):
        self.clear()

        if not list_:
            return

        for row in list_:
            if isinstance(row, dict):
                self.insert_row(row)

    def update_row(self, id, values):
        self.tree_view.item(id, values=tuple(values))
        self.master.event_generate("<<TkfInputUpdate>>", when="tail")
