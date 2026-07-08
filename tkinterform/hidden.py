from contextlib import contextmanager
from .input import Input


class Hidden(Input):
    def __init__(self, master, *args, **kwargs):
        """
        Construct a `tkinterform.Hidden` widget.
        """
        self.master = master
        self.value = None

        super(Hidden, self).__init__(*args, **kwargs)

    def get_value(self):
        return self.value

    def is_valid(self):
        return True

    def on_set(self, *args):
        self.master.event_generate("<<TkfInputUpdate>>", when="tail")

    def set_value(self, value, trace=False):
        self.value = value

        if trace:
            self.on_set()
