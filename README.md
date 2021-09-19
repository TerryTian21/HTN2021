# Welcome to our HTN2021 Project

This projects aims to translate hand written characters into text files. Scryber lets you write directly into the program with a tablet, or use your mouse to write notes, and have the program auto-translate your writing into text. The application can either be run vai the executable file within the Scryber.zip folder linked below, or via the source code. The source code will allow you to run the program as well, but in order to run the program, Tesseract must be installed (both through pip and separately onto the disk.)

## Usage

### Using Executable
In order to use Scryber, download and extract the Scryber.zip file from https://drive.google.com/drive/folders/1wZBe4-HJhIwxhaYyQj5WV20jxI_jX7E_?usp=sharing.

### Using Source
In order to use the source code, Tesseract needs to be installed: go to https://digi.bib.uni-mannheim.de/tesseract/ and find the appropriate version for your operating system.
For windows 64-bit, install: tesseract-ocr-w64-setup-v4.1.0.20190314.exe

After installing, edit the ui.py file and set `pytesseract.pytesseract.tesseract_cmd` equal to the absolute path to the tesseract.exe file within the installation.

Finally, the dependancies can be installed using the requirements.txt file.
