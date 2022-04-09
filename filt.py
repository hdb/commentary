#!/usr/bin/env python
from pandocfilters import toJSONFilter, stringify, RawInline, Span
import re
import json
from datetime import datetime


import pypandoc

n = -1

AUTHOR='Anonymous'


def comment(k, v, fmt, meta):

    if fmt in ['docx', 'json'] and k.startswith('Raw'):
        date_str = datetime.utcnow().isoformat()[:-7] + 'Z'
        return md_to_docx(v[1], date_str, inline=k=='RawInline')

    if fmt in ['markdown', 'json'] and k == 'Span':
        return docx_to_md(v)


def md_to_docx(text, date_str, inline=False):
    match = re.match(r'<!-- (.+(|(?:\n.+)+)) -->', text)
    if match is None: return None
    comment = match.group(1)
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
                            ["author", AUTHOR],
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
        comment = f'<!-- {stringify(text[1])} -->'
        return RawInline('html', comment)
    
    # elif text[0][1][0] != 'comment-end':
    #     return Span(*text)

    else:
        return []


def comment_id(inc=False, dec=False):
    global n
    if inc: n+=1
    if dec: n-=1
    return str(n)

if __name__ == "__main__":
    toJSONFilter(comment)
