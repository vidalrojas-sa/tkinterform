class Widget(object):
    """
    Base class for Tkinterform widgets.
    """

    def __init__(self, id=None, *args, **kwargs):
        self.id = id

        super(Widget, self).__init__(*args, **kwargs)
