# coding: utf-8

from lxml import sax, etree
import utils
from tag import Tag


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
        self.actual_tag_is_eqarr_child = False
        self.level = 0

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
            'den': self._parse_start_den,
            'd': self._parse_start_d,
            'eqArr': self._parse_start_eqarr,
        }
        self.tag_end_evaluator = {
            'lim': self._parse_end_lim,
            'limLow': self._parse_end_limlow,
            'sub': self._parse_common_tag_close,
            'sup': self._parse_common_tag_close,
            'den': self._parse_common_tag_close,
            'num': self._parse_common_tag_close,
            'rad': self._parse_common_tag_close,
            'r': self._parse_end_r,
            'm': self._parse_end_m,
            'd': self._parse_end_d,
            'mr': self._parse_end_mr,
            'deg': self._parse_end_deg,
            'naryPr': self._parse_end_naryPr,
            'eqArr': self._parse_end_eqarr,
#            'e': self._parse_end_e,
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

        parenthesis_weird_patterns = "<d><dPr><ctrlPr><rPr><rFonts></rFonts>"

        if parenthesis_weird_patterns in self.parsed_tags:
            self.parsed_tags = self.parsed_tags.replace(parenthesis_weird_patterns, "")
            return True
        return False

    @classmethod
    def _remove_self_closing_tags(cls, xml_string):
        return xml_string.replace("<m:deg/>", "").replace("<deg />", "")

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
        xml_string = OOXMLtoLatexParser._remove_self_closing_tags(xml_string)
        xml_to_latex_parser = cls(**parser_kwargs)

        if isinstance(xml_string, basestring):
            element = etree.fromstring(xml_string)
            sax.saxify(element, xml_to_latex_parser)
            return xml_to_latex_parser
        else:
            raise TypeError("xml string parameter must be str or unicode")


    @staticmethod
    def change_xml_double_open_tag_to_left_arrow(xml_string):
        return xml_string.replace(r"<<", "left<")

    def _parse_start_eqarr(self, **kwargs):
        self.actual_tag_is_eqarr_child = True
        self.insert_after = r'\\'
        latex = r'\begin{array}{l}'
        if self.insert_before:
            self.result += self.insert_before + latex
            self.insert_before = ''
        else:
            self.result += latex

    def _parse_end_eqarr(self, **kwargs):
        latex = r'\end{array}'
        if self.insert_after:
            self.result += latex + self.insert_after
            #self.insert_after = ''
        else:
            self.result += latex + r'\right .'
        self.actual_tag_is_eqarr_child = False

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
        attr = self._find_symbols(attr)
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
        attr = self._find_symbols(attr)
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

    def _parse_start_d(self, **kwargs):
        self.result += self.insert_before
        self.insert_before = ''

    def _parse_start_mr(self, **kwargs):
        """
        Matrix row
        http://www.datypic.com/sc/ooxml/e-m_mr-1.html
        """
        self.spacing = "&"

    def _parse_end_naryPr(self, **kwargs):
        """
        when the tag 'nary' doesn't have
        the 'chr' child tag, the value of the 'nary'
        is a integral
        """
        pattern = "<nary><naryPr><chr>"
        if pattern not in self.parsed_tags:
            self.result += r"\int"
        self.parsed_tags = self.parsed_tags.replace(pattern, '')



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
        self.insert_before = "{"

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

    def _parse_common_tag_close(self, **kwargs):
        self.result += '}'

    def _parse_start_lim(self, **kwargs):
        if not self.is_underset:
            self.result += '}_{'

    def _parse_end_lim(self, **kwargs):
        if self.is_underset:
            self.result += "{lim}"

    def _parse_end_r(self, **kwargs):
        self.result += self.text
        self.text = ''

    def _parse_end_m(self, **kwargs):
        if self.result.endswith('\\\\'):
            string_list = list(self.result)
            self.result = ''.join(string_list[:-2])
        self.result += '\\end{matrix}'

    def _parse_end_d(self, **kwargs):
        tag = kwargs.get("tag")

        if self.level == tag.level:
            self.result += tag.close_char
        #self.insert_after = ''

    def _parse_end_mr(self, **kwargs):
        self.spacing = ''
        if self.result.endswith("&"):
            string_list = list(self.result)
            string_list[-1] = ''
            self.result = ''.join(string_list)
        self.result += '\\\\'

    def _parse_end_deg(self, **kwargs):
        self.result += ']'

    def startElementNS(self, name, tag, attrs):
        self.level += 1
        if self.should_insert_parenthesis():
            self.insert_before = "\\left ("
            self.insert_after = "\\right )"

        tag = Tag(name[1], self.level, open_char=self.insert_before)
        function = self.tag_start_evaluator.get(tag.name)
        if callable(function):
            function(attrs=attrs)


        self.parsed_tags += unicode(tag)
        self.previous_tag = tag.name

    def endElementNS(self, name, tag):
        if self.level != 0:
            self.level -= 1

        tag = Tag(name[1], self.level, close_char=self.insert_after, is_open_tag=False)
        function = self.tag_end_evaluator.get(tag.name, None)
        if callable(function):
            function(tag=tag)
        self.parsed_tags += unicode(tag)

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
