# Commentary

Commentary is a command line document conversion tool and pandoc filter that preserves native-style comments between Markdown and docx files.

## Installation

```bash
pip install commentary
```

## Basic Usage

```bash

echo 'Hello <!-- this is a comment --> world' > doc.md

# convert from md to docx using the CLI
commentary doc.md -o out.docx

# or invoke as a filter from pandoc
pandoc doc.md -F commentary-filter --wrap=none -o out.docx

# add metadata to your markdown comments
commentary doc.md -o doc.md

```

See [documentation](https://commentary.readthedocs.io/en/latest/usage.html) for full usage guide.
