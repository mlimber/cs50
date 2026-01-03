import pytest

from minesweeper import Sentence

"""
Test suite for the Sentence class.

Spec:
- known_mines: return set of all cells known to be mines (when count == len(cells))
- known_safes: return set of all cells known to be safe (when count == 0)
- mark_mine: remove cell from sentence and decrement count (if cell in sentence)
- mark_safe: remove cell from sentence, count unchanged (if cell in sentence)
"""


# =============================================================================
# known_mines() tests
# =============================================================================

class TestKnownMines:
    """Tests for Sentence.known_mines()"""

    def test_all_cells_are_mines(self):
        """When count equals number of cells, all cells are mines."""
        cells = {(0, 0), (0, 1), (1, 0)}
        sentence = Sentence(cells, 3)
        assert sentence.known_mines() == cells

    def test_not_all_cells_are_mines(self):
        """When count < len(cells), we cannot determine which are mines."""
        cells = {(0, 0), (0, 1), (1, 0)}
        sentence = Sentence(cells, 2)
        assert sentence.known_mines() == set()

    def test_no_mines(self):
        """When count is 0, no cells are mines."""
        cells = {(0, 0), (0, 1), (1, 0)}
        sentence = Sentence(cells, 0)
        assert sentence.known_mines() == set()

    def test_empty_sentence(self):
        """Empty sentence has no known mines."""
        sentence = Sentence(set(), 0)
        assert sentence.known_mines() == set()

    def test_single_cell_is_mine(self):
        """Single cell with count=1 is a known mine."""
        cell = (0, 0)
        sentence = Sentence({cell}, 1)
        assert sentence.known_mines() == {cell}

    def test_single_cell_not_mine(self):
        """Single cell with count=0 is not a mine."""
        cell = (0, 0)
        sentence = Sentence({cell}, 0)
        assert sentence.known_mines() == set()


# =============================================================================
# known_safes() tests
# =============================================================================

class TestKnownSafes:
    """Tests for Sentence.known_safes()"""

    def test_all_cells_are_safe(self):
        """When count is 0, all cells are safe."""
        cells = {(0, 0), (0, 1), (1, 0)}
        sentence = Sentence(cells, 0)
        assert sentence.known_safes() == cells

    def test_not_all_cells_are_safe(self):
        """When count > 0, we cannot determine which are safe."""
        cells = {(0, 0), (0, 1), (1, 0)}
        sentence = Sentence(cells, 1)
        assert sentence.known_safes() == set()

    def test_all_mines(self):
        """When count equals len(cells), no cells are safe."""
        cells = {(0, 0), (0, 1), (1, 0)}
        sentence = Sentence(cells, 3)
        assert sentence.known_safes() == set()

    def test_empty_sentence(self):
        """Empty sentence has no known safes."""
        sentence = Sentence(set(), 0)
        assert sentence.known_safes() == set()

    def test_single_cell_is_safe(self):
        """Single cell with count=0 is safe."""
        cell = (0, 0)
        sentence = Sentence({cell}, 0)
        assert sentence.known_safes() == {cell}

    def test_single_cell_is_mine(self):
        """Single cell with count=1 means it's a mine, not safe."""
        cell = (0, 0)
        sentence = Sentence({cell}, 1)
        assert sentence.known_safes() == set()


# =============================================================================
# mark_mine() tests
# =============================================================================

