# pylint: disable=C0302, R0205, R0902, R0913, R0914, R0915
"""
A module to help write ODT documents with Python.
"""
from typing import List as ListType, Optional, Union, Iterable, Any
from os import remove
from contextlib import suppress
from pathlib import Path
from re import compile as regex
from re import sub as substitute
from datetime import datetime, timezone
try:
    from odf.opendocument import OpenDocumentText, load
    from odf import teletype, easyliststyle
    from odf.style import (Style, TextProperties, ParagraphProperties,
                           TabStop, TabStops, # Both needed. A TabStop is added to TabStops
                           GraphicProperties,
                           TableProperties, TableColumnProperties,
                           TableCellProperties)
    from odf.text import (H as Heading,
                          P as Paragraph,
                          A as Anchor,
                          # Span, # allows formatting within paragraphs (TBD)
                          List, # avoid conflict with List type by remaning type
                          ListItem)
    from odf.draw import Image, Frame, Object
    from odf.table import Table, TableColumn, TableRow, TableCell
    from odf.math import Math
    from odf.element import Element
    from odf.meta import InitialCreator, CreationDate, UserDefined
except ImportError as error:
    raise ImportError("The odfpy library is required for this module. "
                      "Please install it with python - m pip install odfpy") from error
from warnings import warn
# PyLint thinks there's a problem in the following import - but there isn't
# so diable the warning
from namespaces import MATHNS  # pylint: disable=E0401

