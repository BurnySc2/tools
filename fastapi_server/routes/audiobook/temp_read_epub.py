import io
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path

import nltk  # pyre-fixme[21]
from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT  # pyre-fixme[21]
from ebooklib.epub import EpubHtml, EpubReader, Link, Section  # pyre-fixme[21]
from loguru import logger
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize  # pyre-fixme[21]

nltk.download("punkt")


def extract_sentences(text: str) -> list[str]:
    sentences = sent_tokenize(text)
    return sentences


# def get_chapters(doc: fitz.Document) -> list[tuple[int, str, int]]:
#     # tuple[idk, chapter name, page number]
#     toc = doc.get_toc()
#     return toc


# def get_text_of_chapter(doc: fitz.Document, chapter_number: int) -> list[list[str]]:
#     pages = []
#     for page_number in range(doc.chapter_page_count(chapter_number)):
#         page = doc.load_page((chapter_number, page_number))
#         text = page.get_text()
#         # TODO Keep new line characters?
#         # cleansed_text = re.sub(r"\s+", " ", text)
#         # sentences = extract_sentences(cleansed_text)
#         sentences = extract_sentences(text)
#         if sentences:
#             pages.append(sentences)
#     return pages


@dataclass
class EpubChapter:
    chapter_title: str
    chapter_number: int
    word_count: int
    sentence_count: int
    content: list[str]
    combined_text: str


def extract_chapters(data: io.BytesIO) -> list[EpubChapter]:
    c = EpubReader("")
    c.zf = zipfile.ZipFile(data)
    c._load_container()
    c._load_opf_file()
    prev_text = ""
    chapters = []
    chapter_number = 1

    # pyre-fixme[11]
    def follow_link(chapter: Link | Section):
        nonlocal chapter_number, prev_text
        if isinstance(chapter, list | tuple):
            for section in chapter:
                follow_link(section)
            return
        if isinstance(chapter, Section):
            return
        if not isinstance(chapter, Link):
            logger.info(f"Was type: {type(chapter)}")
            return
        # pyre-fixme[11]
        epub_html: EpubHtml = c.book.get_item_with_href(chapter.href.split("#")[0])
        if epub_html.get_type() != ITEM_DOCUMENT:
            return

        # Parse the HTML content
        soup = BeautifulSoup(epub_html.get_body_content(), "html.parser")

        for span in soup.find_all("span"):
            # Seems to do the same as replace_with(span.text)
            # span.unwrap()
            span.replace_with(span.text.strip().strip("\n"))

        chapter_text = soup.get_text()
        texts = [row for row in chapter_text.split("\n") if row.strip() != ""]

        # Combine text for word count, sentence count
        combined_text = " ".join(row for row in texts)
        combined_text = re.sub(r"\s+", " ", combined_text)
        if combined_text != "" and combined_text != prev_text:
            chapters.append(
                EpubChapter(
                    chapter_title=chapter.title,
                    chapter_number=chapter_number,
                    word_count=len(word_tokenize(combined_text)),
                    sentence_count=len(extract_sentences(combined_text)),
                    content=texts,
                    combined_text=combined_text,
                )
            )
            chapter_number += 1
            prev_text = combined_text

    for chapter in c.book.toc:
        follow_link(chapter)
    return chapters


# def extract_info(doc: fitz.Document) -> list[Chapter]:
#     chapters: list[Chapter] = []
#     for chapter_index, chapter in enumerate(get_chapters(doc)):
#         try:
#             title = chapter[1]
#             number = chapter[2]
#             content = get_text_of_chapter(doc, chapter_index)
#             chapters.append(
#                 Chapter(
#                     chapter_title=title,
#                     chapter_number=chapter_index,
#                     page_start=number,
#                     page_count=doc.chapter_page_count(chapter_index),
#                     content=content,
#                 )
#             )
#         except ValueError:
#             # TODO Handle "bad chapter number" error
#             pass
#     return chapters


@dataclass
class EpubMetadata:
    title: str
    language: str
    author: str
    date: str
    # Publisher?
    identifier: str


# def epub_info(data: io.BytesIO) -> dict:
#     def xpath(element, path):
#         return element.xpath(
#             path,
#             namespaces={
#                 "n": "urn:oasis:names:tc:opendocument:xmlns:container",
#                 "pkg": "http://www.idpf.org/2007/opf",
#                 "dc": "http://purl.org/dc/elements/1.1/",
#             },
#         )[0]

#     # prepare to read from the .epub file
#     zip_content = zipfile.ZipFile(data)

#     # find the contents metafile
#     cfname = xpath(
#         etree.fromstring(zip_content.read("META-INF/container.xml")),
#         "n:rootfiles/n:rootfile/@full-path",
#     )

#     # Debug:
#     # with open("temp.xml", "wb") as f:
#     #     f.write(zip_content.read(cfname))

#     # grab the metadata block from the contents metafile
#     metadata = xpath(etree.fromstring(zip_content.read(cfname)), "/pkg:package/pkg:metadata")

#     # repackage the data
#     extracted = {s: xpath(metadata, f"dc:{s}/text()") for s in ("title", "language", "creator", "date", "identifier")}
#     return EpubMetadata(
#         title=extracted["title"],
#         language=extracted["language"],
#         author=extracted["creator"],
#         date=extracted["date"],
#         identifier=extracted["identifier"],
#     )


def extract_metadata(data: io.BytesIO) -> EpubMetadata:
    c = EpubReader("")
    c.zf = zipfile.ZipFile(data)
    c._load_container()
    c._load_opf_file()  # load title and toc etc
    title = c.book.get_metadata("DC", "title")[0][0]
    creator = c.book.get_metadata("DC", "creator")[0][0]
    identifier = c.book.get_metadata("DC", "identifier")[0][0]
    date = c.book.get_metadata("DC", "date")[0][0]
    language = c.book.get_metadata("DC", "language")[0][0]
    return EpubMetadata(
        title=title,
        language=language,
        author=creator,
        # Date seems to be upload date?
        date=date,
        identifier=identifier,
    )


if __name__ == "__main__":
    # Extract metadata
    path = Path("/home/burny/Downloads/pg67979-images-3.epub")
    with path.open("rb") as f:
        data = f.read()
        data = io.BytesIO(data)

    meta = extract_metadata(data)
    info = extract_chapters(data)
