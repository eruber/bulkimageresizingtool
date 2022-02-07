# Bulk Image Resizing Tool (BIRT) #

**BIRT** is a command line utility useful for re-sizing many image files that reside in the same directory.

# Dependencies #

**Python** (3.9.0) - implementation language -- [python info.](https://www.python.org/ "Python Information")

**Click** (8.0.3)  - manages the command line interface -- [click info.](https://palletsprojects.com/p/click/ "Click Information")

**Pillow** (9.0.1) - manages image processing -- [pillow info.](https://pillow.readthedocs.io/en/stable/index.html "Pillow Information")


# Installation #

**BIRT** is distributed using [setuptools](https://pypi.org/project/setuptools/) so it is easy to configure a virtual environment, install birt, and execute it.

For example, on Windows, when the current directory is contains the **BIRT setup.py** file a developer who wishes to modify the source would do

       > python -m venv BIRT_VENV
       > BIRT_VENV/Scripts/activate
       > pip install --editable .
       > birt --help
 
On Linux when the current directory is contains the **BIRT setup.py** file a developer who wishes to modify the source would do

       $ virtualenv BIRT_VENV
       $ . BIRT_VENV/bin/activate
       $ pip install --editable .
       $ birt --help

To install **BIRT** to use and not edit the source code, on Windows after downloading the zip file archive
and unarchiving it do

		cd bulkimageresizingtool
		python -m venv BIRT_VEN
		BIRT_VENV/Scripts/activate
		pip install .
		birt --help
	

# USAGE #

The form of the **BIRT** command line looks like this

	birt [OPTIONS] PATH WIDTH HEIGHT
	
	  Resize images in PATH to a size that is limited to (WIDTH, HEIGHT).
	
	  By default the resized image files will be created in a sub-directory 
	  of PATH named "resized". Use the --subdir SUBDIR option to change the 
	  default name of this sub-directory.
	
	Options:
	
	  --subdir SUBDIR
		Create resized images in SUBDIR with the same file names. Default: "resized"
	
	  -v, --verbose
		Enable verbose output, this is shorthand for --logging_level=DEBUG
	
	  -q, --quiet
		Enable quiet output, this is shorthand for --logging_level=ERROR
	
	  --logging-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]
		Fine tune output by setting logging level
	
	  -t, --test
		Test Mode, do not process images, just emit what would be done.
	
	  -h, --help
		Show this help message and exit.

# MIT License #
Copyright 2022 E.R. Uber (eruber@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of
the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

06 Feb 2022 7:09 PM

# Author #
E.R. Uber (eruber@gmail.com)

# Created #
06 Feb 2022 7:09 PM

# Credits #
A few posts on [Stackoverflow](https://stackoverflow.com/) were helpful in understanding how EXIF metadata embedded
in image files can contain camera orientation information. The details of these
posts are contained in the source code.


