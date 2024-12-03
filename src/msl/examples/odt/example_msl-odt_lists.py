# pylint: disable=C0103
# noqa: E131, E262
"""Example of using odt.py to create lists."""
try:
    from msl.odt import Document
except ImportError as error:
    raise ImportError("msl-odt module is not installed. "
                      "Please install it first.") from error

doc = Document("example_msl-odt_lists.odt")

# List data - showing indentation
item_list = (
    "Cats",
        "Domestic Shorthair",  # noqa: E131
        "Domestic Longhair",
        "Purebred",
            "Russian Blue",
            "Siamese",
                "Seal Point",
                "Flame Point",
    "Dogs",
        "Retrievers",
            "Golden Retriever",
            "Labrador Retriever",
        "Poodles",
            "Toy Poodle",
            "Standard Poodle"
)

# Corresponding levels; set to None for level 1 for all items (e.g. below)
item_level = [
    1,  # "Cats"
    2,  #     "Domestic Shorthair"     noqa: E262
    2,  #     "Domestic Longhair"      noqa: E262
    2,  #     "Purebred"               noqa: E262
    3,  #         "Russian Blue"       noqa: E262
    3,  #         "Siamese"            noqa: E262
    4,  #             "Seal Point"     noqa: E262
    4,  #             "Flame Point"    noqa: E262
    1,  # "Dogs"
    2,  #     "Retrievers"             noqa: E262
    3,  #         "Golden Retriever"   noqa: E262
    3,  #         "Labrador Retriever" noqa: E262
    2,  #     "Poodles"                noqa: E262
    3,  #         "Toy Poodle"         noqa: E262
    3   #         "Standard Poodle"    noqa: E262
]

doc.addheading1('Adding lists with odt.py')
doc.addtext('This document shows how to add lists using the addlist() '
            'function in odt.py and the two helper functions:\n'
            '\taddbullettedlist() and\n'
            '\taddnumberedlist()\n'
            'which do simple single-level lists.'
            'First, open a document. '
            'E.g. doc=Document("example_msl-odt_lists.odt")\n'
            'In Python, lists are added with doc.addlist(), '
            'doc.addbulletedlist() or doc.addnumberedlist().\n'
            'List data is simply a list containing any types of data which '
            'can be written as text into the document.\n')

doc.addheading2('Example 1')
doc.addtext('Basic bulleted list')
doc.addtext('doc.addbulletedlist(item_list)')
doc.addbulletedlist(item_list)
doc.addtext('Note 1: all items at top level.')
doc.addtext('Note 2: equivalent to doc.addlist(item_list, '
            'item_level=None, list_style="bullet").\n')
doc.addheading2('Example 2')
doc.addtext('Basic numbered list')
doc.addtext('doc.addnumberedlist(item_list)')
doc.addnumberedlist(item_list)
doc.addtext('Note 1: all items at top level.')
doc.addtext('Note 2: equivalent to doc.addlist(item_list, '
            'item_level=None, list_style="number").\n')
doc.addheading2('Example 3')
doc.addtext('Bulleted list with sub-levels')
doc.addtext('doc.addlist(item_list, '
            'item_level=item_level, list_style="bullet")')
doc.addlist(item_list, item_level=item_level, list_style="bullet")
doc.addtext('Note: uses Open Office default bullet labels and indent.\n')

doc.addheading2('Example 4')
doc.addtext('Numbered list with sub-levels')
doc.addtext('doc.addlist(item_list, '
            'item_level=item_level, list_style="number")')
doc.addlist(item_list, item_level=item_level, list_style="number")
doc.addtext('Note: uses Open Office default indent '
            'and number format for labels.\n')

# Add a pagebreak
doc.addpagebreak()
doc.addheading2('Example 5')
doc.addtext('The Default')
doc.addtext('doc.addlist(item_list)')
doc.addlist(item_list)
doc.addtext('Note: equivalent to doc.addlist(item_list, '
            'item_level=None, list_style=None).\n')
