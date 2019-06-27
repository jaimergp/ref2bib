"""
Build BibTeX database out of DOIs and rXiv IDs.

3rd party requirements:
- aiohttp
- aiofiles

Usage
=====

Simply add the DOIs or other supported identifiers to the
command line arguments:

    python ref2bib.py id1 id2 id3

You can also create file with line separated identifiers and
use it like this:

    python ref2bib.py -f identifiers.txt

If you want, you can combine both approaches as well:

    python ref2bib.py -f identifiers.txt id1 id2 id3

All identifiers will be collected and duplicates will be omitted.

Supported identifiers
=====================

- DOI
- arXivID

"""

from argparse import ArgumentParser
from datetime import datetime
from textwrap import dedent
from xml.etree import ElementTree
import asyncio
import logging
import sys

if sys.version_info < (3, 7):
    raise RuntimeError("ref2bib requires Python 3.7+")

import aiohttp
import aiofiles


_logger = logging.getLogger(__name__)


####################################################################
# Public API
####################################################################


async def process_identifiers(identifiers: [str], outputfile=None):
    if outputfile is None:
        outputfile = datetime.now().strftime("%Y%m%d-%H%M%S") + ".bib"

    semaphore = asyncio.BoundedSemaphore(100)
    async with aiohttp.ClientSession() as session, semaphore:
        tasks = [
            identifier_to_file(identifier, session, outputfile)
            for identifier in identifiers
        ]
        await asyncio.gather(*tasks)


async def identifier_to_file(
    identifier: str, session: aiohttp.ClientSession, outputfile: str
):
    text = await get_reference(identifier, session)
    if not text:
        return
    async with aiofiles.open(outputfile, "a") as f:
        await f.write(text + "\n")


async def get_reference(identifier: str, session: aiohttp.ClientSession) -> str:
    for handler in _HANDLERS:
        try:
            reference = await handler(identifier, session)
            break
        except (
            aiohttp.client_exceptions.ClientResponseError,
            ValueError,
            NotImplementedError,
        ):
            pass
    else:
        _logger.warning("Could not find a reference for identifier %s", identifier)
        return
    return reference


async def reference_from_doi(identifier: str, session: aiohttp.ClientSession) -> str:
    url = f"https://api.crossref.org/works/{identifier}/transform/application/x-bibtex"
    return await _fetch_request(url, session)


async def reference_from_rxiv(identifier: str, session: aiohttp.ClientSession) -> str:
    # TODO: Group identifiers for a single request?
    url = f"https://export.arxiv.org/api/query?id_list={identifier}"
    text = await _fetch_request(url, session)
    return await _parse_arxiv_xml(text, identifier)


####################################################################
# Private names
####################################################################


async def _fetch_request(url: str, session: aiohttp.ClientSession, **kwargs) -> str:
    response = await session.get(url=url, **kwargs)
    response.raise_for_status()
    return await response.text()


async def _parse_arxiv_xml(text: str, identifier: str) -> str:
    # TODO: Parse the XML response and format as BibTex
    # See https://github.com/ssp/arXivToBibTeX/blob/master/lookup.py
    tree = ElementTree.fromstring(text)
    if tree.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults").text == "0":
        return
    entries = []
    for result in tree.findall("{http://www.w3.org/2005/Atom}entry"):
        title = result.find("{http://www.w3.org/2005/Atom}title").text
        authors = [
            author.find("{http://www.w3.org/2005/Atom}name").text
            for author in result.findall("{http://www.w3.org/2005/Atom}author")
        ]
        # TODO: (should we use `published` or `updated`?)
        year = int(result.find("{http://www.w3.org/2005/Atom}published").text[:4])
        eprint = f"arXiv:{identifier}"
        doi = getattr(result.find("{http://arxiv.org/schemas/atom}doi"), "text", None)
        doi_str = f"Doi = {{{doi}}}," if doi else ""
        bibtex = dedent(
            f"""
            @article{{{identifier},
                Author = {{{' and '.join(authors)}}},
                Title = {{{title}}},
                Year = {year},
                Eprint = {{{eprint}}},
                {doi_str}
            }}"""
        )[1:]
        entries.append(bibtex)
    return "\n".join(entries)


def _parse_cli():
    p = ArgumentParser()
    p.add_argument("ids", nargs="*")
    p.add_argument("-f", "--inputfile")
    p.add_argument("-o", "--outputfile")
    args = p.parse_args()
    if not (args.ids or args.inputfile):
        p.error('At least one identifier is required, either via arguments or -f <inputfile>.')
    return args


def _prepare_identifiers(args):
    ids = []
    if args.inputfile:
        with open(args.inputfile) as f:
            ids = [line.strip() for line in f]
    return set(args.ids + ids)


def main():
    args = _parse_cli()
    identifiers = _prepare_identifiers(args)
    asyncio.run(process_identifiers(identifiers))



# Update this tuple when for handlers are added!
_HANDLERS = (reference_from_doi, reference_from_rxiv)


if __name__ == "__main__":
    main()