class TestMarkMine:
    """Tests for Sentence.mark_mine()"""

    def test_cell_in_sentence(self):
        """Marking a mine in the sentence removes it and decrements count."""
        cells = {(0, 0), (0, 1), (1, 0)}
        sentence = Sentence(cells, 2)
        sentence.mark_mine((0, 0))
        assert sentence.cells == {(0, 1), (1, 0)}
        assert sentence.count == 1

    def test_cell_not_in_sentence(self):
        """Marking a mine not in the sentence has no effect."""
        cells = {(0, 0), (0, 1), (1, 0)}
        sentence = Sentence(cells, 2)
        sentence.mark_mine((9, 9))
        assert sentence.cells == cells
        assert sentence.count == 2

    def test_last_cell_as_mine(self):
        """Marking the only cell as a mine empties the sentence."""
        sentence = Sentence({(0, 0)}, 1)
        sentence.mark_mine((0, 0))
        assert sentence.cells == set()
        assert sentence.count == 0

    def test_multiple_marks(self):
        """Mark multiple cells as mines sequentially."""
        cells = {(0, 0), (0, 1), (1, 0)}
        sentence = Sentence(cells, 2)
        sentence.mark_mine((0, 0))
        sentence.mark_mine((0, 1))
        assert sentence.cells == {(1, 0)}
        assert sentence.count == 0

    def test_idempotent_marking(self):
        """Marking the same cell twice has no additional effect."""
        cells = {(0, 0), (0, 1), (1, 0)}
        sentence = Sentence(cells, 2)
        sentence.mark_mine((0, 0))
        sentence.mark_mine((0, 0))  # second call should do nothing
        assert sentence.cells == {(0, 1), (1, 0)}
        assert sentence.count == 1


# =============================================================================
# __lt__ (less than / subset) tests
# =============================================================================

class TestLessThan:
    """Tests for Sentence.__lt__() - proper subset comparison."""

    def test_proper_subset_is_less_than(self):
        """A sentence with a proper subset of cells is less than the other."""
        s1 = Sentence({(0, 0), (0, 1)}, 1)
        s2 = Sentence({(0, 0), (0, 1), (0, 2)}, 2)
        assert s1 < s2

    def test_equal_sets_not_less_than(self):
        """Equal cell sets are not less than each other."""
        s1 = Sentence({(0, 0), (0, 1)}, 1)
        s2 = Sentence({(0, 0), (0, 1)}, 1)
        assert not (s1 < s2)
        assert not (s2 < s1)

    def test_superset_not_less_than(self):
        """A superset is not less than its subset."""
        s1 = Sentence({(0, 0), (0, 1), (0, 2)}, 2)
        s2 = Sentence({(0, 0), (0, 1)}, 1)
        assert not (s1 < s2)

    def test_disjoint_sets_not_less_than(self):
        """Disjoint sets are not less than each other."""
        s1 = Sentence({(0, 0), (0, 1)}, 1)
        s2 = Sentence({(1, 0), (1, 1)}, 1)
        assert not (s1 < s2)
        assert not (s2 < s1)

    def test_overlapping_but_not_subset(self):
        """Overlapping sets that aren't subsets are not less than."""
        s1 = Sentence({(0, 0), (0, 1)}, 1)
        s2 = Sentence({(0, 1), (0, 2)}, 1)
        assert not (s1 < s2)
        assert not (s2 < s1)

    def test_empty_set_is_subset_of_nonempty(self):
        """Empty set is a proper subset of any non-empty set."""
        s1 = Sentence(set(), 0)
        s2 = Sentence({(0, 0), (0, 1)}, 1)
        assert s1 < s2

    def test_empty_sets_not_less_than(self):
        """Two empty sets are not less than each other."""
        s1 = Sentence(set(), 0)
        s2 = Sentence(set(), 0)
        assert not (s1 < s2)

    def test_single_cell_subset(self):
        """Single cell subset of larger set."""
        s1 = Sentence({(0, 0)}, 1)
        s2 = Sentence({(0, 0), (0, 1), (0, 2)}, 2)
        assert s1 < s2

    def test_count_does_not_affect_comparison(self):
        """Less than only compares cells, not counts."""
        s1 = Sentence({(0, 0), (0, 1)}, 0)
        s2 = Sentence({(0, 0), (0, 1), (0, 2)}, 3)
        assert s1 < s2


# =============================================================================
# __sub__ (subtraction) tests
# =============================================================================

