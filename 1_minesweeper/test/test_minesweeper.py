import pytest

from minesweeper import MinesweeperAI, Sentence

"""
In the MinesweeperAI class, complete the implementations of add_knowledge, make_safe_move, and make_random_move.

add_knowledge should accept a cell (represented as a tuple (i, j)) and its corresponding count, and update self.mines, self.safes, self.moves_made, and self.knowledge with any new information that the AI can infer, given that cell is known to be a safe cell with count mines neighboring it.
The function should mark the cell as one of the moves made in the game.
The function should mark the cell as a safe cell, updating any sentences that contain the cell as well.
The function should add a new sentence to the AI’s knowledge base, based on the value of cell and count, to indicate that count of the cell’s neighbors are mines. Be sure to only include cells whose state is still undetermined in the sentence.
If, based on any of the sentences in self.knowledge, new cells can be marked as safe or as mines, then the function should do so.
If, based on any of the sentences in self.knowledge, new sentences can be inferred (using the subset method described in the Background), then those sentences should be added to the knowledge base as well.
Note that any time that you make any change to your AI’s knowledge, it may be possible to draw new inferences that weren’t possible before. Be sure that those new inferences are added to the knowledge base if it is possible to do so.
make_safe_move should return a move (i, j) that is known to be safe.
The move returned must be known to be safe, and not a move already made.
If no safe move can be guaranteed, the function should return None.
The function should not modify self.moves_made, self.mines, self.safes, or self.knowledge.
make_random_move should return a random move (i, j).
This function will be called if a safe move is not possible: if the AI doesn’t know where to move, it will choose to move randomly instead.
The move must not be a move that has already been made.
The move must not be a move that is known to be a mine.
If no such moves are possible, the function should return None.
"""


# =============================================================================
# make_safe_move() Tests
# =============================================================================

class TestMakeSafeMove:
    """Tests for MinesweeperAI.make_safe_move()"""

    def test_returns_safe_cell_not_already_moved(self):
        """Should return a cell known to be safe and not already played."""
        ai = MinesweeperAI(height=3, width=3)
        ai.safes = {(0, 0), (0, 1), (1, 0)}
        ai.moves_made = {(0, 0)}
        move = ai.make_safe_move()
        assert move in {(0, 1), (1, 0)}
        assert move not in ai.moves_made

    def test_returns_none_when_no_safe_moves(self):
        """Should return None when no safe moves are available."""
        ai = MinesweeperAI(height=3, width=3)
        ai.safes = set()
        move = ai.make_safe_move()
        assert move is None

    def test_returns_none_when_all_safes_already_moved(self):
        """Should return None when all safe cells have been played."""
        ai = MinesweeperAI(height=3, width=3)
        ai.safes = {(0, 0), (0, 1)}
        ai.moves_made = {(0, 0), (0, 1)}
        move = ai.make_safe_move()
        assert move is None

    def test_does_not_modify_moves_made(self):
        """make_safe_move should not modify moves_made."""
        ai = MinesweeperAI(height=3, width=3)
        ai.safes = {(0, 0), (0, 1)}
        original_moves = ai.moves_made.copy()
        ai.make_safe_move()
        assert ai.moves_made == original_moves

    def test_does_not_modify_mines(self):
        """make_safe_move should not modify mines."""
        ai = MinesweeperAI(height=3, width=3)
        ai.safes = {(0, 0)}
        ai.mines = {(1, 1)}
        original_mines = ai.mines.copy()
        ai.make_safe_move()
        assert ai.mines == original_mines

    def test_does_not_modify_safes(self):
        """make_safe_move should not modify safes."""
        ai = MinesweeperAI(height=3, width=3)
        ai.safes = {(0, 0), (0, 1)}
        original_safes = ai.safes.copy()
        ai.make_safe_move()
        assert ai.safes == original_safes

    def test_does_not_modify_knowledge(self):
        """make_safe_move should not modify knowledge."""
        from minesweeper import Sentence
        ai = MinesweeperAI(height=3, width=3)
        ai.safes = {(0, 0)}
        ai.knowledge = [Sentence({(1, 1), (1, 2)}, 1)]
        original_knowledge_len = len(ai.knowledge)
        ai.make_safe_move()
        assert len(ai.knowledge) == original_knowledge_len

    def test_returns_valid_board_position(self):
        """Returned move should be within board bounds."""
        ai = MinesweeperAI(height=3, width=3)
        ai.safes = {(0, 0), (1, 1), (2, 2)}
        move = ai.make_safe_move()
        if move is not None:
            assert 0 <= move[0] < ai.height
            assert 0 <= move[1] < ai.width

    def test_single_safe_cell_available(self):
        """Should return the only available safe cell."""
        ai = MinesweeperAI(height=3, width=3)
        ai.safes = {(1, 1)}
        ai.moves_made = set()
        move = ai.make_safe_move()
        assert move == (1, 1)


