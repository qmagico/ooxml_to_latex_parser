# coding: utf-8


class Tag(object):

    def __init__(self, name, level, open_char="", close_char="",
                 is_open_tag=True, is_self_closing=False):
        self.name = name
        self.open_char = open_char
        self.close_char = close_char
        self.is_open_tag = is_open_tag
        self.is_close_tag = not is_open_tag
        self.is_self_closing = is_self_closing
        self.level = level

    def __str__(self, *args):
        return self._build_tag()

    def __unicode__(self, *args):
        return self.__str__(*args)

    def _build_tag(self):
        if self.is_self_closing:
            return "<{0}/>".format(self.name)
        if self.is_close_tag:
            return "</{0}>".format(self.name)
        return "<{0}>".format(self.name)