class TestSubtraction:
    """Tests for Sentence.__sub__() - sentence subtraction."""

    def test_subtract_subset(self):
        """Subtracting a subset produces difference set and count."""
        s1 = Sentence({(0, 0), (0, 1), (0, 2)}, 2)
        s2 = Sentence({(0, 0), (0, 1)}, 1)
        result = s1 - s2
        assert result.cells == {(0, 2)}
        assert result.count == 1

    def test_subtract_empty_sentence(self):
        """Subtracting empty sentence returns original cells and count."""
        s1 = Sentence({(0, 0), (0, 1)}, 1)
        s2 = Sentence(set(), 0)
        result = s1 - s2
        assert result.cells == {(0, 0), (0, 1)}
        assert result.count == 1

    def test_subtract_from_empty_sentence(self):
        """Subtracting from empty sentence returns empty with negative count."""
        s1 = Sentence(set(), 0)
        s2 = Sentence({(0, 0)}, 1)
        result = s1 - s2
        assert result.cells == set()
        assert result.count == -1

    def test_subtract_equal_sentences(self):
        """Subtracting equal sentences produces empty set with count 0."""
        s1 = Sentence({(0, 0), (0, 1)}, 2)
        s2 = Sentence({(0, 0), (0, 1)}, 2)
        result = s1 - s2
        assert result.cells == set()
        assert result.count == 0

    def test_subtract_disjoint_sets(self):
        """Subtracting disjoint sets returns original cells."""
        s1 = Sentence({(0, 0), (0, 1)}, 2)
        s2 = Sentence({(1, 0), (1, 1)}, 1)
        result = s1 - s2
        assert result.cells == {(0, 0), (0, 1)}
        assert result.count == 1

    def test_subtract_overlapping_sets(self):
        """Subtracting overlapping sets removes common cells."""
        s1 = Sentence({(0, 0), (0, 1), (0, 2)}, 2)
        s2 = Sentence({(0, 1), (0, 2), (0, 3)}, 1)
        result = s1 - s2
        assert result.cells == {(0, 0)}
        assert result.count == 1

    def test_subtraction_does_not_modify_original(self):
        """Subtraction should not modify the original sentences."""
        cells1 = {(0, 0), (0, 1), (0, 2)}
        cells2 = {(0, 0), (0, 1)}
        s1 = Sentence(cells1.copy(), 2)
        s2 = Sentence(cells2.copy(), 1)
        _ = s1 - s2
        assert s1.cells == cells1
        assert s1.count == 2
        assert s2.cells == cells2
        assert s2.count == 1

    def test_subtraction_returns_new_sentence(self):
        """Subtraction returns a new Sentence instance."""
        s1 = Sentence({(0, 0), (0, 1)}, 2)
        s2 = Sentence({(0, 0)}, 1)
        result = s1 - s2
        assert result is not s1
        assert result is not s2
        assert isinstance(result, Sentence)

    def test_count_difference_calculation(self):
        """Count difference is calculated correctly."""
        s1 = Sentence({(0, 0), (0, 1), (0, 2)}, 3)
        s2 = Sentence({(0, 0)}, 1)
        result = s1 - s2
        assert result.count == 2  # 3 - 1

    def test_subset_inference_scenario(self):
        """Test real subset inference: if {A,B}=1 and {A,B,C}=1, then {C}=0."""
        # Sentence 1: {A, B, C} = 1 mine
        s1 = Sentence({(0, 0), (0, 1), (0, 2)}, 1)
        # Sentence 2: {A, B} = 1 mine
        s2 = Sentence({(0, 0), (0, 1)}, 1)
        # If s2 < s1, then s1 - s2 = {C} = 0 (C is safe)
        assert s2 < s1
        result = s1 - s2
        assert result.cells == {(0, 2)}
        assert result.count == 0
        # This means (0,2) is safe since count is 0

    def test_mine_inference_scenario(self):
        """Test mine inference: if {A,B}=2 and {A,B,C}=2, then {C}=0."""
        # Different scenario: {A, B, C} = 2 and {A, B} = 1
        s1 = Sentence({(0, 0), (0, 1), (0, 2)}, 2)
        s2 = Sentence({(0, 0), (0, 1)}, 1)
        assert s2 < s1
        result = s1 - s2
        assert result.cells == {(0, 2)}
        assert result.count == 1
        # This means (0,2) is a mine since count equals len(cells)


# =============================================================================
# mark_safe() tests
# =============================================================================