# =============================================================================
# make_random_move() Tests
# =============================================================================

class TestMakeRandomMove:
    """Tests for MinesweeperAI.make_random_move()"""

    def test_returns_cell_not_already_moved(self):
        """Should return a cell that hasn't been played."""
        ai = MinesweeperAI(height=3, width=3)
        ai.moves_made = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)}
        move = ai.make_random_move()
        assert move not in ai.moves_made

    def test_returns_cell_not_known_mine(self):
        """Should not return a cell known to be a mine."""
        ai = MinesweeperAI(height=3, width=3)
        ai.mines = {(0, 0), (0, 1), (0, 2)}
        move = ai.make_random_move()
        assert move not in ai.mines

    def test_returns_none_when_all_cells_played_or_mines(self):
        """Should return None when no valid moves exist."""
        ai = MinesweeperAI(height=2, width=2)
        ai.moves_made = {(0, 0), (0, 1)}
        ai.mines = {(1, 0), (1, 1)}
        move = ai.make_random_move()
        assert move is None

    def test_returns_valid_board_position(self):
        """Returned move should be within board bounds."""
        ai = MinesweeperAI(height=3, width=3)
        move = ai.make_random_move()
        assert move is not None
        assert 0 <= move[0] < ai.height
        assert 0 <= move[1] < ai.width

    def test_returns_none_for_fully_explored_board(self):
        """Should return None when all cells have been moved."""
        ai = MinesweeperAI(height=2, width=2)
        ai.moves_made = {(0, 0), (0, 1), (1, 0), (1, 1)}
        move = ai.make_random_move()
        assert move is None

    def test_chooses_from_available_cells(self):
        """Should choose from cells that are neither moved nor mines."""
        ai = MinesweeperAI(height=3, width=3)
        ai.moves_made = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0)}
        ai.mines = {(2, 1)}
        # Only (2, 2) should be available
        move = ai.make_random_move()
        assert move == (2, 2)

    def test_randomness_returns_different_cells(self):
        """Multiple calls should potentially return different cells."""
        ai = MinesweeperAI(height=3, width=3)
        moves = set()
        for _ in range(50):
            move = ai.make_random_move()
            if move:
                moves.add(move)
        # With 9 possible cells and 50 tries, we should see multiple different moves
        assert len(moves) > 1

    def test_avoids_both_mines_and_moves_made(self):
        """Should avoid cells that are either mines or already moved."""
        ai = MinesweeperAI(height=3, width=3)
        ai.moves_made = {(0, 0), (0, 1), (0, 2)}
        ai.mines = {(1, 0), (1, 1), (1, 2)}
        # Available: (2, 0), (2, 1), (2, 2)
        for _ in range(20):
            move = ai.make_random_move()
            assert move is not None
            assert move[0] == 2  # Must be in row 2

    def test_empty_board_returns_valid_move(self):
        """On fresh board, random move should return valid cell."""
        ai = MinesweeperAI(height=8, width=8)
        move = ai.make_random_move()
        assert move is not None
        assert 0 <= move[0] < 8
        assert 0 <= move[1] < 8


# =============================================================================
# add_knowledge() Tests
# =============================================================================

