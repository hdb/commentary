#!/usr/bin/env python
from pandocfilters import toJSONFilter, stringify, RawInline, RawBlock, Span
import pypandoc
import re
import json
from datetime import datetime
import os


comment_id_counter = -1

try:
    with open(os.path.join(os.path.dirname(__file__), 'data/commentary_conf.json'), 'r') as p:
        CONFIG = json.load(p)

    AUTHOR = CONFIG['author'] #                 name of author to use for newly added comments

    INCL_META = CONFIG['include_metadata'] #        append metadata to markdown inline html data

    #                                           example:
    #                                           <!-- a:Author Name|d:2022-04-09T20:34:18Z|Here is the comment -->

except:
    AUTHOR, INCL_META ='Anonymous', True



def filter_handler(k, v, fmt, meta):
    """Direct conversion function based on document and element type"""

    if fmt in ['docx'] and k.startswith('Raw'):
        return md_to_docx(text=v[1], inline=k=='RawInline')

    if fmt in ['markdown'] and k == 'Span':
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
    """Convert markdown inline HTML comments to docx comments"""

    date_str = datetime.utcnow().isoformat()[:-7] + 'Z'
    match = re.match(r'<!-- a\:(.+?)\|d\:(.+?)\|(.+(|(?:\n.+)+)) -->', text) # match for metadata comments
    if match is None:
        match = re.match(r'<!-- (.+(|(?:\n.+)+)) -->', text) # general commment match
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
                        "",
                        ["comment-start"],
                        [
                            ["id", comment_id(inc=True)],
                            ["author", author],
                            ["date",date_str],
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
                        "",
                        ["comment-end"],
                        [
                            ["id", comment_id()]
                        ]
                    ],
                    []
                ]
            }
        ]
    }

    return out if not inline else out['c']

def docx_to_md(text):
    """Convert docx comments to markdown inline HTML comments"""

    if text[0][1][0] == 'comment-start':
        author = text[0][2][1][1]
        date_str = text[0][2][2][1]
        if INCL_META:
            comment = f'<!-- a:{author}|d:{date_str}|{stringify(text[1])} -->' # include metadata
        else:
            comment = f'<!-- {stringify(text[1])} -->'
        return RawInline('html', comment)

    # ignore all other span elements
    # elif text[0][1][0] != 'comment-end':
    #     return Span(*text)

    else:
        return []

def md_to_md(text):
    """Add author and timestamp metadata to markdown comments"""

    date_str = datetime.utcnow().isoformat()[:-7] + 'Z'
    match = re.match(r'<!-- a\:(.+?)\|d\:(.+?)\|(.+(|(?:\n.+)+)) -->', text)
    if match is None:
        match = re.match(r'<!-- (.+(|(?:\n.+)+)) -->', text)
        if match is not None:
            return f'{text[:5]}a:{AUTHOR}|d:{date_str}|{text[5:]}'
    return None

def comment_id(inc=False, dec=False):
    """Increment or decrement comment id counter"""

    global comment_id_counter
    if inc: comment_id_counter+=1
    if dec: comment_id_counter-=1
    return str(comment_id_counter)

def main():
    toJSONFilter(filter_handler)

if __name__ == "__main__":
    main()