class TestMarkSafe:
    """Tests for Sentence.mark_safe()"""

    def test_cell_in_sentence(self):
        """Marking a safe cell removes it from sentence, count unchanged."""
        cells = {(0, 0), (0, 1), (1, 0)}
        sentence = Sentence(cells, 2)
        sentence.mark_safe((0, 0))
        assert sentence.cells == {(0, 1), (1, 0)}
        assert sentence.count == 2  # count stays the same

    def test_cell_not_in_sentence(self):
        """Marking a safe cell not in the sentence has no effect."""
        cells = {(0, 0), (0, 1), (1, 0)}
        sentence = Sentence(cells, 2)
        sentence.mark_safe((9, 9))
        assert sentence.cells == cells
        assert sentence.count == 2

    def test_last_cell_as_safe(self):
        """Marking the only cell as safe empties the sentence."""
        sentence = Sentence({(0, 0)}, 0)
        sentence.mark_safe((0, 0))
        assert sentence.cells == set()
        assert sentence.count == 0

    def test_multiple_marks(self):
        """Mark multiple cells as safe sequentially."""
        cells = {(0, 0), (0, 1), (1, 0)}
        sentence = Sentence(cells, 1)
        sentence.mark_safe((0, 0))
        sentence.mark_safe((0, 1))
        assert sentence.cells == {(1, 0)}
        assert sentence.count == 1  # count unchanged

    def test_idempotent_marking(self):
        """Marking the same cell twice has no additional effect."""
        cells = {(0, 0), (0, 1), (1, 0)}
        sentence = Sentence(cells, 1)
        sentence.mark_safe((0, 0))
        sentence.mark_safe((0, 0))  # second call should do nothing
        assert sentence.cells == {(0, 1), (1, 0)}
        assert sentence.count == 1


# =============================================================================
# Integration / Edge case tests
# =============================================================================

class TestIntegration:
    """Integration and edge case tests."""

    def test_mixed_marking(self):
        """Mark some cells as mines and some as safe."""
        cells = {(0, 0), (0, 1), (1, 0), (1, 1)}
        sentence = Sentence(cells, 2)
        sentence.mark_mine((0, 0))  # count: 2 -> 1
        sentence.mark_safe((0, 1))  # count stays 1
        assert sentence.cells == {(1, 0), (1, 1)}
        assert sentence.count == 1

    def test_marking_reveals_remaining_mines(self):
        """After marking safes, remaining cells may be known mines."""
        cells = {(0, 0), (0, 1), (1, 0)}
        sentence = Sentence(cells, 2)
        # Mark one cell safe -> {(0, 1), (1, 0)} with count=2
        sentence.mark_safe((0, 0))
        # Now count == len(cells), so remaining are all mines
        assert sentence.known_mines() == {(0, 1), (1, 0)}

    def test_marking_reveals_remaining_safes(self):
        """After marking mines, remaining cells may be known safe."""
        cells = {(0, 0), (0, 1), (1, 0)}
        sentence = Sentence(cells, 2)
        # Mark two cells as mines -> {(1, 0)} with count=0
        sentence.mark_mine((0, 0))
        sentence.mark_mine((0, 1))
        # Now count == 0, so remaining are all safe
        assert sentence.known_safes() == {(1, 0)}

    def test_empty_after_all_marked(self):
        """Sentence becomes empty after all cells marked."""
        cells = {(0, 0), (0, 1)}
        sentence = Sentence(cells, 1)
        sentence.mark_mine((0, 0))
        sentence.mark_safe((0, 1))
        assert sentence.cells == set()
        assert sentence.count == 0

    def test_original_cells_not_mutated(self):
        """Ensure original set passed to constructor is not mutated."""
        original_cells = {(0, 0), (0, 1), (1, 0)}
        cells_copy = original_cells.copy()
        sentence = Sentence(original_cells, 2)
        sentence.mark_mine((0, 0))
        sentence.mark_safe((0, 1))
        # Original set should be unchanged
        assert original_cells == cells_copy


def test_known_mines():
    pass


def test_known_safes():
    pass


def test_mark_mine_not_present_in_sent():
    pass


def test_mark_mine():
    pass


def mark_safe_not_present_in_sent():
    pass


def mark_safe_present():
    pass
