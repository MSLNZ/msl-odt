#pylint: disable=C0103
"""Example of using odt.py to write equations."""
try:
    from msl.odt import Document
except ImportError as error:
    raise ImportError("msl-odt module is not installed. "
                      "Please install it first.") from error

FILENAME = "example_msl-odt_math.odt"

doc = Document(FILENAME, reopen=False)

doc.addheading1('Adding equations with odt.py')

doc.addtext('This document shows how to add equations to an '
            'Open Document Foundation text document using the odt module.\n'
            'odt is a wrapper for, and therefore requires, the odfpy module. '
            'odfpy can be installed with "python pip install odfpy".\n'
            )

doc.addheading2('Adding equations')
doc.addtext('Using odt and Python to write out Open Document (.odt) files '
            'with equations is straightforward. In Python, first import the '
            'module with "from msl.odt import Document", next open a document '
            'with, e.g., "doc=Document(my_odt_file)".')
doc.addtext('The primary function for adding mathematical equations in odt is '
            'addequation() which takes arguments:')

parameter_list = [  # NOTE: change if odt.py code changes
    "math_text of type: str Default value: Required",
    "math_width of type: Optional[str] Default value: None",
    "math_height of type: Optional[str] Default value: None",
    "wrap of type: Optional[bool] Default value: False"
    ]
doc.addbulletedlist(parameter_list)
doc.addtext('and would be called as, e.g., '
            'doc.addequation(equation_string, "5cm", "7cm") or \n'
            'doc.addfigure(equation_string, image_width=image_width, '
            'image_height=image_height), \n'
            'where image_file, image_width and '
            'image_height are variables of type: str.\n')

doc.addheading2('Equation syntax and sizing')
doc.addtext('The format for the equation_string input follows the '
            'Star Math 5.0 notation used by Open Office and others. See:\n'
            'https://wiki.openoffice.org/wiki/Documentation/'
            'OOoAuthors_User_Manual/Writer_Guide/Math_commands_-_Reference \n'
            'for details on the command set.\n'
            'The syntax is not too dissimilar to LaTex syntax for math.\n'
            'A few useful points:')
doc.addbulletedlist([
            'In general, Greek letters are specified as %letter for lower '
            'case and %LETTER for upper case. E.g. %alpha and %OMEGA.',
            'Most characters will be italicised, as usual for equation text, '
            'to use normal text surround it with \'"\' characters. '
            'E.g. "Some non-italics text".',
            'To group operators or operations, e.g. for a fraction which '
            'is specified as numerator over denominator, enclose items in '
            'braces \'{ }\'. E.g. {a+b+c} over {e+f+g}',
            'Superscripts are signified with the \'^\' character and '
            'subscripts with the \'_\' character. E.g. the area of a circle '
            'would be specified as "%pi times r^3" where r is the radius',
            'Stacking of equations can either be done \'manually\' - by '
            'by adding in the required spaces or using either the '
            '\'stack\' or \'matrix\' options. See the examples in the '
            'Open Office wiki.'])
doc.addtext('\nThe width and height arguments can be used to ensure the math '
            'displays correctly. Values for math_width and math_height can be '
            'found by creating the math in a Open Document editor and then '
            'inspecting the created .xml\n\n'
            'Note 1: if no sizing is provided, or if the sizing is wrong, '
            'the equation will still be written. '
            'It is possible to manually resize equations to the minimum '
            'required size by opening the .odt file in Apache Open Office '
            'and double-clicking the equation. This opens the equation editor '
            'and after closing this and returning to the main .odt document '
            'the equation will now be right-sized. The edited document can '
            'then be manually saved.\n\n'
            'Note 2: equations are written "inline" by default to allow them '
            'to be included in sentences. To ensure text is written on the '
            'line after the equation use "wrap=True" in addequation().')
doc.addpagebreak()  # For formatting
doc.addheading2('Example 1')
equation = '"Area" = %pi R^2'  # The equation string
doc.addtext('Basic equations with text wrapping:')
doc.addtext(f"doc.addequation('{equation}', '5cm', '3cm', wrap=True)")
doc.addequation(equation, '5cm', '5cm', wrap=True)
doc.addtext('Note: estimated sizing and text wrapping\n'
            'With no applied sizing:')
doc.addtext(f"doc.addequation('{equation}', wrap=True)")
doc.addequation(equation, wrap=True)
doc.addtext('Note 1: no sizing\n'
            'Note 2: double-clicking on the above equation in Apache '
            'Open Office will open the equation editor. When this is closed '
            'and focus returns to the main document the frame containing the '
            'equation will be auto-resized to a minimum bounding box.\n'
            'With no height applied:')
doc.addtext(f"doc.addequation('{equation}', math_width=\"4cm\", wrap=True)")
doc.addequation(equation, math_width="4cm", wrap=True)
doc.addtext('Note 1: height wrong? '
            'As before, double-clicking the equation, then exiting the '
            'equation editor will cause the frame surrounding the equation to '
            'be auto-resized.\n')

doc.addpagebreak()  # For formatting
doc.addheading2('Example 2')
doc.addtext('To create stacked equations it is generally easiest to use '
            'either the \'stack\' or \'matrix\' options. When using '
            '\'stack\' to align equations the \'phantom\' command is '
            'to make subsequent left hand side variables invisible.\n'
            'Example using \'matrix\':')
matrix_align = '''matrix{
a # "=" # alignl{b} ##
{} # "=" # alignl{c+1}
}'''
doc.addequation(matrix_align, math_width="2.6cm", math_height="1.4cm",
                wrap=True)  # sizing obtained by inspecting doc and re-running
doc.addtext('is produced from the math code\n'
            f'{matrix_align}\n'
            'Example using \'stack\':')
stack_align = '''stack{
alignl{a} = b #
alignl{phantom{a} = c+1}
}'''
doc.addequation(stack_align, math_width="1.9cm", math_height="1.3cm",
                wrap=True)  # sizing obtained by inspecting doc and re-running
doc.addtext('is produced from the math code\n'
            f'{stack_align}\n\n'
            'See:\n'
            'https://wiki.openoffice.org/wiki/Documentation/'
            'OOoAuthors_User_Manual/Writer_Guide/Math_commands_-_Reference \n'
            'for further details on the full command set.\n')
