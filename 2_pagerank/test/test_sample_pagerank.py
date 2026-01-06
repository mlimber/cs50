import pytest
from pagerank import sample_pagerank


# Fixtures are defined in conftest.py


class TestSamplePagerankReturnsDict:
    """Test that sample_pagerank returns a dictionary with correct structure"""

    def test_returns_dict(self, corpus_simple):
        result = sample_pagerank(corpus_simple, 0.85, 100)
        assert isinstance(result, dict)

    def test_keys_are_all_pages(self, corpus_simple):
        result = sample_pagerank(corpus_simple, 0.85, 100)
        assert set(result.keys()) == set(corpus_simple.keys())

    def test_values_are_floats(self, corpus_simple):
        result = sample_pagerank(corpus_simple, 0.85, 100)
        assert all(isinstance(v, float) for v in result.values())


class TestSamplePagerankProbabilities:
    """Test that PageRank values are valid probabilities summing to 1"""

    def test_probabilities_sum_to_one(self, corpus_simple):
        result = sample_pagerank(corpus_simple, 0.85, 1000)
        assert pytest.approx(sum(result.values()), abs=1e-9) == 1.0

    def test_probabilities_sum_to_one_small_n(self, corpus_simple):
        """Even with n=1, probabilities should sum to 1"""
        result = sample_pagerank(corpus_simple, 0.85, 1)
        assert pytest.approx(sum(result.values()), abs=1e-9) == 1.0

    def test_all_probabilities_non_negative(self, corpus_simple):
        result = sample_pagerank(corpus_simple, 0.85, 1000)
        assert all(prob >= 0 for prob in result.values())

    def test_all_probabilities_at_most_one(self, corpus_simple):
        result = sample_pagerank(corpus_simple, 0.85, 1000)
        assert all(prob <= 1 for prob in result.values())


class TestSamplePagerankMinimumSamples:
    """Test behavior with minimum number of samples (n=1)"""

    def test_n_equals_one(self, corpus_simple):
        """With n=1, exactly one page should have rank 1.0, others 0.0"""
        result = sample_pagerank(corpus_simple, 0.85, 1)
        assert pytest.approx(sum(result.values()), abs=1e-9) == 1.0
        # One page has all the probability
        non_zero = [v for v in result.values() if v > 0]
        assert len(non_zero) == 1
        assert pytest.approx(non_zero[0], abs=1e-9) == 1.0


class TestSamplePagerankConvergence:
    """Test that sampling converges to expected PageRank values"""

    def test_symmetric_corpus_equal_ranks(self, corpus_all_linked):
        """In a symmetric corpus, all pages should have similar ranks"""
        result = sample_pagerank(corpus_all_linked, 0.85, 10000)
        expected = 1.0 / len(corpus_all_linked)
        for page, rank in result.items():
            # Allow 10% tolerance due to random sampling
            assert pytest.approx(rank, abs=0.05) == expected

    def test_large_n_gives_stable_results(self, corpus_simple):
        """With large n, results should be relatively consistent"""
        result1 = sample_pagerank(corpus_simple, 0.85, 10000)
        result2 = sample_pagerank(corpus_simple, 0.85, 10000)
        for page in corpus_simple:
            # Results should be within 10% of each other
            assert abs(result1[page] - result2[page]) < 0.1


class TestSamplePagerankDampingFactor:
    """Test behavior with different damping factors"""

    def test_damping_factor_zero(self, corpus_simple):
        """With damping=0, should be uniform random walk"""
        result = sample_pagerank(corpus_simple, 0.0, 10000)
        expected = 1.0 / len(corpus_simple)
        for rank in result.values():
            assert pytest.approx(rank, abs=0.05) == expected

    def test_damping_factor_one(self, corpus_simple):
        """With damping=1, only follows links"""
        result = sample_pagerank(corpus_simple, 1.0, 10000)
        # All probabilities should still sum to 1
        assert pytest.approx(sum(result.values()), abs=1e-9) == 1.0


class TestSamplePagerankNoLinks:
    """Test behavior when pages have no outgoing links"""

    def test_no_links_page(self, corpus_no_links):
        """Corpus with a page that has no links"""
        result = sample_pagerank(corpus_no_links, 0.85, 10000)
        assert pytest.approx(sum(result.values()), abs=1e-9) == 1.0
        assert all(prob >= 0 for prob in result.values())


class TestSamplePagerankSinglePage:
    """Test with single-page corpus"""

    def test_single_page_gets_all_rank(self, corpus_single_page):
        result = sample_pagerank(corpus_single_page, 0.85, 100)
        assert pytest.approx(result["only.html"], abs=1e-9) == 1.0


class TestSamplePagerankProportions:
    """Test that PageRank values represent proportions of samples"""

    def test_ranks_are_proportions(self, corpus_simple):
        """Each rank should be count/n"""
        n = 1000
        result = sample_pagerank(corpus_simple, 0.85, n)
        # Each value should be expressible as k/n for some integer k
        for rank in result.values():
            k = rank * n
            assert pytest.approx(k, abs=1e-6) == round(k)
