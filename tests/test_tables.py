"""
Test Module for Open Document (.odt) Tables example

This module contains tests to ensure that the Open Document files generated by
the `example_msl-odt_tables.py` script match the expected output file,
`example_msl-odt_tables.odt`, located in the `expected_outputs` directory.

The tests focus on the following aspects:
- The correct creation of `example_msl-odt_tables.odt` by running the
  `example_msl-odt_tables.py` script.
- Comparison of table number between generated and expected files.
- Comparison of table dimensions and cell content.

Setup Process:
--------------
The test module utilizes a pytest fixture to run the
`example_msl-odt_tables.py` script before any tests are executed.
This fixture:
- Runs the script to create `example_msl-odt_tables.odt`
  in the same directory as the script.
- Ensures the file has been created successfully.
- Cleans up by deleting the generated `example_msl-odt_tables.odt`
  after all tests have run.

Test Cases:
-----------
- test_table_elements_count: Asserts that the number of table elements in the
  generated and expected files are the same.
- test_table_dimensions: Checks that tables have the expected row and column
  counts.
- test_table_cell_content: Validates the content of specific cells against
  expected values.

Usage:
------
Run the tests using pytest:
```bash
pytest path/to/your/test_file.py
"""

import subprocess
from pathlib import Path
from inspect import currentframe
from os import environ
from odf.opendocument import load
from odf.text import P as Paragraph  # pylint: disable=no-name-in-module
from odf.table import Table, TableRow, TableCell
import pytest

# Directory paths
BASE_DIR = Path(__file__).resolve().parent
SCRIPT_DIR = BASE_DIR / "../src/msl/examples/odt"
EXPECTED_OUTPUTS_DIR = BASE_DIR / "expected_outputs"
SCRIPT_FILE = SCRIPT_DIR / "example_msl-odt_tables.py"
TEST_FILE = SCRIPT_DIR / "example_msl-odt_tables.odt"
EXPECTED_FILE = EXPECTED_OUTPUTS_DIR / "example_msl-odt_tables.odt"


@pytest.fixture(scope="module", autouse=True)
def setup_test_file():
    """Run the example_msl-odt_tables.py script and create test file."""
    cleanup = True  # Delete created .odt files when finished

    try:
        env = environ.copy()
        env["PYTHONPATH"] = str(Path(__file__).resolve().parent.parent / "src")
        subprocess.run(
            ["python", str(SCRIPT_FILE)],
            cwd=str(SCRIPT_DIR),
            env=env,
            check=True,
            text=True,
            capture_output=True
        )
    except subprocess.CalledProcessError as e:
        print("Subprocess failed with return code:", e.returncode)
        print("Output:", e.output)
        print("Error:", e.stderr)
        raise

    assert TEST_FILE.exists(), f"{TEST_FILE} does not exist."
    yield  # Cleanup occurs after all tests

    if TEST_FILE.exists() and cleanup:
        TEST_FILE.unlink()  # Delete the test file


def test_table_elements_count():
    """Test if the number of tables in the generated file matches the expected file."""
    test = currentframe().f_code.co_name
    if not TEST_FILE.exists():
        pytest.skip(f"Skipping {test}: test file not found.")
    if not EXPECTED_FILE.exists():
        pytest.skip(f"Skipping {test}: golden file not found.")

    doc1 = load(TEST_FILE)
    doc2 = load(EXPECTED_FILE)

    num_table1 = len(doc1.getElementsByType(Table))
    num_table2 = len(doc2.getElementsByType(Table))
    assert num_table1 == num_table2, (
        f"Different numbers of Tables. Test: {num_table1} != Expected: {num_table2}"
    )


def test_table_dimensions():
    """Test if the dimensions of tables in the generated file match the expected file."""
    test = currentframe().f_code.co_name
    if not TEST_FILE.exists() or not EXPECTED_FILE.exists():
        pytest.skip(f"Skipping {test}: test or expected file not found.")

    doc1 = load(TEST_FILE)
    doc2 = load(EXPECTED_FILE)

    tables1 = doc1.getElementsByType(Table)
    tables2 = doc2.getElementsByType(Table)

    assert len(tables1) == len(tables2), (
        "Number of tables do not match between test and expected files."
    )

    for table_index, (table1, table2) in enumerate(zip(tables1, tables2)):
        num_rows1 = len(table1.getElementsByType(TableRow))
        num_rows2 = len(table2.getElementsByType(TableRow))
        assert num_rows1 == num_rows2, (
            f"Row count mismatch in Table {table_index + 1}. "
            f"Test: {num_rows1} != Expected: {num_rows2}."
        )

        for row_index, (row1, row2) in enumerate(zip(
            table1.getElementsByType(TableRow),
            table2.getElementsByType(TableRow))
        ):
            num_cells1 = len(row1.getElementsByType(TableCell))
            num_cells2 = len(row2.getElementsByType(TableCell))
            assert num_cells1 == num_cells2, (
                f"Column count mismatch in Table {table_index + 1}, Row {row_index + 1}. "
                f"Test: {num_cells1} != Expected: {num_cells2}."
            )


def test_table_cell_content():
    """Test if the cell content in tables matches between the generated file and expected file."""
    if not TEST_FILE.exists() or not EXPECTED_FILE.exists():
        pytest.skip(f"Skipping {currentframe().f_code.co_name}: "
                    "test or expected file not found.")

    # Load both documents
    doc1 = load(TEST_FILE)
    doc2 = load(EXPECTED_FILE)

    # Get tables from each document
    for table_index, (table1, table2) in enumerate(
        zip(doc1.getElementsByType(Table),
            doc2.getElementsByType(Table)), start=1
    ):
        for row_index, (row1, row2) in enumerate(
            zip(table1.getElementsByType(TableRow),
                table2.getElementsByType(TableRow)), start=1
        ):
            cells1, cells2 = row1.getElementsByType(
                TableCell), row2.getElementsByType(TableCell)

            assert len(cells1) == len(cells2), (
                f"Column count mismatch in table {table_index}, row {row_index}. "
                f"Test: {len(cells1)} != Expected: {len(cells2)}"
            )

            # Directly compare text content of each cell
            for col_index, (cell1, cell2) in enumerate(zip(cells1, cells2), start=1):
                # Extract text from the Paragraph element within each ListItem
                # Extract text by joining the data from text nodes
                text1 = ''.join(
                    node.data for node in \
                        cell1.getElementsByType(Paragraph)[0].childNodes \
                        if node.nodeType == node.TEXT_NODE) \
                    if cell1.getElementsByType(Paragraph) else ""
                text2 = ''.join(
                    node.data for node in \
                        cell2.getElementsByType(Paragraph)[0].childNodes \
                        if node.nodeType == node.TEXT_NODE) \
                    if cell2.getElementsByType(Paragraph) else ""

                # Print the contents of the table cells for debugging
                print(f"Comparing cell at Table{table_index}"
                      f"({row_index}, {col_index}). "
                      f"Test: '{text1}' | Expected: '{text2}'")
                assert text1 == text2, (
                    f"Cell content mismatch at table {table_index}, row {row_index}, "
                    f"column {col_index}. Test: '{text1}' != Expected: '{text2}'"
                )
