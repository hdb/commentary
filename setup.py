from setuptools import setup

with open("readme.md", "r") as fh:
    long_description = fh.read()

exec(open('commentary/version.py').read())

setup(
    name='commentary',
    version=__version__,
    description='comment-preserving docx <-- --> markdown converter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hdb/commentary",
    author='Hudson Bailey',
    author_email='hudsondiggsbailey@gmail.com',
    license='MIT',
    packages=['commentary'],
    package_data = {
        'commentary': ['data/*.json']
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'pypandoc>=1.4',
        'pandocfilters==1.5.0'
    ],
    scripts=[
        'bin/commentary',
        'filter/commentary-filter'
    ]
)
