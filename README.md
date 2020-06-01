# WikiPub - Wikipedia to ePub

Stuck at home, library's closed, and a kid who loves to read running out of books...what to do? How about an e-book with curated articles from Wikipedia.

This is a script I threw together to turn a list of Wikipedia articles into an ePub file that can then be loaded into your favorite eReader. It is built on a couple excellent Python modules with some additional code for processing a configuration file to define the book's content.

## Installation

Currently the best installation method is to clone the repository and use [Poetry](https://python-poetry.org/) to create a virtual environment and install the required modules.

```
git clone https://github.com/akehrer/wikipub.git

cd wikipub

poetry install

poetry shell
```

## Usage

To use the script pass a TOML based definition file (see below) as the only argument and watch your book get made.

```
python wikipub.py example.toml
```

Some optional arguments are available to override the default behavior:

```
  -o OUTPUT, --output OUTPUT
                        File name and path to save ePub file.
  -t TITLE, --title TITLE
                        Alternate title to use for the file name instead of
                        the one defined in the configuration file. This does
                        not overide the 'output' option
```

Unless an output location is specified, the finished book will be saved in the same location as the definition file.

## Book Definition File

The definition file is a [TOML](https://github.com/toml-lang/toml) configuration file with the following sections.

### Book Section
```
[book]
title = "Radio Controlled Vehicles"
author = "Wikimedia Foundation, Inc."
cover_image_url = "https://upload.wikimedia.org/wikipedia/commons/c/c7/Hyper8.jpg"
```

The `title` and `author` values are required with the `title` value also being used to define the file name of the output file (unless overridden). The `cover_image_url` value is optional and will be used to add a cover image to the book.

### Chapters Sections
```
[[chapters]]
title = "Radio Control"

[[chapters]]
title = "Radio-controlled model"

[[chapters]]
title = "Radio-controlled aircraft"

...
```

One or more `chapters` section should be included to define the Wikipedia articles to use for each chapter in the book. Each chapter is defined by the `title` value of the Wikipedia article.

See the included `example.toml` file for an example book definition file.

## Kindle?

This script currently does not output Amazon Kindle files (.mobi) but the ePub files it makes can easily be converted to Kindle using [Calibre](https://calibre-ebook.com/).

## Thanks

Thanks to the following Python modules and authors for making this insanely easy.

- [wikipedia-api](https://github.com/martin-majlis/Wikipedia-API)
- [ebooklib](https://github.com/aerkalov/ebooklib)

## Alternatives

- [Wikipedia Book Creator](https://en.wikipedia.org/wiki/Help:Books) - This service provided by Wikipedia makes collecting articles into a book easy but currently does not have a good export to ePub option.
- [MediaWiki to LaTeX](http://mediawiki2latex.wmflabs.org/) - This service says it will convert a Wikipedia book to a pdf file, but I was not able to get it to work for me either through the web interface or a local Ubuntu installation.

## Contribute

Bug reports, pull requests, and all other contributions are welcome!
