# coding: utf-8

from lxml import sax, etree
import utils


class OOXMLtoLatexParser(sax.ContentHandler):

    def __init__(self, math_symbols=None):
        sax.ContentHandler.__init__(self)
        self.math_symbols = math_symbols if math_symbols is not None else []
        self.result = ''
        self.insert_before = ''
        self.insert_after = ''
        self.text = ''
        self.previous_tag = ''
        self.spacing = ''
        self.parsed_tags = ''
        self.is_underset = False

        self.tag_start_evaluator = {
            'type': self._parse_start_type,
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
            'lim': self._parse_start_lim,
            'limLow': self._parse_start_limlow,
            'rad': self._parse_start_rad,
            'deg': self._parse_start_deg,
            'den': self._parse_start_den
        }
        self.tag_end_evaluator = {
            'lim': self._parse_end_lim,
            'limLow': self._parse_end_limlow,
            'sub': self._parse_common_tag_close,
            'sup': self._parse_common_tag_close,
            'den': self._parse_common_tag_close,
            'num': self._parse_common_tag_close,
            'r': self._parse_end_r,
            'm': self._parse_end_m,
            'd': self._parse_end_d,
            'mr': self._parse_end_mr,
            'deg': self._parse_end_deg
        }

    def _find_symbols(self, text):
        result = ''
        for char in text:
            for key, value in self.math_symbols.items():
                if isinstance(key, str):
                    found = char == key.decode("utf-8")
                else:
                    found = char == key
                if found:
                    char = value + ' '
            result += char
        return result

    def should_insert_parenthesis(self):
        "windows sucks"

        parenthesis_weird_pattern = "<e><d><dPr><ctrlPr><rPr><rFonts></rFonts><i></i></rPr></ctrlPr></dPr>"

        if parenthesis_weird_pattern in self.parsed_tags:
            self.parsed_tags = self.parsed_tags.replace(parenthesis_weird_pattern, "")
            return True
        return False

    @staticmethod
    def _build_tag(tag_name, close=False):
        """
        build a tag from his name
        """
        if close:
            return "</{0}>".format(tag_name)
        return "<{0}>".format(tag_name)

    @staticmethod
    def getattr(attr):
        try:
            result = attr.getValueByQName("ns00:val")
        except KeyError:
            result = attr.getValueByQName("val")
        return result

    @classmethod
    def parse(cls, xml_string, **parser_kwargs):
        """
        Instantiates an object OOXMLtoLatexParser
         and parse the string given by xml_string

        :param xml_string: An string containing the xml to be
            parsed
        :param parser_kwargs:
            OOXMLtoLatexParser kwargs:
             - math_symbols: list of math symbols
               default to latex_constants.SYMBOLS
        """

        xml_string = OOXMLtoLatexParser.change_xml_double_open_tag_to_left_arrow(xml_string)
        xml_to_latex_parser = cls(**parser_kwargs)

        if isinstance(xml_string, basestring):
            element = etree.fromstring(xml_string)
        else:
            raise TypeError("xml string parameter must be str or unicode")

        sax.saxify(element, xml_to_latex_parser)
        return xml_to_latex_parser

    @staticmethod
    def change_xml_double_open_tag_to_left_arrow(xml_string):
        return xml_string.replace(r"<<", "left<")


    def _parse_start_m(self, **kwargs):
        """
        matrix: http://www.datypic.com/sc/ooxml/e-m_m-1.html
        """
        if self.insert_before:
            self.result += self.insert_before + '\\begin{matrix}'
            self.insert_before = ''
        else:
            self.result += '\\begin{matrix}'

    def _parse_start_begchr(self, **kwargs):
        """
        Delimiter beginning character
        http://www.datypic.com/sc/ooxml/e-m_begChr-1.html
        """
        attr = OOXMLtoLatexParser.getattr(kwargs['attrs'])
        if attr == '{':
            # escape {
            attr = '\\' + attr
        self.insert_before = '\\left ' + attr

    def _parse_start_endchr(self, **kwargs):
        """
        Delimiter Ending Character
        http://www.datypic.com/sc/ooxml/e-m_endChr-1.html
        """
        attr = OOXMLtoLatexParser.getattr(kwargs['attrs'])
        if attr == '}':
            attr = '\\' + attr
        self.insert_after = '\\right ' + attr

    def _parse_start_type(self, **kwargs):
        """
        when a fraction has properties, the fraction
        can be a binom. what a fuck
        """

        if self.previous_tag == "fPr":
            type = OOXMLtoLatexParser.getattr(kwargs['attrs'])
            if type == "noBar":
                self.result = self.result.replace('frac', 'binom', 1)

    def _parse_attrs(self, **kwargs):
        attr = OOXMLtoLatexParser.getattr(kwargs['attrs'])
        self.result += self._find_symbols(attr)

    def _parse_start_sub(self, **kwargs):
        """
        Lower limit (n-ary)
        http://www.datypic.com/sc/ooxml/e-m_sub-1.html
        """
        self.result += '_{'

    def _parse_start_sup(self, **kwargs):
        """
        Upper limit (n-ary)
        http://www.datypic.com/sc/ooxml/e-m_sup-1.html
        """
        self.result += '^{'

    def _parse_start_f(self, **kwargs):
        """
        Fraction Function
        http://www.datypic.com/sc/ooxml/e-m_f-1.html
        """
        self.result += '\\frac{'

    def _parse_start_e(self, **kwargs):
        """
        Base
        http://www.datypic.com/sc/ooxml/e-m_e-1.html
        """
        self.result += self.insert_before
        self.insert_before = ''

    def _parse_start_mr(self, **kwargs):
        """
        Matrix row
        http://www.datypic.com/sc/ooxml/e-m_mr-1.html
        """
        self.spacing = "&"

    def _parse_end_limlow(self, **kwargs):
        if not self.is_underset:
            self.result += "}"

    def _parse_start_limlow(self, **kwargs):
        """
        Lower-Limit Function
        http://www.datypic.com/sc/ooxml/e-m_limLow-1.html
        """
        self.result += '\\underbrace{'

    def _parse_start_rad(self, **kwargs):
        """
        Radical Function
        http://www.datypic.com/sc/ooxml/e-m_rad-1.html
        """
        self.result += '\sqrt'

    def _parse_start_deg(self, **kwargs):
        """
        Degree
        http://www.datypic.com/sc/ooxml/e-m_deg-1.html
        """
        self.result += '['

    def _parse_start_den(self, **kwargs):
        """
        Denominator
        http://www.datypic.com/sc/ooxml/e-m_den-1.html
        """
        self.result += '{'

    def _parse_common_tag_close(self):
        self.result += '}'

    def _parse_start_lim(self, **kwargs):
        if not self.is_underset:
            self.result += '}_{'

    def _parse_end_lim(self):
        if self.is_underset:
            self.result += "{lim}"

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
        if self.should_insert_parenthesis():
            self.insert_before = "\\left ("
            self.insert_after = "\\right )"

        tag_name = name[1]
        function = self.tag_start_evaluator.get(tag_name)
        if callable(function):
            function(attrs=attrs)

        self.parsed_tags += OOXMLtoLatexParser._build_tag(tag_name)
        self.previous_tag = tag_name

    def endElementNS(self, name, tag):
        tag_name = name[1]
        function = self.tag_end_evaluator.get(tag_name, None)
        if callable(function):
            function()
        self.parsed_tags += OOXMLtoLatexParser._build_tag(tag_name, close=True)

    def characters(self, data):

        if data == 'lim':
            self.is_underset = True
            self.result = utils.replace_last_substring(self.result, "\underbrace{", "\underset")
        else:
            if data.strip() == r"left":
                self.text = r"<"
            else:
                self.text += "{\ "
                self.text += self._find_symbols(data)
                self.text += "}"

            if self.spacing:
                self.text += self.spacing
