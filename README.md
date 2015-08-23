# Ooxml to latex parser

A parser to transform Open Office Xml equations in latex equations

### What is Open Office XML (ooxml)

Open Office XML is a zipped, xml based file format developed by Microsoft for representing spreadsheets, charts, presentations and word processing documents.

### The objective of this project

This projects aims to transform ooxml oMath tags, used to represent equations in word, in latex equations.

### What this project won't do

Is not in the scope open and extract xml files from **.docx** and even not handle other tags that isn't specified in [http://www.datypic.com/sc/ooxml/s-shared-math.xsd.html](http://www.datypic.com/sc/ooxml/s-shared-math.xsd.html)

# Usage

## instalation

	pip install -r requirements.txt

## usage

```python
# coding: utf-8
from ooxml_to_latex.ooxml_to_latex import OOXMLtoLatexParser

# real numbers set
xml = '''
<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
	<m:r>
		<w:rPr>
			<w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>
		</w:rPr>
		<m:t xml:space="preserve">ℝ</m:t>
	</m:r>
</m:oMath>
'''

# main function
# receives a xml string and returns a latex
latex = OOXMLtoLatexParser.parse(xml)

print latex
>>> \mathbb{R}
```

# Suported tags

These are the currently supported tags, more are comming!!

Documentation [here](http://www.datypic.com/sc/ooxml/s-shared-math.xsd.html)

* begChr
* endChr
* chr
* pos
* sub
* sup
* f
* e
* m
* mr
* limLow
* rad
* deg
* den
* num
* lim
* r
* d