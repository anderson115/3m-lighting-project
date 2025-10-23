"""Unit tests for Target collectors."""
from __future__ import annotations

from textwrap import dedent

from src.pipeline.collectors.target import TargetParser

SAMPLE = dedent(
    """
    ### [![Image 1: Sample](img)](https://www.target.com/p/sample-product/-/A-123#lnk=sametab)
    $9.99
    [Sample Product](https://www.target.com/p/sample-product/-/A-123#lnk=sametab)
    [Sample Brand](https://www.target.com/b/sample-brand/-/N-123)
    [4.5 out of 5 stars with 10 ratings 10 reviews](https://www.target.com/p/sample-product/-/A-123?type=scroll_to_review_section#lnk=sametab)

    ### [![Image 2: Another](img2)](https://www.target.com/p/another-product/-/A-456#lnk=sametab)
    $15.49
    [Another Product](https://www.target.com/p/another-product/-/A-456#lnk=sametab)
    [Another Brand](https://www.target.com/b/another-brand/-/N-456)
    [4.0 out of 5 stars with 5 ratings 5 reviews](https://www.target.com/p/another-product/-/A-456?type=scroll_to_review_section#lnk=sametab)
    """
)


def test_target_parser_extracts_products():
    parser = TargetParser()
    products = parser.parse('\n' + SAMPLE)  # mimic actual split
    assert len(products) == 2
    first = products[0]
    assert first.title == 'Sample Product'
    assert first.price == '$9.99'
    assert first.brand == 'Sample Brand'
    assert '4.5 out of 5 stars' in (first.rating or '')
