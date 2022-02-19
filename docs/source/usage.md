# CLI Usage

```Python console
usage: commentary [-h] [-o [OUTPUT]] [-a [AUTHOR]] [-m] [-t] [-p] [-D]
                  [-A [DEFAULT_AUTHOR]]
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
  -m, --metadata        preserve comment metadata in docx to md conversions
  -p, --print           print results to terminal
  -D, --force-docx-comments
                        force conversion to docx-style comments during md -->
                        md conversion. default is to use markdown-style
                        comments
  -A [DEFAULT_AUTHOR], --default-author [DEFAULT_AUTHOR]
                        configure default name to appear in docx comments

```

## Configuration

Use `-A 'AUTHOR NAME'` to save the default comment author name to `~/.config/commentary.yaml`.

## Comment Metadata

Using the `-m` flag, Commentary will save docx comment metadata within markdown html comment tags. For markdown-to-docx conversions, Commentary will re-convert these comments to docx with their original author and time-stamp metadata.

```{note} docx comments spanning multiple paragraphs may fail to convert correctly to markdown comments.
```