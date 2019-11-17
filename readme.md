# Commentary

Commentary is a command line document conversion tool that preserves native-style comment formatting between Markdown and MS Word.

Create fully marked-up docx files in Markdown without having to touch Word.

## Requirements

- Python 3
- Pandoc
- Pypandoc

## Installation

```
git clone git@github.com:hdbhdb/commentary.git
cd commentary
pip install -r requirements.txt
```

PyPI package is forthcoming.

## Usage

```
usage: commentary [-h] [-o [OUTPUT]] [-a [AUTHOR]] [-A [DEFAULT_AUTHOR]] [-p]
                  [-D]
                  [input]

comment-preserving docx-markdown converter

positional arguments:
  input                 input

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTPUT], --output [OUTPUT]
                        ouput filename. supports docx and txt/md
  -a [AUTHOR], --author [AUTHOR]
                        name to appear in docx comments
  -A [DEFAULT_AUTHOR], --default-author [DEFAULT_AUTHOR]
                        configure default name to appear in docx comments
  -p, --print           print results to terminal
  -D, --force-docx-comments
                        force conversion to docx-style comments during md -->
                        md conversion. default is to use markdown-style
                        comments
```