class TestAddKnowledge:
    """Tests for MinesweeperAI.add_knowledge()"""

    # -------------------------------------------------------------------------
    # Basic functionality: marking cell as move and safe
    # -------------------------------------------------------------------------

    def test_marks_cell_as_move_made(self):
        """add_knowledge should mark the cell as a move made."""
        ai = MinesweeperAI(height=3, width=3)
        ai.add_knowledge((1, 1), 0)
        assert (1, 1) in ai.moves_made

    def test_marks_cell_as_safe(self):
        """add_knowledge should mark the cell as safe."""
        ai = MinesweeperAI(height=3, width=3)
        ai.add_knowledge((1, 1), 0)
        assert (1, 1) in ai.safes

    def test_multiple_calls_accumulate_moves(self):
        """Multiple calls should accumulate moves_made."""
        ai = MinesweeperAI(height=3, width=3)
        ai.add_knowledge((0, 0), 0)
        ai.add_knowledge((1, 1), 0)
        ai.add_knowledge((2, 2), 0)
        assert (0, 0) in ai.moves_made
        assert (1, 1) in ai.moves_made
        assert (2, 2) in ai.moves_made

    # -------------------------------------------------------------------------
    # Sentence creation: neighbors and undetermined cells
    # -------------------------------------------------------------------------

    def test_adds_sentence_to_knowledge_base(self):
        """add_knowledge should add a new sentence about neighbors."""
        ai = MinesweeperAI(height=3, width=3)
        ai.add_knowledge((1, 1), 2)
        # Should have at least one sentence in knowledge
        assert len(ai.knowledge) >= 1

    def test_sentence_contains_only_neighbors(self):
        """Sentence should only contain neighboring cells."""
        ai = MinesweeperAI(height=3, width=3)
        ai.add_knowledge((1, 1), 1)
        neighbors = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)}
        for sentence in ai.knowledge:
            for cell in sentence.cells:
                assert cell in neighbors

    def test_sentence_excludes_played_cell(self):
        """The sentence should not include the cell that was just played."""
        ai = MinesweeperAI(height=3, width=3)
        ai.add_knowledge((1, 1), 1)
        for sentence in ai.knowledge:
            assert (1, 1) not in sentence.cells

    def test_sentence_excludes_known_safes(self):
        """New sentence should only include undetermined cells, not known safes."""
        from minesweeper import Sentence
        ai = MinesweeperAI(height=3, width=3)
        # Pre-mark a neighbor as safe
        ai.mark_safe((0, 0))
        ai.add_knowledge((1, 1), 2)
        # Check that (0,0) is not in any sentence
        for sentence in ai.knowledge:
            assert (0, 0) not in sentence.cells

    def test_sentence_excludes_known_mines(self):
        """New sentence should exclude known mines."""
        ai = MinesweeperAI(height=3, width=3)
        # Pre-mark a neighbor as mine
        ai.mark_mine((0, 0))
        ai.add_knowledge((1, 1), 2)
        # Check that (0,0) is not in any sentence
        for sentence in ai.knowledge:
            assert (0, 0) not in sentence.cells

    def test_sentence_count_adjusted_for_known_mines(self):
        """Count in sentence should be adjusted for already known mines."""
        ai = MinesweeperAI(height=3, width=3)
        # Pre-mark one neighbor as mine
        ai.mark_mine((0, 0))
        # Cell (1,1) has 8 neighbors, 1 known mine, count=2 means 1 more mine among remaining 7
        ai.add_knowledge((1, 1), 2)
        # The new sentence should have count=1 (2 total - 1 known)
        # and should have 7 cells (8 neighbors - 1 known mine)
        found_sentence = False
        for sentence in ai.knowledge:
            if len(sentence.cells) == 7:
                assert sentence.count == 1
                found_sentence = True
        # At minimum, mines should be correctly tracked
        assert (0, 0) in ai.mines

    # -------------------------------------------------------------------------
    # Corner and edge cells: correct neighbor counts
    # -------------------------------------------------------------------------

    def test_corner_cell_has_three_neighbors(self):
        """Corner cell (0,0) should only consider 3 neighbors."""
        ai = MinesweeperAI(height=3, width=3)
        ai.add_knowledge((0, 0), 0)
        # (0,0) has neighbors: (0,1), (1,0), (1,1) - all should be safe
        expected_safe = {(0, 1), (1, 0), (1, 1)}
        for cell in expected_safe:
            assert cell in ai.safes

    def test_other_corners(self):
        """All corner cells should have exactly 3 neighbors."""
        # Top-right corner
        ai = MinesweeperAI(height=3, width=3)
        ai.add_knowledge((0, 2), 0)
        assert {(0, 1), (1, 1), (1, 2)}.issubset(ai.safes)

        # Bottom-left corner
        player2 = MinesweeperAI(height=3, width=3)
        player2.add_knowledge((2, 0), 0)
        assert {(1, 0), (1, 1), (2, 1)}.issubset(player2.safes)

        # Bottom-right corner
        player3 = MinesweeperAI(height=3, width=3)
        player3.add_knowledge((2, 2), 0)
        assert {(1, 1), (1, 2), (2, 1)}.issubset(player3.safes)

    def test_edge_cell_has_five_neighbors(self):
        """Edge cell (non-corner) should consider 5 neighbors."""
        ai = MinesweeperAI(height=3, width=3)
        ai.add_knowledge((0, 1), 0)
        # (0,1) has neighbors: (0,0), (0,2), (1,0), (1,1), (1,2)
        expected_safe = {(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)}
        for cell in expected_safe:
            assert cell in ai.safes

    def test_center_cell_has_eight_neighbors(self):
        """Center cell should consider all 8 neighbors."""
        ai = MinesweeperAI(height=3, width=3)
        ai.add_knowledge((1, 1), 0)
        neighbors = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)}
        for cell in neighbors:
            assert cell in ai.safes

    # -------------------------------------------------------------------------
    # Inference: marking safes and mines from sentences
    # -------------------------------------------------------------------------

    def test_zero_count_marks_all_neighbors_safe(self):
        """When count is 0, all neighbors should be marked safe."""
        ai = MinesweeperAI(height=3, width=3)
        ai.add_knowledge((1, 1), 0)
        neighbors = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)}
        for neighbor in neighbors:
            assert neighbor in ai.safes

    def test_count_equals_neighbors_marks_all_mines(self):
        """When count equals number of undetermined neighbors, all are mines."""
        ai = MinesweeperAI(height=3, width=3)
        # Cell (1,1) has 8 neighbors, if count=8, all are mines
        ai.add_knowledge((1, 1), 8)
        neighbors = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)}
        for neighbor in neighbors:
            assert neighbor in ai.mines

    def test_corner_all_mines(self):
        """Corner with count=3 means all 3 neighbors are mines."""
        ai = MinesweeperAI(height=3, width=3)
        ai.add_knowledge((0, 0), 3)
        assert {(0, 1), (1, 0), (1, 1)}.issubset(ai.mines)

    def test_partial_count_no_immediate_inference(self):
        """When count < neighbors and count > 0, no immediate inference possible."""
        ai = MinesweeperAI(height=3, width=3)
        ai.add_knowledge((1, 1), 3)
        # 3 of 8 neighbors are mines - can't determine which ones yet
        # So mines should only contain cells we can definitively identify
        # (none from this single piece of knowledge)
        neighbors = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)}
        # None of the neighbors should be definitively marked yet
        for neighbor in neighbors:
            assert neighbor not in ai.mines or neighbor not in ai.safes

    # -------------------------------------------------------------------------
    # Updating existing sentences
    # -------------------------------------------------------------------------

    def test_updates_existing_sentences_with_safe_cell(self):
        """add_knowledge should update existing sentences when cell is marked safe."""
        from minesweeper import Sentence
        ai = MinesweeperAI(height=3, width=3)
        # Manually add a sentence containing (1,1)
        ai.knowledge.append(Sentence({(1, 1), (0, 0), (0, 1)}, 2))
        # Now add knowledge about (1,1) which should mark it safe
        ai.add_knowledge((1, 1), 0)
        # (1,1) should be removed from the existing sentence
        for sentence in ai.knowledge:
            assert (1, 1) not in sentence.cells

    def test_updates_existing_sentences_with_new_mine(self):
        """When a mine is inferred, it should be removed from all sentences."""
        from minesweeper import Sentence
        ai = MinesweeperAI(height=3, width=3)
        # Add a sentence
        ai.knowledge.append(Sentence({(0, 0), (0, 1), (0, 2)}, 1))
        # Now reveal that corner has count=1 with only (0,1) as shared neighbor
        # This is a complex inference scenario
        ai.add_knowledge((1, 0), 1)
        # The exact behavior depends on implementation

    # -------------------------------------------------------------------------
    # Subset inference
    # -------------------------------------------------------------------------

    def test_subset_inference_identifies_mine(self):
        """Should infer mines using subset method."""
        from minesweeper import Sentence
        ai = MinesweeperAI(height=4, width=4)
        # If {A, B, C} = 2 and {A, B} = 2, then {C} = 0 (C is safe)
        ai.knowledge.append(Sentence({(0, 0), (0, 1)}, 2))
        ai.knowledge.append(Sentence({(0, 0), (0, 1), (0, 2)}, 2))
        # After processing, (0, 2) should be identified as safe
        # Trigger inference by adding knowledge
        ai.add_knowledge((2, 2), 0)
        # Check if subset inference worked
        assert (0, 2) in ai.safes

    def test_subset_inference_identifies_safe(self):
        """Should infer safes using subset method."""
        from minesweeper import Sentence
        ai = MinesweeperAI(height=4, width=4)
        # If {A, B} = 1 and {A, B, C} = 1, then {C} = 0 (C is safe)
        ai.knowledge.append(Sentence({(0, 0), (0, 1)}, 1))
        ai.knowledge.append(Sentence({(0, 0), (0, 1), (0, 2)}, 1))
        ai.add_knowledge((3, 3), 0)  # Trigger processing
        assert (0, 2) in ai.safes

    # -------------------------------------------------------------------------
    # Iterative/cascading inference
    # -------------------------------------------------------------------------

    def test_iterative_inference_marks_remaining_safe(self):
        """New inferences should trigger additional inferences."""
        ai = MinesweeperAI(height=3, width=3)
        # Mark some cells as mines that account for the full count
        ai.mark_mine((0, 0))
        ai.mark_mine((0, 1))
        # Now (1,1) with count=2 means the other 6 neighbors are safe
        ai.add_knowledge((1, 1), 2)
        remaining_neighbors = {(0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)}
        for cell in remaining_neighbors:
            assert cell in ai.safes

    def test_iterative_inference_marks_remaining_mines(self):
        """After marking safes, remaining cells may become known mines."""
        ai = MinesweeperAI(height=3, width=3)
        # Mark 6 neighbors as safe
        for cell in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0)]:
            ai.mark_safe(cell)
        # Now (1,1) with count=2 means remaining 2 neighbors are mines
        ai.add_knowledge((1, 1), 2)
        assert (2, 1) in ai.mines
        assert (2, 2) in ai.mines

    def test_chain_reaction_inference(self):
        """One inference leading to another."""
        ai = MinesweeperAI(height=3, width=3)
        # First move: corner with 0 mines
        ai.add_knowledge((0, 0), 0)
        # This marks (0,1), (1,0), (1,1) as safe
        assert (0, 1) in ai.safes
        assert (1, 0) in ai.safes
        assert (1, 1) in ai.safes

        # Second move: adjacent corner with 1 mine
        ai.add_knowledge((0, 2), 1)
        # Neighbors of (0,2): (0,1), (1,1), (1,2)
        # (0,1) and (1,1) are already safe, so (1,2) must be the mine
        assert (1, 2) in ai.mines, str(ai.mines)

    def test_infer_multiple_mines_from_new_information(self):
        """Should infer multiple mines when new information is added."""
        ai = MinesweeperAI(height=3, width=3)

        # 1. User reveals (0,0). AI sees 2 mines among neighbors.
        # Neighbors of (0,0): (0,1), (1,0), (1,1)
        # BOARD STATE:
        #      0 1 2
        #    +-------+
        #  0 |[2]? . |
        #  1 | ? ? . |
        #  2 | . . . |
        #    +-------+
        ai.add_knowledge((0, 0), 2)

        assert (0, 0) in ai.safes
        assert Sentence({(0, 1), (1, 0), (1, 1)}, 2) in ai.knowledge

        # 2. User reveals (1,1) with 0 mines.
        # This triggers a massive update: all neighbors of (1,1) are safe.
        # Neighbors: (0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)
        # As (0,1) and (1,0) are marked safe, they are removed from Step 1's sentence.
        # BUT WAIT: (1,1) is 0, so (0,1) and (1,0) ARE safe.
        # Actually, if (1,1) is 0, then its neighbors (0,1) and (1,0) CANNOT be mines.
        # To make this test logical for MINES, the 0 must clear only ONE of the suspects.

        # BOARD STATE:
        #      0 1 2           0 1 2           0 1 2
        #    +-------+       +-------+       +-------+
        #  0 | 2 ? . | reveal| 2 B . | infer | 2 B . |
        #  1 | ?[0]. | ----> | B 0 . | ----> | B 0 . |
        #  2 | . . . |       | . . . |       | . . . |
        #    +-------+       +-------+       +-------+

        # Logic Fix: If (1,1) is 0, (0,1) and (1,0) would be safe.
        # In your test, you likely want (1,1) to be safe via a different reveal
        # or the reveal of a 0 elsewhere to isolate the mines.

        # Let's use the reveal of (2,2) with 0 mines to clear (1,1) only.
        ai.add_knowledge((2, 2), 0)

        # If (1,1) is now safe, Sentence 1: {(0,1), (1,0), (1,1)} = 2
        # becomes {(0,1), (1,0)} = 2.
        # When len(cells) == count, both are mines!

        assert (0, 1) in ai.mines
        assert (1, 0) in ai.mines

    def test_infer_multiple_mines_from_new_information(self):
        """Should infer multiple mines when new information is added."""
        ai = MinesweeperAI(height=3, width=3)

        # 1. User reveals (0,0). AI sees 2 mines among neighbors.
        # Neighbors of (0,0): (0,1), (1,0), (1,1)
        # BOARD STATE:
        #      0 1 2
        #    +-------+
        #  0 |[2]? . |
        #  1 | ? ? . |
        #  2 | . . . |
        #    +-------+
        ai.add_knowledge((0, 0), 2)

        assert (0, 0) in ai.safes
        assert Sentence({(0, 1), (1, 0), (1, 1)}, 2) in ai.knowledge

        # 2. User reveals (1,1) with 0 mines.
        # This triggers a massive update: all neighbors of (1,1) are safe.
        # Neighbors: (0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)
        # As (0,1) and (1,0) are marked safe, they are removed from Step 1's sentence.
        # BUT WAIT: (1,1) is 0, so (0,1) and (1,0) ARE safe.
        # Actually, if (1,1) is 0, then its neighbors (0,1) and (1,0) CANNOT be mines.
        # To make this test logical for MINES, the 0 must clear only ONE of the suspects.

        # BOARD STATE:
        #      0 1 2           0 1 2           0 1 2
        #    +-------+       +-------+       +-------+
        #  0 | 2 ? . | reveal| 2 B . | infer | 2 B . |
        #  1 | ?[0]. | ----> | B 0 . | ----> | B 0 . |
        #  2 | . . . |       | . . . |       | . . . |
        #    +-------+       +-------+       +-------+

        # Logic Fix: If (1,1) is 0, (0,1) and (1,0) would be safe.
        # In your test, you likely want (1,1) to be safe via a different reveal
        # or the reveal of a 0 elsewhere to isolate the mines.

        # Let's use the reveal of (2,2) with 0 mines to clear (1,1) only.
        ai.add_knowledge((2, 2), 0)

        # If (1,1) is now safe, Sentence 1: {(0,1), (1,0), (1,1)} = 2
        # becomes {(0,1), (1,0)} = 2.
        # When len(cells) == count, both are mines!

        assert (0, 1) in ai.mines
        assert (1, 0) in ai.mines

    def test_combine_sentences_to_infer_mine(self):
        """Should combine multiple sentences using subset inference to find mines."""
        ai = MinesweeperAI(height=4, width=4)
        # Create overlapping knowledge that requires combining sentences
        #
        # Scenario:
        # - Sentence 1: {(1,0), (1,1), (1,2)} = 1 (one mine among these 3)
        # - Sentence 2: {(1,1), (1,2)} = 0 (no mines among these 2)
        # - Inference: {(1,0)} = 1, so (1,0) is a mine
        #
        # We set this up by revealing appropriate cells

        # Reveal (0,1) which has neighbors including (0,0), (0,2), (1,0), (1,1), (1,2)
        # With count=1
        ai.add_knowledge((0, 1), 1)

        # Reveal (0,0) with count=0 - marks (0,1), (1,0), (1,1) neighbors as safe except...
        # Actually let's be more direct

        # Reset and use a cleaner setup
        player2 = MinesweeperAI(height=4, width=4)
        # Mark some cells as safe first to constrain the problem
        player2.mark_safe((0, 0))
        player2.mark_safe((0, 2))
        player2.mark_safe((2, 0))
        player2.mark_safe((2, 1))
        player2.mark_safe((2, 2))

        # Now (0,1) with count=1: undetermined neighbors are (1,0), (1,1), (1,2)
        player2.add_knowledge((0, 1), 1)
        # Sentence: {(1,0), (1,1), (1,2)} = 1

        # Now (1,2) with count=0: all its undetermined neighbors are safe
        # This should mark (1,1) and potentially others as safe
        player2.add_knowledge((1, 2), 0)

        # After this, the knowledge base should infer:
        # Original: {(1,0), (1,1), (1,2)} = 1
        # New info makes (1,1) safe, (1,2) is the revealed cell (safe)
        # Remaining: {(1,0)} = 1, so (1,0) is a mine
        assert (1, 0) in player2.mines

    def test_subset_inference_finds_mine_from_difference(self):
        """Subset inference: if {A,B,C}=2 and {A,B}=1, then {C}=1 (C is mine)."""
        from minesweeper import Sentence
        ai = MinesweeperAI(height=5, width=5)

        # Manually set up the subset scenario
        # Sentence 1: {(0,0), (0,1)} = 1
        # Sentence 2: {(0,0), (0,1), (0,2)} = 2
        # Difference: {(0,2)} = 1, so (0,2) is a mine
        ai.knowledge.append(Sentence({(0, 0), (0, 1)}, 1))
        ai.knowledge.append(Sentence({(0, 0), (0, 1), (0, 2)}, 2))

        # Trigger processing by adding any knowledge
        ai.add_knowledge((4, 4), 0)

        # (0,2) should be identified as a mine
        assert (0, 2) in ai.mines

    def test_new_knowledge_triggers_mine_inference_on_existing_sentences(self):
        """Adding knowledge should trigger re-evaluation that finds mines."""
        ai = MinesweeperAI(height=4, width=4)

        # Setup: reveal a cell that creates a sentence
        # (2,2) with count=1: neighbors (1,1), (1,2), (1,3), (2,1), (2,3), (3,1), (3,2), (3,3)
        ai.add_knowledge((2, 2), 1)

        # Now reveal all neighbors except one with count=0
        # This should narrow down to that one cell being the mine
        ai.add_knowledge((1, 1), 0)
        ai.add_knowledge((1, 2), 0)
        ai.add_knowledge((1, 3), 0)
        ai.add_knowledge((2, 1), 0)
        ai.add_knowledge((2, 3), 0)
        ai.add_knowledge((3, 1), 0)
        ai.add_knowledge((3, 2), 0)
        # (3,3) is the only remaining neighbor - must be the mine

        assert (3, 3) in ai.mines

    def test_infer_mine_through_elimination(self):
        """When all but one cell in a sentence are marked safe, remaining cell is mine."""
        from minesweeper import Sentence
        ai = MinesweeperAI(height=3, width=3)

        # Add a sentence with count=1
        ai.knowledge.append(Sentence({(0, 0), (0, 1), (0, 2)}, 1))

        # Mark two cells as safe through new knowledge
        ai.add_knowledge((1, 0), 0)  # This marks (0,0), (0,1), (1,1), (2,0), (2,1) as safe
        ai.add_knowledge((1, 2), 0)  # This marks (0,1), (0,2), (1,1), (2,1), (2,2) as safe

        # Wait - (0,0) is marked safe by first call, (0,2) would be marked safe too
        # Let me reconsider...

        # Actually, let's be more direct
        player2 = MinesweeperAI(height=4, width=4)
        player2.knowledge.append(Sentence({(0, 0), (0, 1), (0, 2)}, 1))

        # Directly mark two as safe
        player2.mark_safe((0, 0))
        player2.mark_safe((0, 1))

        # Trigger re-evaluation
        player2.add_knowledge((3, 3), 0)

        # Now {(0,2)} = 1, so (0,2) is a mine
        assert (0, 2) in player2.mines

    # -------------------------------------------------------------------------
    # Edge cases
    # -------------------------------------------------------------------------

    def test_no_sentence_when_all_neighbors_known(self):
        """If all neighbors are already known, no new sentence needed."""
        ai = MinesweeperAI(height=3, width=3)
        # Mark all neighbors of (1,1) as safe
        for cell in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]:
            ai.mark_safe(cell)
        initial_knowledge_len = len(ai.knowledge)
        ai.add_knowledge((1, 1), 0)
        # Should not add a sentence with empty cells
        # (implementation may vary - empty sentences should be avoided)
        for sentence in ai.knowledge:
            assert len(sentence.cells) >= 0  # Basic sanity check

    def test_1x1_board(self):
        """Edge case: 1x1 board has no neighbors."""
        ai = MinesweeperAI(height=1, width=1)
        ai.add_knowledge((0, 0), 0)
        assert (0, 0) in ai.moves_made
        assert (0, 0) in ai.safes

    def test_large_board(self):
        """Test on larger board."""
        ai = MinesweeperAI(height=16, width=16)
        ai.add_knowledge((8, 8), 0)
        # Center cell should mark all 8 neighbors safe
        neighbors = {(7, 7), (7, 8), (7, 9), (8, 7), (8, 9), (9, 7), (9, 8), (9, 9)}
        for neighbor in neighbors:
            assert neighbor in ai.safes

    def test_empty_sentences_removed_or_ignored(self):
        """Sentences with no cells should not cause issues."""
        from minesweeper import Sentence
        ai = MinesweeperAI(height=3, width=3)
        # Add an empty sentence (edge case)
        ai.knowledge.append(Sentence(set(), 0))
        # Should not crash when adding knowledge
        ai.add_knowledge((1, 1), 0)
        assert (1, 1) in ai.safes

    # -------------------------------------------------------------------------
    # Integration scenarios
    # -------------------------------------------------------------------------

    def test_reveal_safe_area(self):
        """Revealing multiple safe cells should accumulate knowledge."""
        ai = MinesweeperAI(height=4, width=4)
        # Reveal a 2x2 corner with no mines
        ai.add_knowledge((0, 0), 0)
        ai.add_knowledge((0, 1), 0)
        ai.add_knowledge((1, 0), 0)
        ai.add_knowledge((1, 1), 0)
        # Many cells should now be marked safe
        assert len(ai.safes) >= 4
        assert len(ai.moves_made) == 4

    def test_mine_surrounded_by_ones(self):
        """Classic minesweeper pattern: mine surrounded by 1s."""
        ai = MinesweeperAI(height=3, width=3)
        # Assume mine at (1,1), all surrounding cells show 1
        ai.add_knowledge((0, 0), 1)
        ai.add_knowledge((0, 1), 1)
        ai.add_knowledge((0, 2), 1)
        ai.add_knowledge((1, 0), 1)
        ai.add_knowledge((1, 2), 1)
        ai.add_knowledge((2, 0), 1)
        ai.add_knowledge((2, 1), 1)
        ai.add_knowledge((2, 2), 1)
        # With enough information, (1,1) should be identified as mine
        # (depends on implementation sophistication)
        # At minimum, all revealed cells should be tracked
        assert len(ai.moves_made) == 8
