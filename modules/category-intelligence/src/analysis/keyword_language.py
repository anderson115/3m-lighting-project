"""Keyword vs. community language analysis."""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

_URL_PATTERN = re.compile(r"https?://\S+")
_TOKEN_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z\-\d']+")
_STOPWORDS = {
    "the",
    "of",
    "to",
    "and",
    "a",
    "in",
    "for",
    "with",
    "on",
    "at",
    "from",
    "into",
    "is",
    "are",
    "be",
    "your",
    "you",
    "this",
    "that",
    "it",
    "as",
    "have",
    "has",
    "was",
    "were",
    "can",
    "will",
    "but",
    "just",
    "they",
    "them",
    "get",
    "got",
    "our",
    "out",
    "all",
    "any",
    "had",
    "more",
    "when",
    "what",
    "why",
    "how",
    "about",
    "make",
    "made",
    "into",
    "than",
    "their",
    "there",
    "also",
    "im",
    "i'm",
    "ive",
    "i've",
    "really",
    "probably",
    "going",
    "thing",
    "need",
    "know",
    "want",
    "great",
    "good",
    "even",
    "like",
    "some",
    "would",
    "use",
    "then",
    "put",
    "could",
    "stuff",
    "used",
    "work",
    "hang",
    "https",
    "www",
    "amp",
    "bought",
    "went",
    "posting",
    "did",
    "i'd",
    "id",
    "mine",
    "didn't",
    "took",
    "youtube",
    "moderators",
    "cheaper",
    "wouldn't",
    "said",
    "one",
    "two",
    "three",
}


@dataclass(frozen=True)
class HiddenTerm:
    """A candidate term that appears in community language but not in ads."""

    term: str
    community_freq: int
    ad_freq: int
    example: str | None = None
    source_url: str | None = None
    subreddit: str | None = None


@dataclass(frozen=True)
class KeywordLanguageSummary:
    """Aggregate view of keyword vs. community language signals."""

    total_ad_records: int
    total_community_records: int
    top_ad_terms: list[tuple[str, int]]
    hidden_terms: list[HiddenTerm]


def _strip_urls(text: str) -> str:
    return _URL_PATTERN.sub(" ", text)


def _tokenise(text: str) -> list[str]:
    cleaned = _strip_urls(text.lower())
    tokens = [match.group(0) for match in _TOKEN_PATTERN.finditer(cleaned)]
    return [
        token
        for token in tokens
        if token not in _STOPWORDS and len(token) > 2 and not token.isdigit()
    ]


def _load_json_lines(paths: Sequence[Path]) -> list[dict]:
    data: list[dict] = []
    for path in paths:
        if not path.exists():
            continue
        loaded = json.loads(path.read_text())
        if isinstance(loaded, dict):
            data.append(loaded)
        elif isinstance(loaded, list):
            data.extend(loaded)
    return data


def _extract_ad_corpus(ad_records: Iterable[dict]) -> tuple[list[str], int]:
    corpus: list[str] = []
    total = 0
    for record in ad_records:
        total += 1
        fields = []
        for key in (
            "title",
            "description",
            "short_description",
            "product_description",
        ):
            value = record.get(key)
            if isinstance(value, str):
                fields.append(value)
        features = record.get("features")
        if isinstance(features, list):
            fields.extend(str(item) for item in features)
        categories = record.get("categories")
        if isinstance(categories, list):
            fields.extend(str(item) for item in categories)
        corpus.append(" ".join(fields))
    return corpus, total


def _extract_community_corpus(community_records: Iterable[dict]) -> tuple[list[str], int]:
    corpus: list[str] = []
    total = 0
    for record in community_records:
        body = record.get("body")
        if not isinstance(body, str):
            continue
        corpus.append(body)
        total += 1
    return corpus, total


def _select_examples(
    candidates: Sequence[str],
    community_records: Iterable[dict],
    max_examples: int = 15,
) -> dict[str, HiddenTerm]:
    examples: dict[str, HiddenTerm] = {}
    for record in community_records:
        body = record.get("body")
        if not isinstance(body, str):
            continue
        lower_body = body.lower()
        for term in candidates:
            if term in examples:
                continue
            if term in lower_body:
                examples[term] = HiddenTerm(
                    term=term,
                    community_freq=0,
                    ad_freq=0,
                    example=body.strip(),
                    source_url=record.get("permalink"),
                    subreddit=record.get("subreddit"),
                )
                if len(examples) >= max_examples:
                    return examples
    return examples


def compute_keyword_language_summary(
    ad_files: Sequence[Path],
    community_files: Sequence[Path],
    min_community_freq: int = 5,
    max_hidden_terms: int = 20,
) -> KeywordLanguageSummary:
    """Compare ad-language and community-language corpora."""

    ad_records = _load_json_lines(ad_files)
    community_records = _load_json_lines(community_files)

    ad_corpus, ad_total = _extract_ad_corpus(ad_records)
    community_corpus, community_total = _extract_community_corpus(community_records)

    ad_tokens = Counter()
    for text in ad_corpus:
        ad_tokens.update(_tokenise(text))

    community_tokens = Counter()
    for text in community_corpus:
        community_tokens.update(_tokenise(text))

    top_ad_terms = ad_tokens.most_common(25)

    hidden: list[HiddenTerm] = []
    base_candidates: list[str] = []
    for term, freq in community_tokens.most_common():
        if freq < min_community_freq:
            break
        if len(term) < 5:
            continue
        if not any(char.isalpha() for char in term):
            continue
        ad_threshold = max(1, math.ceil(freq * 0.05))
        if ad_tokens[term] <= ad_threshold:
            base_candidates.append(term)
        if len(base_candidates) >= max_hidden_terms:
            break

    example_mapping = _select_examples(base_candidates, community_records)

    for term in base_candidates:
        example = example_mapping.get(term)
        hidden.append(
            HiddenTerm(
                term=term,
                community_freq=community_tokens[term],
                ad_freq=ad_tokens[term],
                example=example.example if example else None,
                source_url=example.source_url if example else None,
                subreddit=example.subreddit if example else None,
            )
        )

    return KeywordLanguageSummary(
        total_ad_records=ad_total,
        total_community_records=community_total,
        top_ad_terms=top_ad_terms,
        hidden_terms=hidden,
    )


def keyword_language_summary_to_dict(summary: KeywordLanguageSummary) -> dict:
    """Convert summary dataclass into a serializable dictionary."""

    return {
        "total_ad_records": summary.total_ad_records,
        "total_community_records": summary.total_community_records,
        "top_ad_terms": summary.top_ad_terms,
        "hidden_terms": [
            {
                "term": term.term,
                "community_freq": term.community_freq,
                "ad_freq": term.ad_freq,
                "example": term.example,
                "source_url": term.source_url,
                "subreddit": term.subreddit,
            }
            for term in summary.hidden_terms
        ],
    }


def write_keyword_language_summary(summary: KeywordLanguageSummary, output_path: Path) -> dict:
    """Serialize summary to JSON and return the payload."""

    payload = keyword_language_summary_to_dict(summary)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    return payload
