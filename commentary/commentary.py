#!/usr/bin/env python3

import argparse
import pypandoc
import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'data/commentary_conf.json')
FILTER_PATH = os.path.join(os.path.dirname(__file__), 'commentary_filter.py')

def parse():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        prog='commentary',
        description='comment-preserving docx-markdown converter',
        )

    parser.add_argument('input', nargs='?', default=None, help='input')
    parser.add_argument('-o', '--output', nargs='?', default=None, help='ouput filename. supports docx and txt/md')
    parser.add_argument('-a', '--author', nargs='?', default=None, help='configure default name to use for comments')
    parser.add_argument('-m', '--toggle-metadata', action='store_true', help='toggle whether comment metadata is used for markdown comments')
    parser.add_argument('-p', '--print', action='store_true', help='print results to terminal')
    parser.add_argument('--pandoc-args', nargs='*', default=[], help='Other pandoc arguments to include in document conversion')

    # TODO: add ability to configure default extra pandoc settings

    args = parser.parse_args()
    return args

def configure_author(author):
    """Configure default comments author in ~/.config/commentary.yaml."""

    return edit_config({'author':author})['author']

def toggle_meta():
    """Toggle whether or not metadata is included in meta"""

    conf = edit_config({})
    return edit_config({'include_metadata': not conf['include_metadata']})['include_metadata']

def edit_config(data):
    """Edit configuration in data/commentary_conf.json"""

    with open(CONFIG_PATH, 'r') as f:
        conf = json.load(f)
    if len(data) > 0:
        for k,v in data.items():
            conf[k] = v
        with open(CONFIG_PATH, 'w') as f:
            json.dump(conf,f, indent=4)
    return conf

def main():
    args = parse()

    markdown_exts = ['txt', 'md', 'markdown', 'mdown', 'mkdn', 'mkd', 'mdwn', 'mkdown']

    if args.author is not None:
        author = configure_author(args.author)
        print(f'author was set to "{author}"')
        if args.input is None: exit()
    
    if args.toggle_metadata:
        status = toggle_meta()
        print(f'include_metadata was set to {status}')
        if args.input is None: exit()
    
    if args.output is not None:
        output_format = os.path.splitext(os.path.basename(args.output))[1][1:]
        out_format_name = 'docx' if output_format == 'docx' else 'markdown' if output_format in markdown_exts else None
    else:
        out_format_name = 'markdown'


    out = pypandoc.convert_file(
        args.input, 
        to=out_format_name, 
        outputfile=args.output, 
        filters=FILTER_PATH, 
        extra_args=[
            '--wrap=none',
            '--track-changes=all',
            *[f'--{a}' for a in args.pandoc_args]
        ]
    )

    if args.output is None or args.print:
        print(out)

if __name__ == '__main__':
    main()
