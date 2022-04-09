#!/usr/bin/env python
from pandocfilters import toJSONFilter, stringify, RawInline, RawBlock, Span
import pypandoc
import re
import json
from datetime import datetime

n = -1

AUTHOR='Anonymous'
INCL_META=True


def comment(k, v, fmt, meta):

    if fmt in ['docx', 'json'] and k.startswith('Raw'):
        return md_to_docx(text=v[1], inline=k=='RawInline')

    if fmt in ['markdown', 'json'] and k == 'Span':
        return docx_to_md(text=v)

    if fmt in ['markdown'] and k.startswith('Raw'):
        meta_comment = md_to_md(v[1])
        if meta_comment is None:
            return None
        elif k == 'RawInline':
            return RawInline('html', meta_comment)
        elif k == 'RawBlock':
            return RawBlock('html', meta_comment)


def md_to_docx(text, inline=False):
    date_str = datetime.utcnow().isoformat()[:-7] + 'Z'
    match = re.match(r'<!-- a\:(.+?)\|d\:(.+?)\|(.+(|(?:\n.+)+)) -->', text)
    if match is None:
        match = re.match(r'<!-- (.+(|(?:\n.+)+)) -->', text)
        if match is None: return None
        author = AUTHOR
        comment = match.group(1)
    else:
        author = match.group(1)
        date_str = match.group(2)
        comment = match.group(3)
    comment_blocks = json.loads(pypandoc.convert_text(comment,to='json',format='markdown'))['blocks'][0]['c']
    out = {
        "t": "Para",
        "c": [
            {
                "t": "Span",
                "c": [
                    [
                        comment_id(inc=True),
                        ["comment-start"],
                        [
                            ["author", author],
                            ["date",date_str]
                        ]
                    ],
                   comment_blocks
                ]
            },
            {
                "t": "Space"
            },
            {
                "t": "Span",
                "c": [
                    [
                        comment_id(),
                        [
                            "comment-end"
                        ],
                        []
                    ],
                    []
                ]
            }
        ]
    }

    return out if not inline else out['c']

def docx_to_md(text):
    if text[0][1][0] == 'comment-start':
        author = text[0][2][1][1]
        date_str = text[0][2][2][1]
        if INCL_META:
            comment = f'<!-- a:{author}|d:{date_str}|{stringify(text[1])} -->'
        else:
            comment = f'<!-- {stringify(text[1])} -->'
        return RawInline('html', comment)

    # elif text[0][1][0] != 'comment-end':
    #     return Span(*text)

    else:
        return []

def md_to_md(text):
    date_str = datetime.utcnow().isoformat()[:-7] + 'Z'
    match = re.match(r'<!-- a\:(.+?)\|d\:(.+?)\|(.+(|(?:\n.+)+)) -->', text)
    if match is None:
        match = re.match(r'<!-- (.+(|(?:\n.+)+)) -->', text)
        if match is not None:
            return f'{text[:5]}a:{AUTHOR}|d:{date_str}|{text[5:]}'
    return None

def comment_id(inc=False, dec=False):
    global n
    if inc: n+=1
    if dec: n-=1
    return str(n)

if __name__ == "__main__":
    toJSONFilter(comment)
