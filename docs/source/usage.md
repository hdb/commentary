# Usage

```Python console
usage: commentary [-h] [-o [OUTPUT]] [-a [AUTHOR]] [-m] [-p] [--pandoc-args [PANDOC_ARGS [PANDOC_ARGS ...]]] [input]

comment-preserving docx-markdown converter

positional arguments:
  input                 input

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTPUT], --output [OUTPUT]
                        ouput filename. supports docx and txt/md
  -a [AUTHOR], --author [AUTHOR]
                        configure default name to use for comments
  -m, --toggle-metadata
                        toggle whether comment metadata is used for markdown comments
  -p, --print           print results to terminal
  --pandoc-args [PANDOC_ARGS [PANDOC_ARGS ...]]
                        Other pandoc arguments to include in document conversion

```

## Metadata

By default commentary uses will save author and timestamp metadata within markdown html comment tags using the following format:

```html
<!-- a:Anonymous|d:2022-04-10T00:07:46Z|this is a comment -->
```

Commentary will re-convert these comments to docx with their original author and time-stamp metadata. This allows comment timestamps and author data to be preserved between multiple docx/markdown conversions.

This feature can be toggled off/on using the `-m` flag.

## Configuring Author Name

Use `-a '{name}'` to save your name to `data/commentary_conf.json`. This name will appear on markdown and docx comments that you author.

## Filter Usage

commentary is driven by pandoc filters. You can invoke `commentary-filter` directly in your pandoc workflow:

```bash
echo 'Hello <!-- this is a comment --> world' > doc.md

pandoc doc.md -F commentary-filter --wrap=none --to=markdown
```

The comment author for the filter can be configured using:

```bash
commentary -a '{name}'
```