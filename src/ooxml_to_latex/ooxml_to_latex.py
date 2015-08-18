# coding: utf-8

from lxml import sax, etree


class XMLtoLatexParser(sax.ContentHandler):

    def __init__(self, math_symbols=None):
        sax.ContentHandler.__init__(self)
        self.math_symbols = math_symbols if math_symbols is not None else []
        self.result = ''
        self.insert_before = ''
        self.insert_after = ''
        self.text = ''
        self.previous_tag = ''
        self.spacing = ''
        self.tag_start_evaluator = {
            'begChr': self._parse_start_begchr,
            'endChr': self._parse_start_endchr,
            'chr': self._parse_attrs,
            'pos': self._parse_attrs,
            'sub': self._parse_start_sub,
            'sup': self._parse_start_sup,
            'f': self._parse_start_f,
            'e': self._parse_start_e,
            'm': self._parse_start_m,
            'mr': self._parse_start_mr,
            'limLow': self._parse_start_limlow,
            'rad': self._parse_start_rad,
            'deg': self._parse_start_deg,
            'den': self._parse_start_den
        }
        self.tag_end_evaluator = {
            'sub': self._parse_common_tag_close,
            'sup': self._parse_common_tag_close,
            'den': self._parse_common_tag_close,
            'num': self._parse_common_tag_close,
            'lim': self._parse_end_lim,
            'r': self._parse_end_r,
            'm': self._parse_end_m,
            'd': self._parse_end_d,
            'mr': self._parse_end_mr,
            'deg': self._parse_end_deg
        }

    def _find_symbols(self, text):
        for key, value in self.math_symbols.items():
            if isinstance(key, str):
                found = text == key.decode("utf-8")
            else:
                found = text == key
            if found:
                text = value + ' '
        return text

    @classmethod
    def parse(cls, xml_element_or_string, **parser_kwargs):
        xml_to_latex_parser = cls(**parser_kwargs)

        if isinstance(xml_element_or_string, basestring):
            element = etree.fromstring(xml_element_or_string)
        else:
            element = xml_element_or_string

        sax.saxify(element, xml_to_latex_parser)
        return xml_to_latex_parser.result

    @staticmethod
    def remove_invalid_tags(xml_string):
        return xml_string.replace('<sub />', '').replace('<sup />', '').replace('<deg />', '')

    def _parse_start_m(self, **kwargs):
        if self.insert_before:
            self.result += self.insert_before + '\\begin{matrix}'
            self.insert_before = ''
        else:
            self.result += '\\begin{matrix}'

    def _parse_start_begchr(self, **kwargs):
        attr = kwargs['attrs'].getValueByQName("ns00:val")
        if attr == '{':
            # escape {
            attr = '\\' + attr
        self.insert_before = '\\left ' + attr

    def _parse_start_endchr(self, **kwargs):
        attr = kwargs['attrs'].getValueByQName("ns00:val")
        if attr == '}':
            attr = '\\' + attr
        self.insert_after = '\\right ' + attr

    def _parse_attrs(self, **kwargs):
        self.result += self._find_symbols(
            kwargs['attrs'].getValueByQName("ns00:val"))

    def _parse_start_sub(self, **kwargs):
        self.result += '_{'

    def _parse_start_sup(self, **kwargs):
        self.result += '^{'

    def _parse_start_f(self, **kwargs):
        self.result += '\\frac{'

    def _parse_start_e(self, **kwargs):
        self.result += self.insert_before
        self.insert_before = ''

    def _parse_start_mr(self, **kwargs):
        self.spacing = "&"

    def _parse_start_limlow(self, **kwargs):
        self.result += '\\underset{'

    def _parse_start_rad(self, **kwargs):
        self.result += '\sqrt'

    def _parse_start_deg(self, **kwargs):
        self.result += '['

    def _parse_start_den(self, **kwargs):
        self.result += '{'

    def _parse_common_tag_close(self):
        self.result += '}'

    def _parse_end_lim(self):
        self.result += '}{lim}'

    def _parse_end_r(self):
        self.result += self.text
        self.text = ''

    def _parse_end_m(self):
        if self.result.endswith('\\\\'):
            string_list = list(self.result)
            self.result = ''.join(string_list[:-2])
        self.result += '\\end{matrix}'

    def _parse_end_d(self):
        self.result += self.insert_after
        self.insert_after = ''

    def _parse_end_mr(self):
        self.spacing = ''
        if self.result.endswith("&"):
            string_list = list(self.result)
            string_list[-1] = ''
            self.result = ''.join(string_list)
        self.result += '\\\\'

    def _parse_end_deg(self):
        self.result += ']'

    def startElementNS(self, name, tag, attrs):
        tag = name[1]
        function = self.tag_start_evaluator.get(tag)
        if callable(function):
            function(attrs=attrs)

    def endElementNS(self, name, tag):
        tag = name[1]
        function = self.tag_end_evaluator.get(tag, None)
        if callable(function):
            function()

    def characters(self, data):
        if data != 'lim':
            self.text += self._find_symbols(data)
            if self.spacing:
                self.text += self.spacing
