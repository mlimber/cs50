import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


# Shared test fixtures for pagerank tests


@pytest.fixture
def corpus_simple():
    """Simple corpus with clear link structure"""
    return {
        "1.html": {"2.html"},
        "2.html": {"1.html", "3.html"},
        "3.html": {"2.html"},
    }


@pytest.fixture
def corpus_no_links():
    """Corpus where a page has no outgoing links"""
    return {
        "1.html": {"2.html"},
        "2.html": set(),  # No outgoing links
        "3.html": {"1.html"},
    }


@pytest.fixture
def corpus_single_page():
    """Corpus with a single page"""
    return {
        "only.html": set(),
    }


@pytest.fixture
def corpus_all_linked():
    """Corpus where every page links to every other page"""
    return {
        "a.html": {"b.html", "c.html"},
        "b.html": {"a.html", "c.html"},
        "c.html": {"a.html", "b.html"},
    }
