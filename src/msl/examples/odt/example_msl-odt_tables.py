#pylint: disable=C0103
"""Example of using odt.py to create tables."""
try:
    from msl.odt import Document
except ImportError as error:
    raise ImportError("msl-odt module is not installed. "
                      "Please install it first.") from error

doc = Document("example_msl-odt_tables.odt")

# Table data
header_row = ['Name', 'Age', 'Town']
name = ['Alice', 'Bobby', 'Charlise']
age = [30.123, 0.123456, 123]
town = ['Hell', 'Belmont', 'Longyearbyen']

# Note: IDE will give error as doc undefined until runtime
table_data = [header_row] + doc.maketabledata(name, age, town)
# Or alternatively
table_data = doc.maketabledata(name, age, town, header_row=header_row)

doc.addheading1('Adding tables with odt.py')
doc.addtext('This document shows how to add tables using the addtable() '
            'function in odt.py\n'
            'First, open a document. E.g. doc=Document("example_msl-odt_tables.odt")\n'
            'Tables are added with doc.addtable()\n'
            '\nOpen Document tables are written row-by-row. '
            'The helper function maketabledata() can be used to combine '
            'column variables, and an optional header row, into a suitable '
            'format for use with addtable().\n'
            'E.g.: doc.addtable(maketabledata(col1data, col2data, '
            'header_row=["col1label", "col2label"]))\n'
            )

doc.addheading2('Example 1')
doc.addtext('Individual column widths with decimal tab stop on second column')
doc.addtext('doc.addtable(table_data, column_width=[3.5, 4.0, 5],\n'
            '\tdecimal_tab=[None, 0.4, None],\n'
            '\tborder_style="Header row")')
doc.addtable(table_data, column_width=[3.5, 4.0, 5],
             decimal_tab=[None, 0.4, None],
             border_style="Header row")

doc.addtext('Note: decimal tab stop too small, numbers not aligned.\n')

doc.addheading2('Example 2')
doc.addtext('Single column width with decimal tab stop on second column')
doc.addtext('doc.addtable(table_data, column_width=4.5,\n'
            '\tdecimal_tab=[None, 1.1, None],\n'
            '\tborder_style="All")')
doc.addtable(table_data, column_width=4.5,
             decimal_tab=[None, 1.1, None],
             border_style="All")
doc.addtext(f'Note: default cell text padding is {doc.tablecellpadding}.\n')

doc.addheading2('Example3')
doc.addtext('Total table width with no decimal tabs or borders')
doc.addtext('doc.addtable(table_data, table_width=3)')
doc.addtable(table_data, table_width=3)
doc.addtext('Note: column width too small, text wrapped.\n'
            'Further details can be found in odt.py')
