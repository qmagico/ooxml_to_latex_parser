# coding: utf-8

import unittest

from ooxml_to_latex.ooxml_to_latex import OOXMLtoLatexParser
from ooxml_to_latex.latex_constants import SYMBOLS
from utils import read_xml

template_path = 'templates'


class OoXMLtoLatexTestCase(unittest.TestCase):

    def test_frac(self):
        xml_string = read_xml('frac.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('\\frac{2}{2}', parsed)

    def test_equiv(self):
        xml_string = read_xml('equiv.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\equiv 2', parsed)

    def test_approx(self):
        xml_string = read_xml('approx.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\\approx 1', parsed)

    def test_ast(self):
        xml_string = read_xml('ast.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('\\ast ', parsed)

    def test_bar(self):
        xml_string = read_xml('bar.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('\\left |1\\right |', parsed)

    def test_brackets(self):
        xml_string = read_xml('brackets.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('\\left [2\\right ]', parsed)

    def test_cap(self):
        xml_string = read_xml('cap.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\\cap 3', parsed)

    def test_cdot(self):
        xml_string = read_xml('cdot.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('4\\cdot 2', parsed)

    def test_circ(self):
        xml_string = read_xml('circ.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('\\circ ', parsed)

    def test_complex_set(self):
        xml_string = read_xml('complex_set.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('\mathbb{C} ', parsed)

    def test_cong(self):
        xml_string = read_xml('cong.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\\cong 2', parsed)

    def test_cup(self):
        xml_string = read_xml('cup.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\\cup 2', parsed)

    def test_curly_braces(self):
        xml_string = read_xml('curly_braces.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('\\left \\{2\\right \\}', parsed)

    def test_div(self):
        xml_string = read_xml('div.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\\div ', parsed)

    def test_empty_set(self):
        xml_string = read_xml('emptyset.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('\\emptyset ', parsed)

    def test_forall(self):
        xml_string = read_xml('forall.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('\\forall ', parsed)

    def test_ge(self):
        xml_string = read_xml('ge.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\\ge^ 1', parsed)

    def test_gg(self):
        xml_string = read_xml('gg.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('1\\gg 5', parsed)

    def test_in(self):
        xml_string = read_xml('in.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('\\in 2', parsed)

    def test_integers_set(self):
        xml_string = read_xml('intergers_set.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('\\mathbb{Z} ', parsed)

    def test_le(self):
        xml_string = read_xml('le.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('1\\le 4', parsed)

    def test_ll(self):
        xml_string = read_xml('ll.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('1\\ll 2', parsed)

    def test_nabla(self):
        xml_string = read_xml('nabla.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('4\\nabla 10', parsed)

    def test_naturals_set(self):
        xml_string = read_xml('naturals_set.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('\\mathbb{N} ', parsed)

    def test_ne(self):
        xml_string = read_xml('ne.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('3\\ne 2', parsed)

    def test_ni(self):
        xml_string = read_xml('ni.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\\ni 2', parsed)

    def test_notin(self):
        xml_string = read_xml('notin.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('3\\notin 1', parsed)

    def test_notsubset(self):
        xml_string = read_xml('notsubset.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\\not\\subset 2', parsed)

    def test_notsupset(self):
        xml_string = read_xml('notsupset.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\\not\\supset 2', parsed)

    def test_nsubseteq(self):
        xml_string = read_xml('nsubseteq.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\\nsubseteq 2', parsed)

    def test_nsupseteq(self):
        xml_string = read_xml('nsupseteq.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\\nsupseteq 2', parsed)

    def test_pm(self):
        xml_string = read_xml('pm.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('3\\pm 2', parsed)

    def test_propto(self):
        xml_string = read_xml('propto.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('5\\propto 10', parsed)

    def test_rational_set(self):
        xml_string = read_xml('rational_set.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('\\mathbb{Q} ', parsed)

    def test_real_set(self):
        xml_string = read_xml('real_set.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('\\mathbb{R} ', parsed)

    def test_sim(self):
        xml_string = read_xml('sim.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\\sim 5', parsed)

    def test_subset(self):
        xml_string = read_xml('subset.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\\subset 2', parsed)

    def test_subseteq(self):
        xml_string = read_xml('subseteq.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\\subseteq 2', parsed)

    def test_supset(self):
        xml_string = read_xml('supset.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\\supset 2', parsed)

    def test_supseteq(self):
        xml_string = read_xml('supseteq.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('2\\supseteq 2', parsed)

    def test_times(self):
        xml_string = read_xml('times.xml', template_path)
        parsed = OOXMLtoLatexParser.parse(xml_string, math_symbols=SYMBOLS)

        self.assertEquals('1\\cdot 2', parsed)

if __name__ == '__main__':
    unittest.main()