class Document(object):
    """
    A class to create and manipulate Open Document Text (ODT) files.

    This class provides methods to add various elements to an ODT document,
    including headings, paragraphs, figures, equations, tables, and lists.
    It supports features such as converting URLs into hyperlinks, managing
    styles, and handling tables with optional formatting and captions.

    Attributes
    ----------
    filename : Union[str, Path]
        The name of the file to create or open.
    doc : OpenDocumentText
        The OpenDocumentText object representing the ODT document.

    Methods
    -------
    __init__(filename: Union[str, Path], reopen: bool = False):
        Initializes the document class, creating a new ODT file or
        reopening an existing one.

    addheading1(headingText: str) -> None:
        Adds a Level 1 heading to the document.

    addheading2(headingText: str) -> None:
        Adds a Level 2 heading to the document.

    addtext(text: str) -> None:
        Adds a new paragraph to the document and converts URLs to hyperlinks.

    addfigure(image_filename: str, image_width: str, image_height: str, \
              caption_text: Optional[str] = None) -> None:
        Adds an image to the document with an optional caption.

    addequation(math_text: str, math_width: Optional[str] = None, \
                math_height: Optional[str] = None, wrap: Optional[bool] = False) -> None:
        Adds a mathematical equation to the document.

    addpagebreak() -> None:
        Adds a page break to the document.

    initialize_table_count() -> None:
        Updates the table count if there are existing tables.

    maketabledata(*args: Iterable[Any], \
                  header_row: Optional[ListType[str]] = None) \
        -> ListType[ListType[str]]:
        Merges multiple columns of data into a row-major list of lists for table creation.

    addtable(table_data: ListType[ListType[str]], \
             column_width: Optional[Union[ListType[Union[int, float]], Union[int, float]]] = None, \
             table_width: Optional[Union[int, float]] = None, \
             decimal_tab: Optional[ListType[Optional[Union[float, int]]]] = None, \
             caption_text: Optional[str] = None, \
             border_style: Optional[str] = None) -> None:
        Adds a table to the document with optional formatting.

    addlist(item_list: ListType[Any], \
            item_level: Optional[ListType[int]] = None, \
            list_style: Optional[str] = None) -> None: 
        Adds a hierarchical list to the document.

    addbulletedlist(item_list: ListType[Any]) -> None:
        Adds a bulleted list to the document.

    addnumberedlist(item_list: ListType[Any]) -> None:
        Adds a numbered list to the document.
    """
    def __init__(self, filename: Union[str, Path], reopen: bool = False):
        # Make filename a Path
        if isinstance(filename, str):
            filename = Path(filename)
        # Check if the filename has a .odt extension
        if not filename.name.endswith('.odt'):
            filename = filename.with_suffix('.odt')

        self.filename = filename
        self.title = filename.stem  # Get just the filename without the extension

        # Handle reopening or starting a new document
        if reopen and Path(self.filename).exists:
            self.doc = load(self.filename)  # Reopen the existing document
        else:
            self.doc = OpenDocumentText()  # Create a new document
            # Remove the document file (if it exists) and prepare to write a new one
            with suppress(FileNotFoundError):
                remove(self.filename)

        # Add metadata
        time_now = datetime.now(timezone.utc)
        time_in_min = time_now.isoformat(timespec="minutes").split("+")[0]
        self.creation_date = time_in_min
        self.doc.meta.addElement(CreationDate(text=self.creation_date))
        self.doc.meta.addElement(UserDefined(name="Title", text=self.title))
        self.doc.meta.addElement(InitialCreator(text="msl-odt"))

        # Define styles
        self.define_styles()

        # Set table count. Styles for Table and Table columns are
        # made during creation of tables and uniquely identified
        # by a style name based on an incrementing tablecount
        # so a check is needed if an existing file is opened.
        self.tablecount = 0
        self.initialize_table_count() # Increment count for existing tables


    def define_styles(self) -> None:
        """ Define styles for odt document. """
        # Headings
        self.h1style = Style(name="heading1", family="paragraph")
        self.h1style.addElement(TextProperties(
            attributes={'fontsize': "14pt", 'fontweight': "bold"}))
        self.doc.styles.addElement(self.h1style)
        self.h2style = Style(name="heading2", family="paragraph")
        self.h2style.addElement(TextProperties(
            attributes={'fontsize': "12pt", 'fontweight': "bold"}))
        self.doc.styles.addElement(self.h2style)

        # Automatic style for figures
        self.nowrapframestyle = Style(family="graphic", name="nowrap",
                                      parentstylename="Frame")
        self.nowrapframestyle.addElement(
            GraphicProperties(wrap="none",
                              horizontalrel="paragraph-content",
                              horizontalpos="center",
                              verticalrel="paragraph-content",
                              verticalpos="top",
                              runthrough="foreground"))
        self.doc.automaticstyles.addElement(self.nowrapframestyle)

        # Automatic style for page breaks
        self.afterbreakstyle = Style(name='afterbreak', family="paragraph",
                                parentstylename="Standard")
        self.afterbreakstyle.addElement(ParagraphProperties(breakafter="page"))
        self.doc.automaticstyles.addElement(self.afterbreakstyle)

        # Automatic style for Tables
        # At present only three cell border styles are used: Header Row.
        # All or None.
        # One style is needed for header row (bottom border only),
        # four for All borders and one for no borders, or None,
        # which is the default border style.
        # To make a table with all borders and no doubled up lines, Open Office
        # writes table cells using the follow sequence of border styles:
        #        A1 A1 A1 ... E1
        #        A2 A2 A2 ... E2
        #         .  .  .      .
        #         .  .  .      .
        #         .  .  .      .
        #        A2 A2 A2 ... E2
        # These styles below are named firstrow, firstrow end, otherrow and
        # otherrowend.
        # Styles for Table and Table columns are made during creation
        # and uniquely identified by a style name based on an
        # incrementing tablecount
        self.tablefontsize = "10pt"
        self.tableborderwidth = "0.05pt"   # line width
        self.tableborderline = "solid"     # line style
        self.tablebordercolour = "#000000" # line colour (black)
        self.tablecellpadding = "0.1cm"
        self.cellparagraphstyle = Style(name="cellparagraph",
                                        family="paragraph")
        self.cellparagraphstyle.addElement(TextProperties(
            attributes={'fontsize': self.tablefontsize}))
        self.doc.automaticstyles.addElement(self.cellparagraphstyle)
        self.cellheaderrowstyle = Style(name="cellheaderrow",
                                        family="table-cell")
        self.cellheaderrowstyle.addElement(
            TableCellProperties(padding=self.tablecellpadding,
                                borderleft="none",
                                borderright="none",
                                bordertop="none",
                                borderbottom=f'{self.tableborderwidth} '
                                             f'{self.tableborderline} '
                                             f'{self.tablebordercolour}'))
        self.doc.automaticstyles.addElement(self.cellheaderrowstyle)
        self.cellfirstrowstyle = Style(name="cellfirstrow",
                                        family="table-cell")
        self.cellfirstrowstyle.addElement(
            TableCellProperties(padding=self.tablecellpadding,
                                borderleft=f'{self.tableborderwidth} '
                                           f'{self.tableborderline} '
                                           f'{self.tablebordercolour}',
                                borderright="none",
                                bordertop=f'{self.tableborderwidth} '
                                          f'{self.tableborderline} '
                                          f'{self.tablebordercolour}',
                                borderbottom=f'{self.tableborderwidth} '
                                             f'{self.tableborderline} '
                                             f'{self.tablebordercolour}'))
        self.doc.automaticstyles.addElement(self.cellfirstrowstyle)
        self.cellfirstrowendstyle = Style(name="cellfirstrowend",
                                        family="table-cell")
        self.cellfirstrowendstyle.addElement(
            TableCellProperties(padding=self.tablecellpadding,
                                borderleft=f'{self.tableborderwidth} '
                                           f'{self.tableborderline} '
                                           f'{self.tablebordercolour}',
                                borderright=f'{self.tableborderwidth} '
                                            f'{self.tableborderline} '
                                            f'{self.tablebordercolour}',
                                bordertop=f'{self.tableborderwidth} '
                                          f'{self.tableborderline} '
                                          f'{self.tablebordercolour}',
                                borderbottom=f'{self.tableborderwidth} '
                                             f'{self.tableborderline} '
                                             f'{self.tablebordercolour}'))
        self.doc.automaticstyles.addElement(self.cellfirstrowendstyle)
        self.cellotherrowstyle = Style(name="cellotherrow",
                                        family="table-cell")
        self.cellotherrowstyle.addElement(
            TableCellProperties(padding=self.tablecellpadding,
                                borderleft=f'{self.tableborderwidth} '
                                           f'{self.tableborderline} '
                                           f'{self.tablebordercolour}',
                                borderright="none",
                                bordertop="none",
                                borderbottom=f'{self.tableborderwidth} '
                                             f'{self.tableborderline} '
                                             f'{self.tablebordercolour}'))
        self.doc.automaticstyles.addElement(self.cellotherrowstyle)
        self.cellotherrowendstyle = Style(name="cellotherrowend",
                                        family="table-cell")
        self.cellotherrowendstyle.addElement(
            TableCellProperties(padding=self.tablecellpadding,
                                borderleft=f'{self.tableborderwidth} '
                                           f'{self.tableborderline} '
                                           f'{self.tablebordercolour}',
                                borderright=f'{self.tableborderwidth} '
                                            f'{self.tableborderline} '
                                            f'{self.tablebordercolour}',
                                bordertop="none",
                                borderbottom=f'{self.tableborderwidth} '
                                             f'{self.tableborderline} '
                                             f'{self.tablebordercolour}'))
        self.doc.automaticstyles.addElement(self.cellotherrowendstyle)

        # Automatic styles for lists
        # At present only two list labelling styles are used: Bullet or Number
        # The 'bullet' style uses the default characters used by Open Office.
        # and 'number' style follows the default numbering style
        # The labelling style is to show only the entry for that level e.g.:
        #     1)    some text
        #         1)    some more text
        #         2)    even more text
        # To show all levels in the item label e.g:
        #     1)    some text
        #         1.1)    some more text
        #         1.2)    even more text
        # change the indentlabelstyle to easyliststyle.SHOW_ALL_LEVELS below
        self.listindent = "0.635cm" # default indent for sub-lists == 0.25 in
        self.indentlabelstyle = easyliststyle.SHOW_ONE_LEVEL
        # self.indentlabelstyle = easyliststyle.SHOW_ALL_LEVELS
        self.bulletlistarray = ('•', '◦', '▪') * 4 # Label characters
        self.bulletliststyle = easyliststyle\
                                  .styleFromList('bullet',
                                                 self.bulletlistarray,
                                                 self.listindent,
                                                 self.indentlabelstyle)
        self.doc.automaticstyles.addElement(self.bulletliststyle)
        self.numberlistarray = ('1.',) * 10 # Label format
        self.numberliststyle = easyliststyle\
                                  .styleFromList('number',
                                                 self.numberlistarray,
                                                 self.listindent,
                                                 self.indentlabelstyle)
        self.doc.automaticstyles.addElement(self.numberliststyle)

        # Define automatic styles -TBD
        # boldstyle = Style(name="Bold", family="text")
        # boldprop = TextProperties(fontweight="bold")
        # boldstyle.addElement(boldprop)
        # thisdoc.automaticstyles.addElement(boldstyle)

    def addheading1(self, heading_text: str) -> None:
        """
        Add a Level 1 Heading to document.

        Parameters
        ----------
        heading_text : str
            The heading text to add.

        Returns
        -------
        None.

        """
        heading_paragraph = Heading(outlinelevel=1, stylename=self.h1style,
                                    text=heading_text)
        self.doc.text.addElement(heading_paragraph)

    def addheading2(self, heading_text: str) -> None:
        """
        Add a Level 2 heading to document.

        Parameters
        ----------
        heading_text : str
            The heading text to add.

        Returns
        -------
        None.

        """
        heading_paragraph = Heading(outlinelevel=2, stylename=self.h2style,
                                    text=heading_text)
        self.doc.text.addElement(heading_paragraph)

    def addtext(self, text: str) -> None:
        """
        Add a new paragraph to document

        Parameters
        ----------
        text : str
            Text to add. The use of `\t` and `\n` are supported.
            Uses ODFPY `teletype` function to handle whitespace.
            Detects URLs starting with `http://` or `https://`
            and converts them to hyperlinks.
        Returns
        -------
        None.

        """
        # Regular expression to detect URLs
        url_pattern = regex(r"(http[s]?://[^\s]+)")

        paragraph_element = Paragraph()
        # Split text into parts, separating URLs from other text
        parts = url_pattern.split(text)
        for part in parts:
            if url_pattern.match(part):
                # If it's a URL, add a hyperlink (A element)
                link = Anchor(href=part, text=part)
                paragraph_element.addElement(link)
            else:
                # Otherwise, it's normal text, add it to the paragraph
                teletype.addTextToElement(paragraph_element, part)

        #teletype.addTextToElement(paragraph_element, text)
        self.doc.text.addElement(paragraph_element)

    # Add a figure inline in a paragraph
    def addfigure(self, image_filename: str, image_width: str, image_height: str, \
                  caption_text: Optional[str] = None) -> None:
        """
        Add an image to document as a separate paragraph, with optional caption.

        The image needs to be added to the `.odt` document and then as an element
        to a frame which is added to a paragraph, which is added to the doc.
        The name of the frame is set to the image filename.

        Optional caption text can be added. No auto-numbering is done
        so to obtain numbered figures use, e.g.,
        caption_text='Figure 123: Desired caption text'.

        If the file does not exist text to that effect is added to the document
        as a placeholder.

        Parameters
        ----------
        image_filename : str
            The image file to add to the ODT file.
            File name as a string, not a file handle.
        image_width : str
            Width of the image in the document.
            Example: "8cm"
        image_height : str
            Height of the image in the document.
            Example: "5cm"
        caption_text : Optional[str]
            Optional text added to a second paragraph as plain text.
            There is no auto-numbering so to obtain numbered figures use, e.g.,
            caption_text='Figure 123: Desired caption text'.

        Returns
        -------
        None.

        """
        picture_paragraph = Paragraph(stylename="Standard")
        if Path(image_filename).exists():
            picref = self.doc.addPicture(image_filename)  # add picture to file
            # Clean up filename to make it valid as a frame name
            # allowing alphanumeric, underscore and hyphen characters
            # and substituting underscores (_) for all others.
            frame_name = substitute(r'[^a-zA-Z0-9]', '_',
                                    Path(image_filename).stem)

            picture_frame = Frame(stylename=self.nowrapframestyle,
                                  width=image_width, height=image_height,
                                  anchortype="paragraph")
            picture_frame.setAttribute("name", frame_name)
            picture_frame.addElement(Image(href=picref))
            picture_paragraph.addElement(picture_frame)
        else:
            teletype.addTextToElement(picture_paragraph,
                                      f'Error: file {image_filename} '
                                      f'does not exist.')
        self.doc.text.addElement(picture_paragraph)
        if caption_text:
            caption_paragraph = Paragraph(stylename="Caption")
            teletype.addTextToElement(caption_paragraph, caption_text)
            self.doc.text.addElement(caption_paragraph)

    def addequation(self, math_text: str, \
                    math_width: Optional[str] = None, \
                    math_height: Optional[str] = None, \
                    wrap: Optional[bool] = False) -> None:
        """
        Add some math as a separate paragraph.

        Create an annotation using the Star Math 5.0 notation
        used by Open Office and others.
        See: wiki.openoffice.org/wiki/Documentation/
             OOoAuthors_User_Manual/Writer_Guide/Math_commands_-_Reference
        for details on the command set.

        The annotation is put into a frame which is attached to a paragraph.
        The width and height arguments can be used to ensure the math displays
        correctly. Values for `math_width` and `math_height` can be found by
        creating the math in a Open Document editor and then inspecting the
        created `.xml`
        If no sizing is given the equation can still be manually resized by
        opening and editing the `.odt` file.

        Parameters
        ----------
        math_text : str
            A string containing the equation in Star Math 5.0 notation.
            Example '"Area" = %pi R^2'
        math_width : str
            Width of the math text frame.
            Example: "5.3cm"
        math_height : str
            Height of the math text frame.
            Example: "3.5cm"
        wrap : bool
            Whether or not the surrounding text is wrapped.
            Default is False.
            Example 'wrap=True'

        Returns
        -------
        None.

        """
        # To make a math formula in Open Format Documents requires two things.
        # 1) A math annotation object
        # 2) A frame (in a paragraph) which has the object in it.
        # First, the math annotation object
        math_object = Math()
        math_annotation = Element(qname=(MATHNS,'annotation'))
        math_annotation.addText(math_text, check_grammar=False)
        math_annotation.setAttribute((MATHNS,'encoding'),'StarMath 5.0',
                                    check_grammar=False)
        math_object.addElement(math_annotation)
        # Second, add the object to a frame, inside a paragraph
        math_draw_object = Object()
        math_draw_object.addElement(math_object)
        if math_width and math_height:
            if wrap:
                math_frame = Frame(stylename=self.nowrapframestyle,
                                  width=math_width,
                                  height=math_height,
                                  anchortype="paragraph")
            else:
                math_frame = Frame(width=math_width,
                                  height=math_height,
                                  anchortype="paragraph")
        elif math_width and (not math_height): # width but no height specified
            if wrap:
                math_frame = Frame(stylename=self.nowrapframestyle,
                                  width=math_width,
                                  anchortype="paragraph")
            else:
                math_frame = Frame(width=math_width,
                                  anchortype="paragraph")
        elif math_height and (not math_width): # height but no width specified
            if wrap:
                math_frame = Frame(stylename=self.nowrapframestyle,
                                  height=math_height,
                                  anchortype="paragraph")
            else:
                math_frame = Frame(height=math_height,
                                  anchortype="paragraph")
        else: # Neither width nor height specified
            if wrap:
                math_frame = Frame(stylename=self.nowrapframestyle,
                                  anchortype="paragraph")
            else:
                math_frame = Frame(anchortype="paragraph")

        math_frame.addElement(math_draw_object)
        math_paragraph = Paragraph(stylename="standard")
        math_paragraph.addElement(math_frame)
        self.doc.text.addElement(math_paragraph)

    def addpagebreak(self) -> None:
        """
        Add a pagebreak to the document.

        Add a page break by adding an empty paragraph of style 
        `afterbreakstyle`, which is a paragraph with specific properties
        (specifically a pagebreak after it).

        Returns
        -------
        None.

        """
        paragraph_element = Paragraph(stylename=self.afterbreakstyle)
        self.doc.text.addElement(paragraph_element)

    def initialize_table_count(self) -> None:
        """
        Update table_count if there are any existing tables.

        Returns
        -------
        None.

        """
        # Access the automatic styles in the document
        for style in self.doc.automaticstyles.getElementsByType(Style):
            # Check if the style name matches the table naming pattern
            style_name = style.getAttribute("name")  # Get the style name
            if style_name and style_name.startswith("Table"):
                # Extract the number from the style name
                try:  # Get number after 'Table'
                    table_number = int(style_name[5:])
                    if table_number >= self.tablecount:     # Set to next
                        self.tablecount = table_number + 1  # available count
                except ValueError:
                    continue  # Ignore styles that don't have a valid number

    def maketabledata(self, *args: Iterable[Any],
                      header_row: Optional[ListType[str]]=None) -> ListType[ListType[str]]:
        """
        Merge variables (columns) into row-major list of lists for table creation.

        Each column (variable) is provided as a separate argument, which can be
        a `list`, `numpy` array, or any iterable.
        Formats `float` or `int` items to `str`.

        For more precise formatting, convert data to `str` before calling
            e.g.: `[f'{i:0.2f} for i in my_variable]`
                  `[f'{i:0.4E} for i in my_variable]`
                  etc.
        And optional header row can be supplied as the last argument.
        It must be supplied as a keyword argument e.g.:
            `maketabledata(col1, col2, header_row=['Name', 'Age'])`

        Parameters
        ----------
        *args : Iterable[Any]
            Variable number of iterables (e.g., `list`s, `numpy` arrays etc.),
            each representing a column.
            Raises error if iterables have different lengths.

        header_row : Optional[List[str]]
            Optional list of labels for header row.
            Must be given as a keyword argument e.g.
                `table_data = maketabledata(column1data,
                                            column2data,
                                            header_row=headerrowdata)`
            Default is `None`, which means only column data are provided.
            In this case the header row can be prepended e.g.:
                `table_data = [headerrowdata] + maketabledata(column1data,
                                                              column2data)`
        Returns
        -------
        list of list : Row-major data where each inner list
                       represents a row of the table.
        """
        # Ensure all arguments have the same length
        num_rows = len(args[0])
        if any(len(column) != num_rows for column in args):
            raise ValueError("Columns must have identical number of elements.")

        # Combine columns into rows
        # The zip function combines elements from multiple lists into tuples.
        # *args unpacks the list of column input variables, so
        # zip(*args) creates tuples where each tuple represents a row
        # with elements from each column.
        table_data = [[f'{cell}' for cell in row] for row in zip(*args)]
        # Prepend header row if provided
        if isinstance(header_row, ListType):
            if len(header_row) != len(args):
                raise ValueError("Number of items in 'header_row' must match number of columns.")
            table_data = [header_row] + table_data
        return table_data


    # Add table to document
    def addtable(self, table_data: ListType[ListType[str]],
                 column_width: Optional[Union[ListType[Union[int, float]],
                                              Union[int, float]]] = None,
                 table_width: Optional[Union[int, float]] = None,
                 decimal_tab: Optional[ListType[Optional[Union[float, int]]]]
                              = None,
                 caption_text: Optional[str]=None,
                 border_style: Optional[str]=None) -> None:
        """
        Add table with optional column or table width/s and header row.

        Table data is row-major form (rows then columns) and widths can
        be specified either individually or a single value for all columns
        or just a single table width. If no widths are specified the columns
        are all made as wide as possible.
        Additionally, numerical values (as `str`) can be aligned on the
        decimal point character by specifying a tab stop for that column.

        The optional caption is added to a second paragraph as plain text.
        There is no auto-numbering so to obtain numbered tables use, e.g.,
        caption_text='Table 123: Desired caption text'.

        Optional border styles can be applied to the table. The default
        is no borders.

        See also: companion function `maketable_data` which combines multiple
                  arguments (columns) and merges them into a row-major
                  `list` of `list`s suitable for input to `addtable`.
                  A header row can either be a separate argument
                  or pre-pended as required.
                  E.g.: 1) `addtable(maketabledata(column1data,
                                                   column2data,
                                                   header_row=header_row))`
                     or 2) `addtable([header_row] + maketabledata(column1data,
                                                                  column2data))`
        Parameters
        ----------
        table_data : List[List[str]]
            A list of lists containing text for each row of the table.
            Example ``[['User', 'Cost ($)'] ['Alice', '1.23'] ['Bob', '12.3']]``
        column_width : Optional[Union[List[Union[int, float]], Union[int, float]]]
            Optional list of ints or floats specifying widths of columns (cm).
            If a single value is provided, it is used for all columns.
            Example: `[1, 2.3]` or `4`, or `None`.
        table_width : Optional[Union[int, float]]
            Optional total width of table (cm).
            If specified and column_width is not provided, column widths
            will be calculated as `table_width / number of columns`.
            If both column_width and table_width are provided column_width
            will be used and a warning generated.
            Example: `3.2`
        decimal_tab : Optional[List[Optional[Union[float, int]]]]
            Optional list of floats specifying the position (cm) of the decimal
            tab stop for each column from the left column margin.
            If a column does not require a tab stop, use None.
            Example: `[None, 1.23, 2]`
        caption_text : Optional[str]
            Optional text added to a second paragraph as plain text.
            There is no auto-numbering so to obtain numbered figures use, e.g.,
            `caption_text='Figure 123: Desired caption text'`.
        border_style : Optional[str]
            Optional text specifying what borders to draw on the table.
            Currently, "None", "Header Row" or "All". Default is None.
            Note: The `MSL Style Manual` prefers "Header Row".

        Returns
        -------
        None.

        """
        def add_caption():
            """Helper function to add caption if provided."""

            if caption_text:
                caption_paragraph = Paragraph(stylename="Caption")
                teletype.addTextToElement(caption_paragraph, caption_text)
                self.doc.text.addElement(caption_paragraph)

        def calculate_column_widths():
            """Helper function to calculate column widths based on inputs."""
            num_columns = len(table_data[0]) if table_data else 0
            if column_width is None:
                if table_width is not None:
                    if not isinstance(table_width, (float, int)):
                        raise ValueError("'table_width' must be a scalar")
                    equal_width = table_width / num_columns
                    return [equal_width] * num_columns
                # If we get here something has gone wrong so ...
                raise ValueError("Either 'column_width' or "
                                 "'table_width' must be provided.")
            if isinstance(column_width, (int, float)):
                return [column_width] * num_columns
            if isinstance(column_width, list) and len(column_width) == num_columns:
                return column_width
            # If we get here something has gone wrong so ...
            raise ValueError("Invalid 'column_width' argument.")

        def configure_decimal_styles():
            """Helper function to configure decimal tab stops."""
            num_columns = len(table_data[0]) if table_data else 0
            table_style_name = f"Table{self.tablecount:02}"
            styles = []
            if decimal_tab:
                for index, tab_stop in enumerate(decimal_tab):
                    if tab_stop is not None:
                        style_name = f"{table_style_name}Column{index + 1}decimal_tab"
                        style = Style(name=style_name, family="paragraph")
                        paragraph_props = ParagraphProperties()
                        tab_stops = TabStops()
                        tab_stop_elem = TabStop(position=f"{tab_stop}cm",
                                                type="char", char=".")
                        tab_stops.addElement(tab_stop_elem)
                        paragraph_props.addElement(tab_stops)
                        style.addElement(paragraph_props)
                        text_properties = \
                            TextProperties(attributes={'fontsize': self.tablefontsize})
                        style.addElement(text_properties)
                        self.doc.automaticstyles.addElement(style)
                        styles.append(style_name)
                    else:
                        styles.append(None)
            return styles or [None] * num_columns

        def get_border_styles(is_header=False):
            """Helper function to configure borders based on specified style."""
            num_columns = len(table_data[0]) if table_data else 0
            if border_style:
                border_style_normalized = border_style.lower()
            else:
                border_style_normalized = 'none'

            if border_style_normalized == 'header_row' and is_header:
                return [self.cellheaderrowstyle] * num_columns
            if border_style_normalized == 'all':
                return [self.cellotherrowstyle] * (num_columns - 1) \
                    + [self.cellotherrowendstyle]
            # Else no style was provided so ...
            return [None] * num_columns

        # Begin table setup
        add_caption()
        decimal_styles = configure_decimal_styles()

        # Table style
        table_style_name = f"Table{self.tablecount:02}"
        table_style = Style(name=table_style_name, family="table")
        table_style.addElement(TableProperties(
            width=f'{sum(calculate_column_widths())}cm',
            align="center"))
        self.doc.automaticstyles.addElement(table_style)

        # Create table element
        table = Table(name=f"Table{self.tablecount}", stylename=table_style_name)

        # Add columns with calculated widths
        for col_index, col_width in enumerate(calculate_column_widths()):
            column_style_name = f"{table_style_name}Col{col_index + 1:02}Style"
            column_style = Style(name=column_style_name, family="table-column")
            column_style.addElement(TableColumnProperties(columnwidth=f"{col_width}cm"))
            self.doc.automaticstyles.addElement(column_style)
            table.addElement(TableColumn(stylename=column_style_name))

        # Add header row
        header_row = TableRow()
        header_styles = get_border_styles(is_header=True)
        for i, cell_text in enumerate(table_data[0]):
            cell = TableCell(stylename=header_styles[i])
            cell.addElement(Paragraph(text=cell_text,
                                      stylename=self.cellparagraphstyle))
            header_row.addElement(cell)
        table.addElement(header_row)

        # Add remaining rows with border and decimal styles
        for row in table_data[1:]:
            table_row = TableRow()
            row_styles = get_border_styles()
            for i, cell_text in enumerate(row):
                cell = TableCell(stylename=row_styles[i])
                paragraph_style = decimal_styles[i] if decimal_styles[i] \
                    else self.cellparagraphstyle
                cell.addElement(Paragraph(text=cell_text,
                                          stylename=paragraph_style))
                table_row.addElement(cell)
            table.addElement(table_row)

        # Finalize table
        self.doc.text.addElement(table)
        self.tablecount += 1


    def addlist(self, item_list: ListType[Any],
                item_level: Optional[ListType[int]] = None,
                list_style: Optional[str] = None) -> None:
        """
        Add a hierarchical list (bulleted or numbered) to `.odt` document.

        Parameters
        ----------
        item_list : List[Any]
            A list of objects representing the items to be included in the list.
        item_level : Optional[List[int]]
            A list of integers representing the hierarchical level for each item.
                If not provided, all items are at the top level (level 1).
        list_style : str
            The style of the list, either bulleted or numbered.
            Must be one of the two valid values: 'bullet' or 'number'.
            If no list_style is provided, 'bullet' is used.

        Raises
        ------
        ValueError
            If `item_level` has fewer elements than `item_list`
            or if an invalid list structure is detected.
        ValueError
            If `list_style` is not 'bullet' or 'number'.
        """

        def validate_list_style(list_style: str) -> str:
            """Helper function to validate list_style argument."""
            if list_style:
                list_style = list_style.lower()
                if list_style not in ('bullet', 'number'):
                    raise ValueError(f"Invalid list style: {list_style}. "
                                     "Must be 'bullet' or 'number'.")
                return self.bulletliststyle if list_style == 'bullet' \
                    else self.numberliststyle
            # If we get here no style was provided so ...
            warn("No style provided for list. Using 'bullet' style.")
            return self.bulletliststyle

        def initialise_list_array() -> list:
            """Helper function to initialise list array."""
            list_array = [None] * 10  # ODT lists have <= 10 sublevels
            list_array[0] = List()
            return list_array

        def open_sublevels(list_array, start_level, target_level):
            """Helper function to open sublist levels as required."""
            for level_count in range(start_level + 1, target_level + 1):
                list_array[level_count] = List()

        def close_sublevels(list_array, start_level, target_level):
            """Helper function to close sublist levels as required."""
            for level_count in range(start_level, target_level, -1):
                list_array[level_count - 1].childNodes[-1].\
                    addElement(list_array[level_count])

        # Validate style and initialise list array
        liststyle = validate_list_style(list_style)
        list_array = initialise_list_array()

        if not item_level:  # Default - all items at top level
            item_level = [1] * len(item_list)

        if len(item_level) < len(item_list):
            raise ValueError('A list level must be provided for each list item.')

        # Do first list item - level 0
        if item_level[0] != 1:
            raise ValueError('List level must start at 1.')
        list_array[0].setAttribute('stylename', liststyle)
        list_item = ListItem()
        para = Paragraph(text=f'{item_list[0]}')
        list_item.addElement(para)
        list_array[0].addElement(list_item)
        last_level = 0

        for item, level in zip(item_list[1:], item_level[1:]):
            if level > last_level + 2:
                raise ValueError('Sub list level change cannot be > 1.')
            level -= 1  # Convert to zero-based indexing
            if level > last_level:
                open_sublevels(list_array, last_level, level)
            elif level < last_level:
                close_sublevels(list_array, last_level, level)

            # now that we are at the proper level, add the item.
            list_array[level].setAttribute('stylename', liststyle)
            list_item = ListItem()
            para = Paragraph(text=f'{item}')
            list_item.addElement(para)
            list_array[level].addElement(list_item)
            last_level = level

        # Close off any remaining open lists
        for level_count in range(last_level, 0, -1):
            list_array[level_count-1].childNodes[-1].addElement(list_array[level_count])

        # Add the list to the document
        self.doc.text.addElement(list_array[0])


    def addbulletedlist(self, item_list: ListType[Any]) -> None: # Helper function
        """
        Add a bulleted list to `.odt` document.

        See `addlist` for further options.

        Parameters
        ----------
        item_list : List[Any]
            A list of objects representing the items to be included in the list.

        Returns
        -------
        None

        """
        self.addlist(item_list=item_list,
                     item_level = None,
                     list_style = 'bullet')

    def addnumberedlist(self, item_list: ListType[Any]): # Helper function
        """
        Add a numbered list to `.odt` document.

        See `addlist` for further options.

        Parameters
        ----------
        item_list : List[Any]
            A list of objects representing the items to be included in the list.

        Returns
        -------
        None

        """
        self.addlist(item_list=item_list,
                     item_level = None,
                     list_style = 'number')

    def save(self):
        """
        Save file

        Returns
        -------
        None.

        """
        self.doc.save(self.filename)

    def close(self):
        """
        Save and close file

        Returns
        -------
        None.

        """
        self.doc.save(self.filename)
        self.doc = None

    def __del__(self):
        if hasattr(self, 'doc'): # .close() has not been called
            self.doc.save(self.filename)  # last thing to do is write the file.
