from tkinter import ttk
from .widget import Widget


class Label(Widget, ttk.Label):
    def __init__(self, master, id=None, **kwargs):
        super(Label, self).__init__(id=id, master=master, **kwargs)
