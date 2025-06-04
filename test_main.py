import pytest
from main import Chess


def test_generate_moves_not_empty():
    cs = Chess('settings.json')
    moves = cs.generate_moves()
    assert len(moves) > 0


def test_contains_pawn_a2_to_a3():
    cs = Chess('settings.json')
    moves = cs.generate_moves()
    assert any(m['source'] == 81 and m['target'] == 71 for m in moves)
