# coding: utf-8

import unittest
import os
from src.ooxml_to_latex import OOXMLtoLatexParser
from src.ooxml_to_latex import unicode_to_latex
from utils import read_xml

join_path = os.sep.join

fixtures_path = join_path(['fixtures'])
bug_fixes_path = join_path(['bug_fixes'])


class OoXMLtoLatexTestCase(unittest.TestCase):

    def test_sup_does_not_work(self):
        xml_string = read_xml("sup_does_not_work.xml", bug_fixes_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(xml_string, math_symbols=unicode_to_latex)

        self.assertMultiLineEqual(r'{\ l=}\left \{{\ S}_{{\ k}}\right \}_{{\ k=1}}^{{\ 5}}', ooxml_to_latex.result)

    def test_underset_is_not_a_limit(self):
        xml_string = read_xml("underset_is_not_limit.xml", bug_fixes_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(xml_string, math_symbols=unicode_to_latex)

        self.assertMultiLineEqual(r'\underbrace{{\ 7}^{{\ k}}}_{{\ n\ digitos}}<{\ 7}^{{\ k+1}}{\ =7}{\ 7}^'
                          r'{{\ k}}<\underbrace{{\ 10}{\ 7}^{{\ k}}}_{{\ n+1\ digitos}}', ooxml_to_latex.result)

    def test_bigcup_bug_fix(self):
        xml_string = read_xml("bigcup.xml", bug_fixes_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'\left (\bigcup  _{{\ i\in I}}^{}{\ S}_{{\ i}}\right )^{{\ c}}{\ =}\bigcap'
                          r'  _{{\ i\in I}}^{}\left ({\ S}_{{\ i}}^{{\ c}}\right )', ooxml_to_latex.result)

    def test_sum(self):
        xml_string = read_xml("sum.xml", bug_fixes_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r"\bigcap  _{}^{}{\ l=}\bigcap  _{{\ i\in I}}^{}{\ S}_{{\ i}}{\ =}"
                          r"\left \{{\ x/ x\in }{\ S}_{{\ i}}{\ para\ cada\ i\in I}\right \}", ooxml_to_latex.result)

    def test_fractions_without_bar_must_be_a_binom(self):
        xml_string = read_xml(
            "fractions_without_bar_must_be_a_binom.xml", bug_fixes_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertMultiLineEqual(r"\binom{{\ n}}{{\ 0}}", ooxml_to_latex.result)

    def test_insert_parenthesis_in_superscript(self):
        xml_string = read_xml(
            "insert_parenthesis_in_superscript.xml", bug_fixes_path)
        xml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r"\left ({\ a+b}\right )^{{\ n}}", xml_to_latex.result)

    def test_multiple_fractions(self):
        xml_string = read_xml("multiple_fractions.xml", bug_fixes_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertMultiLineEqual(r"{\ S}_{{\ n}}{\ :}\frac{{\ 1}}{\sqrt[]{\ 1}}{\ +}\frac{{\ 1}}"
                                  r"{\sqrt[]{\ 2}}{\ +\cdots  +}\frac{{\ 1}}{\sqrt[]"
                                  r"{\ n}}{\ \geq  }\sqrt[]{\ n}", ooxml_to_latex.result)

    def test_lim(self):
        xml_string = read_xml("lim.xml", fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(xml_string, math_symbols=unicode_to_latex)

        self.assertMultiLineEqual(r"\underset{\ n\rightarrow  \infty }{lim}\left "
                                  r"({\ 1+}\frac{{\ 1}}{{\ n}}\right )^{{\ n}}", ooxml_to_latex.result)

    def test_bigcap(self):
        xml_string = read_xml("bigcap.xml", fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r"\bigcap  _{}^{}", ooxml_to_latex.result)

    def test_dots(self):
        xml_string = read_xml("dots.xml", fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r"{\ \cdots  }", ooxml_to_latex.result)

    def test_multiples_symbols_in_text(self):
        xml_string = read_xml('multiples_symbols_in_text.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ \pi  n}', ooxml_to_latex.result)

    def test_cos(self):
        xml_string = read_xml('cos.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ cos}\left ({\ 2}\right )', ooxml_to_latex.result)

    def test_fat(self):
        xml_string = read_xml('fat.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 6}{\ !}', ooxml_to_latex.result)

    def test_sin(self):
        xml_string = read_xml('sin.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ sin}\left ({\ 10}\right )', ooxml_to_latex.result)

    def test_pow(self):
        xml_string = read_xml('pow.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ e}^{{\ 7}}', ooxml_to_latex.result)

    def test_log(self):
        xml_string = read_xml('log.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ log}\left ({\ 2}\right )', ooxml_to_latex.result)

    def test_exp(self):
        xml_string = read_xml('exp.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ exp}\left ({\ 4}\right )', ooxml_to_latex.result)

    def test_radius_of_the_circle(self):
        xml_string = read_xml('radius_of_the_circle.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ C}{\ =}{\ \pi  }{\ \cdot  }{\ d}{\ =}{\ 2}{\ \cdot  '
                          r'}{\ \pi  }{\ \cdot  }{\ r}', ooxml_to_latex.result)

    def test_emc2(self):
        xml_string = read_xml('emc2.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ E}{\ =}{\ mc}^{{\ 2}}', ooxml_to_latex.result)

    def test_function(self):
        xml_string = read_xml('function.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ f}\left ({\ x}\right ){\ =}\sum  _{{\ i}{\ =}{\ 0}}^{{\ '
                          r'\infty }}\frac{{\ f}^{\left ({\ i}\right )}\left ({\ 0}\right )}{{\ i}'
                          r'{\ !}}{\ x}^{{\ i}}', ooxml_to_latex.result)

    def test_ln(self):
        xml_string = read_xml('ln.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ ln}\left ({\ 10}\right )', ooxml_to_latex.result)

    def test_frac(self):
        xml_string = read_xml('frac.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'\frac{{\ 2}}{{\ 2}}', ooxml_to_latex.result)

    def test_equiv(self):
        xml_string = read_xml('equiv.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 2}{\ \equiv  }{\ 2}', ooxml_to_latex.result)

    def test_approx(self):
        xml_string = read_xml('approx.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals('{\\ 2}{\\ \\approx  }{\\ 1}', ooxml_to_latex.result)

    def test_ast(self):
        xml_string = read_xml('ast.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals('{\\ \\ast }', ooxml_to_latex.result)

    def test_bar(self):
        xml_string = read_xml('bar.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'\left |{\ 1}\right |', ooxml_to_latex.result)

    def test_brackets(self):
        xml_string = read_xml('brackets.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'\left [{\ 2}\right ]', ooxml_to_latex.result)

    def test_cap(self):
        xml_string = read_xml('cap.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 2}{\ \cap }{\ 3}', ooxml_to_latex.result)

    def test_cdot(self):
        xml_string = read_xml('cdot.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 4}{\ \cdot  }{\ 2}', ooxml_to_latex.result)

    def test_circ(self):
        xml_string = read_xml('circ.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ \circ  }', ooxml_to_latex.result)

    def test_complex_set(self):
        xml_string = read_xml('complex_set.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ \mathbb{C} }', ooxml_to_latex.result)

    def test_cong(self):
        xml_string = read_xml('simeq.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 2}{\ \simeq  }{\ 2}', ooxml_to_latex.result)

    def test_cup(self):
        xml_string = read_xml('cup.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 2}{\ \cup }{\ 2}', ooxml_to_latex.result)

    def test_curly_braces(self):
        xml_string = read_xml('curly_braces.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'\left \{{\ 2}\right \}', ooxml_to_latex.result)

    def test_div(self):
        xml_string = read_xml('div.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 2}{\ \div  }', ooxml_to_latex.result)

    def test_empty_set(self):
        xml_string = read_xml('emptyset.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ \emptyset }', ooxml_to_latex.result)

    def test_forall(self):
        xml_string = read_xml('forall.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ \forall  }', ooxml_to_latex.result)

    def test_ge(self):
        xml_string = read_xml('geq.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 2}{\ \geq  }{\ 1}', ooxml_to_latex.result)

    def test_gg(self):
        xml_string = read_xml('succcurlyeq.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 1}{\ \succcurlyeq  }{\ 5}', ooxml_to_latex.result)

    def test_in(self):
        xml_string = read_xml('in.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ \in }{\ 2}', ooxml_to_latex.result)

    def test_integers_set(self):
        xml_string = read_xml('intergers_set.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ \mathbb{Z} }', ooxml_to_latex.result)

    def test_le(self):
        xml_string = read_xml('leq.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 1}{\ \leq  }{\ 4}', ooxml_to_latex.result)

    def test_ll(self):
        xml_string = read_xml('preccurlyeq.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 1}{\ \preccurlyeq  }{\ 2}', ooxml_to_latex.result)

    def test_nabla(self):
        xml_string = read_xml('nabla.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 4}{\ \nabla  }{\ 10}', ooxml_to_latex.result)

    def test_naturals_set(self):
        xml_string = read_xml('naturals_set.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ \mathbb{N} }', ooxml_to_latex.result)

    def test_ne(self):
        xml_string = read_xml('ne.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 3}{\ \ne }{\ 2}', ooxml_to_latex.result)

    def test_ni(self):
        xml_string = read_xml('ni.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 2}{\ \ni  }{\ 2}', ooxml_to_latex.result)

    def test_notin(self):
        xml_string = read_xml('notin.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 3}{\ \notin }{\ 1}', ooxml_to_latex.result)

    def test_notsubset(self):
        xml_string = read_xml('notsubset.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 2}{\ \not\subset  }{\ 2}', ooxml_to_latex.result)

    def test_notsupset(self):
        xml_string = read_xml('notsupset.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 2}{\ \not\supset  }{\ 2}', ooxml_to_latex.result)

    def test_nsubseteq(self):
        xml_string = read_xml('nsubseteq.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 2}{\ \nsubseteq }{\ 2}', ooxml_to_latex.result)

    def test_nsupseteq(self):
        xml_string = read_xml('nsupseteq.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 2}{\ \nsupseteq }{\ 2}', ooxml_to_latex.result)

    def test_pm(self):
        xml_string = read_xml('pm.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 3}{\ \pm  }{\ 2}', ooxml_to_latex.result)

    def test_propto(self):
        xml_string = read_xml('propto.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 5}{\ \propto  }{\ 10}', ooxml_to_latex.result)

    def test_rational_set(self):
        xml_string = read_xml('rational_set.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ \mathbb{Q} }', ooxml_to_latex.result)

    def test_real_set(self):
        xml_string = read_xml('real_set.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ \mathbb{R} }', ooxml_to_latex.result)

    def test_sim(self):
        xml_string = read_xml('sim.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 2}{\ \sim  }{\ 5}', ooxml_to_latex.result)

    def test_subset(self):
        xml_string = read_xml('subset.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 2}{\ \subset  }{\ 2}', ooxml_to_latex.result)

    def test_subseteq(self):
        xml_string = read_xml('subseteq.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 2}{\ \subseteq  }{\ 2}', ooxml_to_latex.result)

    def test_supset(self):
        xml_string = read_xml('supset.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 2}{\ \supset  }{\ 2}', ooxml_to_latex.result)

    def test_supseteq(self):
        xml_string = read_xml('supseteq.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 2}{\ \supseteq  }{\ 2}', ooxml_to_latex.result)

    def test_times(self):
        xml_string = read_xml('times.xml', fixtures_path)
        ooxml_to_latex = OOXMLtoLatexParser.parse(
            xml_string, math_symbols=unicode_to_latex)

        self.assertEquals(r'{\ 1}{\ \cdot  }{\ 2}', ooxml_to_latex.result)

if __name__ == '__main__':
    unittest.main()
