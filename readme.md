# Commentary

Commentary is a command line document conversion tool that preserves native-style comments and tracked-changes between Markdown and MS Word. It uses Pandoc to convert between file types, Git to track document changes, and RegEx to translate comments, insertions and deletions to appropriate style.

The goal of this project is to facilitate an entirely Markdown workflow with docx editing, annotation and collaboration capabilities comparable to Word.

## Requirements

- [Python 3](https://www.python.org/downloads/)
- [Git](https://git-scm.com/) (optional; required for track changes)
- [Pandoc](https://pandoc.org/)

## Installation

```
git clone git@github.com:hdbhdb/commentary.git
cd commentary
pip install -r requirements.txt
```

PyPI package is forthcoming.

## Usage

```
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
  -t, --track-changes   include tracked changes in addition to comments. file
                        must be tracked by git repo for this option to work.
                        [experimental]
  -p, --print           print results to terminal
  -D, --force-docx-comments
                        force conversion to docx-style comments during md -->
                        md conversion. default is to use markdown-style
                        comments
  -A [DEFAULT_AUTHOR], --default-author [DEFAULT_AUTHOR]
                        configure default name to appear in docx comments

```

## Configuration

Use `-A 'AUTHOR NAME'` to save the default comment author name to `~/.commentary-conf.yaml`.

## Converting Comments

Commentary handles comments well in most cases. Docx comments which highlight areas spanning multiple paragraphs may fail, however.

Using the `-m` flag, Commentary will save docx comment metadata within markdown html comment tags. For markdown-to-docx conversions, Commentary will re-convert these comments to docx with their original author and time-stamp metadata.

## Tracking Changes

With the `-t` flag, Commentary can turn git diffs into docx-formatted tracked-changes, though this feature is still experimental and fails in some complex use cases. In order to use this feature, the input file must be tracked by `git`. If the input file has any uncommitted changes, Commentary will diff the current file against the last commit. If there are no uncommitted changes, Commentary will diff between the last two commits.
