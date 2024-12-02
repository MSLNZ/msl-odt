# msl-odt

[![Tests Status](https://github.com/MSLNZ/msl-odt/actions/workflows/tests.yml/badge.svg)](https://github.com/MSLNZ/msl-odt/actions/workflows/tests.yml)
[![Docs Status](https://github.com/MSLNZ/msl-odt/actions/workflows/docs.yml/badge.svg)](https://github.com/MSLNZ/msl-odt/actions/workflows/docs.yml)

## Overview

`msl-odt` is a Python module for creating and modifying Open Document Text (.odt) files. It provides an interface for adding formatted text, tables, lists, equations, images, and other elements to an ODT document. The module uses the `odfpy` library for Open Document file manipulation and aims to follow PEP8 conventions.

## Features

- **Add Text and Headings:** Supports adding paragraphs, heading levels 1 and 2, and handling special characters like `\t` and `\n`.
- **Hyperlink Detection:** Automatically converts URLs (starting with `http://` or `https://`) in text to hyperlinks.
- **Page Breaks:** Insert page breaks for document formatting.
- **Table Support:** Allows creating tables with customisable column widths, table widths, borders, and optional captions.
- **Figure support:** Supports adding images with specified dimensions and optional captions.
- **Hierarchical Lists:** Add bulleted or numbered lists with optional hierarchical levels for nested lists.
- **Equation Support:** Add equations using Star Math 5.0 notation, with options for setting frame size and text wrapping.


## Installation

`msl-odt` is available for installation via the [Python Package Index](https://pypi.org/) and may be installed with [pip](https://pip.pypa.io/en/stable/)

To install the module, using `pip`:

```console
pip install odfpy
```

## Examples
Examples on how to use the code are available in the `msl-odt` [repository](https://github.com/MSLNZ/msl-odt/tree/main/src/msl/examples/odt) and these examples are also included with the `msl-odt` installation in the `../site-packages/msl/examples/msl-odt` directory of your Python interpreter.

The examples are provided as `Python` to allow users to cut-and-paste into their own code.