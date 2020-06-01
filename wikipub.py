# WikiPub - Convert Wikipedia to ePub
# Copyright (C) 2020 Aaron Kehrer
# 
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License 
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License along with this program. 
# If not, see <https://www.gnu.org/licenses/>.


import sys
import argparse
from pathlib import Path

import requests
import toml
import wikipediaapi

from ebooklib import epub

wiki = wikipediaapi.Wikipedia("en", extract_format=wikipediaapi.ExtractFormat.HTML)

book = epub.EpubBook()

parser = argparse.ArgumentParser()
parser.add_argument(
    "conf",
    help="Path to TOML book configuration file to use. The ouput file will share the same name and location unless otherwise specified.",
    type=str,
)
parser.add_argument(
    "-o", "--output", help="File name and path to save ePub file.", type=str
)
parser.add_argument(
    "-t",
    "--title",
    help="Alternate title to use for the file name instead of the one defined in the configuration file. This does not overide the 'output' option",
    type=str,
)


def load_conf(path: Path) -> dict:
    conf = {}
    with Path("book.toml").open() as fp:
        conf = toml.load(fp)
    return conf


def make_epub(conf: dict, out: Path):
    b_title = conf["book"]["title"]
    book.set_identifier(b_title.lower().replace(" ", "-"))
    book.set_title(b_title)
    book.set_language("en")
    book.add_author(conf["book"]["author"])
    book.add_metadata("DC", "creator", "Created with wikipub")

    if "cover_image_url" in conf["book"]:
        url = conf["book"]["cover_image_url"]
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            img_path = url.split("/")[-1]
            book.set_cover(img_path, r.content)

    book.spine.append("nav")

    for idx, chapter in enumerate(conf["chapters"]):
        page = wiki.page(chapter["title"])
        if page.exists():
            c_title = chapter["title"]
            print(f"Processing: {c_title}")
            c_title_stub = c_title.lower().replace(" ", "-")
            f_name = f"{idx:03}_{c_title_stub}.xhtml"
            e_ch = epub.EpubHtml(title=c_title, file_name=f_name)
            e_ch.set_content(page.text)
            book.add_item(e_ch)
            book.spine.append(e_ch)
            book.toc.append(e_ch)

    # Finish off the book
    print("Finishing...")
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Save the book
    print("Saving...")
    epub.write_epub(out, book)
    print(f"Saved as: {out}")


if __name__ == "__main__":
    args = parser.parse_args()
    conf_path = Path(args.conf)
    if not conf_path.exists():
        print(f'error: no file at "{args.conf}"')
        sys.exit(1)
    else:
        try:
            conf = load_conf(conf_path)
        except Exception as e:
            print(f"error: {e}")
            sys.exit(1)

    if args.title is not None:
        out_path = Path(conf_path.parent / f"{args.title}.epub")
    elif args.output is not None:
        out_path = Path(args.output)
    else:
        out_path = Path(conf_path.parent / f"{conf['book']['title']}.epub")

    make_epub(conf, out_path)
