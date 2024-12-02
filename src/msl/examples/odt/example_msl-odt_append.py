# pylint: disable=C0103
""" Example of using odt.py to append.
    Add new tables to an existing document
    Such as that created by example_msl-odt_tables.py
"""
try:
    from msl.odt import Document
except ImportError as error:
    raise ImportError("msl-odt module is not installed. "
                      "Please install it first.") from error
from pathlib import Path
from shutil import copy
from subprocess import run

source_filename = Path("example_msl-odt_readme.odt")  # The source file
filename = Path("example_msl-odt_append.odt")  # Filename for append
if not source_filename.exists():
    print(f"{source_filename} does not exist. Creating it now.")
    run(["python", "example_msl-odt_tables.py"],  # run example_msl-odt_tables
        check=True)
copy(source_filename, filename)

doc = Document(filename, reopen=True)

# Table data
header_row = ['Name', 'Age', 'Town']
name = ['Data', 'Ego', 'Foxtrot']
age = [40.567, 0.45678, 456]
town = ['Dubbo', 'Pitcairn Is.', 'Mosgiel']

table_data = [header_row] + doc.maketabledata(name, age, town)
# Or alternatively
table_data = doc.maketabledata(name, age, town, header_row=header_row)

doc.addpagebreak()
doc.addheading1('Appending tables with odt.py')
doc.addtext('This document shows how to append additional tables '
            'using the "reopen=True" option in odt.py\n'
            'First, open a document for appending. '
            'E.g. doc=Document(filename, reopen=True)\n'
            'Then add tables using doc.addtable()\n'
            'See example_msl-odt_tables.py for other examples.'
            )
doc.addheading2('Example 1')
doc.addtext('Individual column widths with decimal tab stop on second column')
doc.addtext('doc.addtable(table_data, column_width=[3, 4.0, 5.5], \n'
            '\tdecimal_tab=[None, 0.7, None], \n'
            '\tborder_style="All")')
doc.addtable(table_data, column_width=[3, 4.0, 5.5],
             decimal_tab=[None, 0.7, None],
             border_style="All")
doc.addtext('Note: decimal tab needs to be large enough for numbers to align.\n')

doc.addheading2('Example 2')
doc.addtext('Single column width with decimal tab stop on second column')
doc.addtext('doc.addtable(table_data, column_width=5.5, \n'
            '\tdecimal_tab=[None, 1.1, None], \n'
            '\tborder_style="Header row")')
doc.addtable(table_data, column_width=5.5,
             decimal_tab=[None, 1.1, None],
             border_style="Header row")
doc.addtext(f'Note: default cell text padding is {doc.tablecellpadding}.\n')

doc.addheading2('Example3')
doc.addtext('Total table width with no decimal tabs or borders')
example_3 = '''doc.addtable(table_data, table_width=14)'''
doc.addtext(example_3)
doc.addtable(table_data, table_width=14)
doc.addtext('Note: table width needs to be sufficient or text will wrap.\n'
            'Further details can be found in odt.py')
