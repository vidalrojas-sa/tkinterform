from abc import ABCMeta, abstractmethod
from .widget import Widget


class Input(Widget, metaclass=ABCMeta):
    """
    Base class for `tkinterform.Input` widgets, used as a standard interface
    for `tkinterform.Input` widgets.
    """

    def __init__(self, *args, **kwargs):
        super(Input, self).__init__(*args, **kwargs)

    @abstractmethod
    def get_value(self):
        """Override method to get this `tkinterform.Input` value."""
        pass

    @abstractmethod
    def is_valid(self):
        """Override method to handle invalid behaviors."""
        pass

    @abstractmethod
    def set_value(self, value):
        """Override method to set this `tkinterform.Input` value."""
        pass
