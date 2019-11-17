#!/usr/bin/python3

import re
import datetime
import argparse
import pypandoc
import os
import string
from random import choice
from pathlib import Path
import yaml

def parse():

    parser = argparse.ArgumentParser(
        prog='commentary',
        description='comment-preserving docx-markdown converter',
        )

    parser.add_argument('input', nargs='?', default=None, help='input')
    parser.add_argument('-o', '--output', nargs='?', default=None, help='ouput filename. supports docx and txt/md')
    parser.add_argument('-a', '--author', nargs='?', default=None, help='name to appear in docx comments')
    parser.add_argument('-A', '--default-author', nargs='?', default=None, help='configure default name to appear in docx comments')
    parser.add_argument('-p', '--print', action='store_true', help='print results to terminal')
    parser.add_argument('-D', '--force-docx-comments', action='store_true', help='force conversion to docx-style comments during md --> md conversion. default is to use markdown-style comments')  

    # TODO: add ability to configure default extra pandoc settings

    args = parser.parse_args()
    return args

def markdown2word(input, author):

    with open(input, 'r') as file:
        text = file.read()

    date_str = datetime.datetime.utcnow().isoformat()[:-7] + 'Z'
    comment_id_placeholder = "".join(choice(string.ascii_letters + string.punctuation + string.digits) for x in range(10))

    sub1 = re.sub(r'(.|\n)<!-- (.+(|(?:\n.+)+)) -->',
        r'[\2]{.comment-start id="'+comment_id_placeholder+'" author="'+author+'" date="'+date_str+'"}\1[]{.comment-end id="'+comment_id_placeholder+'"}',
        text,flags=re.MULTILINE) # this is cutting a character

    sub2 = sub1
    comment_ids = {'start': iter(range(1000)), 'end': iter(range(1000))} # assumes less than 1000 comments in a given document
    for i in range(sub1.count('comment-start id')):
        for x in comment_ids:
            sub2 = sub2.replace('.comment-'+x+' id="'+comment_id_placeholder+'"','.comment-'+x+' id="'+str(next(comment_ids[x]))+'"', 1)

    # TODO: add a catch for forward slash added by pandoc if .md document was created through pandoc and not commentary (i.e., '...}words\[]{...')
    
    # TODO: address the loss of author/timestamp metadata for docx's received by others -- could solve by:
    #
    # - keeping initial comments in document and re-calculating comment-id index based on already existing word-style comments; OR
    # - creating optional docx metadata preservation inside of html comments (e.g., <!-- A:Ernest|T:1942-10-15T13:48:00Z|this could be made more concise -->)

    return sub2

def word2markdown(input, input_format):

    if input_format in markdown_files:
        with open(input, 'r') as file:
            rawmd = file.read()
    else:
        rawmd = pypandoc.convert(input, 'markdown', format='docx', extra_args=['--wrap=none','--track-changes=all'])

    sub = re.sub(r'\[(.+)\]\{\.comment-start id="[0-9]*" author=".+" date="[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}\:[0-9]{2}\:[0-9]{2}Z"}(.*?)(\\\[|\[)(\\\]|\]){.comment-end id="[0-9]*"}',
        r'\2 <!-- \1 -->',
        rawmd,flags=re.MULTILINE)

    return sub

def writemd(text, output):

    with open(output, "w") as text_file:
        text_file.write(text)

    return text

def writedocx(text, output):
    
    return pypandoc.convert_text(text, 'docx', format='md', outputfile=output)  # add support for extra_args?

def configureAuthor(author):

    data = {
        'author': author
    }   

    with open(config_file, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)
    
    print('created file: ' + config_file)

    return author

def main():

    args = parse()

    global markdown_files 
    markdown_files = ['txt', 'md', 'markdown', 'mdown', 'mkdn', 'mkd', 'mdwn', 'mkdown']

    global config_file
    config_file = str(Path.home())+"/.commentary-conf.yaml"

    if args.default_author is not None:
        configureAuthor(args.default_author)

    input_format = os.path.splitext(os.path.basename(args.input))[1][1:]

    if args.output is not None:
        output_format = os.path.splitext(os.path.basename(args.output))[1][1:]
    else:
        output_format = None
        
    if input_format in markdown_files and (not output_format in markdown_files or args.force_docx_comments):

        if args.author is None:

            try:
                config = yaml.safe_load(open(config_file))
                author = config['author']

            except:
                author = 'Anonymous'
        else:
            author = args.author


        new_text = markdown2word(args.input, author)

        if args.print:
            print(new_text)
            
            if args.output is None:
                exit()

        output = args.output

        if output_format in markdown_files:
            writemd(new_text, output)

        else:
        
            if args.output is None:
                output_format = 'docx'
                output = os.path.splitext(os.path.basename(args.input))[0]+'.'+output_format

            writedocx(new_text, output)

    else:

        new_text = word2markdown(args.input, input_format)

        if args.print:
            print(new_text)

            if args.output is None:
                exit()

        if args.output is None:
            output_format = 'md'
            output = os.path.splitext(os.path.basename(args.input))[0]+'.'+output_format

        else:
            output = args.output

        writemd(new_text, output)

if __name__ == '__main__':
    main()