#pylint: disable=C0103
"""Example of using odt.py to write basic text."""
import inspect # to get a list of functions in odt
try:
    from msl.odt import Document
except ImportError as error:
    raise ImportError("msl-odt module is not installed. "
                      "Please install it first.") from error
FILENAME = "example_msl-odt_introduction.odt"

doc = Document(FILENAME, reopen=False)

doc.addheading1('Creating a basic text document with odt.py')

doc.addtext('This document shows how to add simple text to an '
            'Open Document Foundation text document using the odt module.\n'
            'odt is a wrapper for, and therefore requires, the odfpy module. '
            'Which can be installed with "python pip install odfpy".\n\n'
            )

doc.addheading2('Open Document Foundation text')
doc.addtext('An .odt file is simply a renamed zip file containing .xml code '
            'which various editors can display in a human-readable form. '
            'This can be seen by renaming a .odt file with a .zip extension. '
            'If the file is opened with a suitable archive program it will '
            'contain a "content.xml" file along with other items, all of '
            'which together can be processed by a document editor to give a '
            'human-readable text.\n'
            'This is different to, e.g., LaTeX where the text document is '
            'usually "compiled" to produce the final formatted document, '
            'e.g. a .pdf file.\n '
            'While LaTeX is an extremely capable document creation system, '
            'more WYSIWIG (What You See Is (mostly) What You Get) editors '
            'such as Word, Google Docs or open source ones like Apache '
            'Open Office or LibreOffice can work with .odt files.\n')
doc.addheading2('Available functions')
doc.addtext('The following functions are available in odt:')
# Get a list of all the addXYZ() functions in odt module
odtclass = doc.__class__
# Filter for functions that start with 'add'
add_functions = [name for name, func in \
                 inspect.getmembers(odtclass, inspect.isfunction) \
                     if name.startswith('add')]
doc.addlist(add_functions,list_style='bullet')

doc.addtext('\n\n')
doc.addheading2("Using functions")
doc.addtext('Using odt and Python to write out Open Document (.odt) files '
            'is straightforward. In Python, first import the module with '
            '"from msl.odt import Document", next open a document with, e.g., '
            '"doc=Document(my_odt_file)". Then call the functions available on "doc" '
            '(see list above). E.g. the following page break is created with '
            '"doc.addpagebreak()"')
doc.addpagebreak()

doc.addheading2('Adding text')
doc.addtext('The addtext() and other functions usually create new paragraphs. '
            'The input to addtext() can be formatted using escape sequences '
            'such as "\\n" (Newline) and "\\t" (Horizontal tab). E.g. '
            'this text "Lorem ipsum \\n\\tDolor sit amet \\n\\tConsecuter '
            '\\nAdipisci \\n\\nElit, sed." produces:'
            )
doc.addtext('Lorem ipsum \n\tDolor sit amet \n\tConsecuter '
            '\nAdipisci \n\nElit, sed.')
doc.addtext('\n')

doc.addheading2('Adding the rest')
doc.addtext('For examples of how to add Equations, Figures, Tables and Lists, '
            'using Python and the msl-odt module, see the other example scripts.')
