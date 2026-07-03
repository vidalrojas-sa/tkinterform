class Widget(object):
    """
    Base class for Tkinterform widgets.
    """

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop("name", None)
        super(Widget, self).__init__(*args, **kwargs)
