# pylint: disable=C0103
"""Example of using odt.py to write figures."""
try:
    from msl.odt import Document
except ImportError as error:
    raise ImportError("msl-odt module is not installed. "
                      "Please install it first.") from error

FILENAME = "example_msl-odt_figures.odt"

doc = Document(FILENAME, reopen=False)

doc.addheading1('Adding figures with odt.py')

doc.addtext('This document shows how to add figures to an '
            'Open Document Foundation text document using the odt module.\n'
            'odt is a wrapper for, and therefore requires, the odfpy module. '
            'odfpy can be installed with "python pip install odfpy".\n\n'
            )

doc.addheading2('Adding figures')
doc.addtext('Using odt and Python to write out Open Document (.odt) files '
            'with figures is straightforward. In Python, first import the '
            'module with "from msl.odt import Document", next open a document '
            'with, e.g., "doc=Document(my_odt_file)".')
doc.addtext('The primary function for adding images in odt is '
            'addfigure() which takes arguments:')

parameter_list = [    # NOTE: change if odt.py code changes
    "image_filename of type: str Default value: Required",
    "image_width of type: str Default value: Required",
    "image_height of type: str Default value: Required",
    "caption_text of type: Optional[str] Default value: None"
]
doc.addbulletedlist(parameter_list)
doc.addtext('and would be called as, e.g., '
            'doc.addfigure(image_file, "5cm", "7cm") or \n'
            'doc.addfigure(image_file, image_width=image_width, '
            'image_height=image_height), \n'
            'where image_file, image_width and '
            'image_height are variables of type: str.\n')

doc.addheading2('Example images')
TESTCARD_1 = 'Sweden_TV1_colour_1969.png'
TESTCARD_2 = 'PM5544_with_non-PAL_signals.png'

doc.addtext('The following images are publically available:')
doc.addnumberedlist([
    'htps://commons.wikimedia.org/wiki/File:Sweden_TV1_colour_1969.png',
    'https://commons.wikimedia.org/wiki/File:PM5544_with_non-PAL_signals.png'])
doc.addtext('and will be used as the test images in this document and ')
doc.addtext('will be labelled "TESTCARD_1" and "TESTCARD_2" in the examples below.')
doc.addtext('See over the page - pagebreak created using doc.addpagebreak() - '
            'for examples.')
doc.addpagebreak()

doc.addheading2('Example 1')
doc.addtext('Basic figure addition:')
doc.addtext('doc.addfigure(TESTCARD_1, "7cm", "5cm")')
doc.addfigure(TESTCARD_1, "7cm", "5cm")
doc.addtext('Note: no caption\n')

doc.addheading2('Example 2')
image_width = '8cm'
image_height = '8cm'
caption_text = 'Figure 2. The PM5544 test card'
doc.addtext('Figure addition with caption:')
doc.addtext('doc.addfigure(TESTCARD_2,\n'
            '\timage_width=image_width,\n'
            '\timage_height=image_height,\n'
            '\tcaption_text=caption_text)')
doc.addfigure(TESTCARD_2,
              image_width=image_width,
              image_height=image_height,
              caption_text=caption_text)
doc.addtext('where:')
doc.addbulletedlist([f'image_width="{image_width}"',
                     f'image_height="{image_height}"',
                     f'caption_text="{caption_text}"'])
doc.addtext('Note: addfigure() does not do automatic numbering or labelling '
            'of captions.')
