class Widget(object):
    """
    Base class for Tkinterform widgets.
    """

    def __init__(self, *args, tkf_name=None, **kwargs):
        self.tkf_name = tkf_name
        super(Widget, self).__init__(*args, **kwargs)
