import pytest
from pagerank import transition_model


# Sample corpora for testing
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


class TestTransitionModelReturnsDict:
    """Test that transition_model returns a dictionary"""

    def test_returns_dict(self, corpus_simple):
        result = transition_model(corpus_simple, "1.html", 0.85)
        assert isinstance(result, dict)

    def test_keys_are_all_pages(self, corpus_simple):
        result = transition_model(corpus_simple, "1.html", 0.85)
        assert set(result.keys()) == set(corpus_simple.keys())


class TestTransitionModelProbabilities:
    """Test that probabilities are valid and sum to 1"""

    def test_probabilities_sum_to_one(self, corpus_simple):
        result = transition_model(corpus_simple, "1.html", 0.85)
        assert pytest.approx(sum(result.values()), abs=1e-9) == 1.0

    def test_probabilities_sum_to_one_all_pages(self, corpus_simple):
        """Check sum for all pages in corpus"""
        for page in corpus_simple:
            result = transition_model(corpus_simple, page, 0.85)
            assert pytest.approx(sum(result.values()), abs=1e-9) == 1.0

    def test_all_probabilities_non_negative(self, corpus_simple):
        result = transition_model(corpus_simple, "1.html", 0.85)
        assert all(prob >= 0 for prob in result.values())

    def test_all_probabilities_at_most_one(self, corpus_simple):
        result = transition_model(corpus_simple, "1.html", 0.85)
        assert all(prob <= 1 for prob in result.values())


class TestTransitionModelDampingFactor:
    """Test behavior with different damping factors"""

    def test_damping_factor_zero(self, corpus_simple):
        """With damping=0, should choose uniformly from all pages"""
        result = transition_model(corpus_simple, "1.html", 0.0)
        expected_prob = 1.0 / len(corpus_simple)
        for prob in result.values():
            assert pytest.approx(prob, abs=1e-9) == expected_prob

    def test_damping_factor_one(self, corpus_simple):
        """With damping=1, should only follow links (if available)"""
        result = transition_model(corpus_simple, "1.html", 1.0)
        # Page 1.html only links to 2.html
        assert pytest.approx(result["2.html"], abs=1e-9) == 1.0
        assert pytest.approx(result["1.html"], abs=1e-9) == 0.0
        assert pytest.approx(result["3.html"], abs=1e-9) == 0.0

    def test_damping_factor_standard(self, corpus_simple):
        """Test with standard damping factor 0.85"""
        result = transition_model(corpus_simple, "1.html", 0.85)
        # Page 1.html links only to 2.html
        # P(2.html) = 0.85 * 1.0 + 0.15 * (1/3) = 0.85 + 0.05 = 0.9
        # P(1.html) = 0.85 * 0.0 + 0.15 * (1/3) = 0.05
        # P(3.html) = 0.85 * 0.0 + 0.15 * (1/3) = 0.05
        assert pytest.approx(result["2.html"], abs=1e-9) == 0.85 + 0.15 / 3
        assert pytest.approx(result["1.html"], abs=1e-9) == 0.15 / 3
        assert pytest.approx(result["3.html"], abs=1e-9) == 0.15 / 3


class TestTransitionModelNoLinks:
    """Test behavior when current page has no outgoing links"""

    def test_no_links_uniform_distribution(self, corpus_no_links):
        """If page has no links, choose uniformly from all pages"""
        result = transition_model(corpus_no_links, "2.html", 0.85)
        expected_prob = 1.0 / len(corpus_no_links)
        for prob in result.values():
            assert pytest.approx(prob, abs=1e-9) == expected_prob

    def test_no_links_probabilities_sum_to_one(self, corpus_no_links):
        result = transition_model(corpus_no_links, "2.html", 0.85)
        assert pytest.approx(sum(result.values()), abs=1e-9) == 1.0


class TestTransitionModelSinglePage:
    """Test with single-page corpus"""

    def test_single_page_probability_is_one(self, corpus_single_page):
        result = transition_model(corpus_single_page, "only.html", 0.85)
        assert pytest.approx(result["only.html"], abs=1e-9) == 1.0


class TestTransitionModelMultipleLinks:
    """Test when page has multiple outgoing links"""

    def test_multiple_links_distribution(self, corpus_all_linked):
        """Page a.html links to b.html and c.html"""
        result = transition_model(corpus_all_linked, "a.html", 0.85)
        # P(linked page) = 0.85 * (1/2) + 0.15 * (1/3) = 0.425 + 0.05 = 0.475
        # P(current page) = 0.85 * 0 + 0.15 * (1/3) = 0.05
        expected_linked = 0.85 * 0.5 + 0.15 / 3
        expected_unlinked = 0.15 / 3
        assert pytest.approx(result["b.html"], abs=1e-9) == expected_linked
        assert pytest.approx(result["c.html"], abs=1e-9) == expected_linked
        assert pytest.approx(result["a.html"], abs=1e-9) == expected_unlinked

    def test_page_with_two_links(self, corpus_simple):
        """Page 2.html links to 1.html and 3.html"""
        result = transition_model(corpus_simple, "2.html", 0.85)
        # P(linked page) = 0.85 * (1/2) + 0.15 * (1/3)
        # P(current page) = 0.85 * 0 + 0.15 * (1/3)
        expected_linked = 0.85 * 0.5 + 0.15 / 3
        expected_unlinked = 0.15 / 3
        assert pytest.approx(result["1.html"], abs=1e-9) == expected_linked
        assert pytest.approx(result["3.html"], abs=1e-9) == expected_linked
        assert pytest.approx(result["2.html"], abs=1e-9) == expected_unlinked
