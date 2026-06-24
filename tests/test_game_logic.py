import pytest

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "difficulty, expected",
    [
        ("Easy", (1, 20)),
        ("Normal", (1, 100)),
        ("Hard", (1, 50)),
    ],
)
def test_range_known_difficulties(difficulty, expected):
    assert get_range_for_difficulty(difficulty) == expected


def test_range_unknown_defaults_to_normal():
    # Anything unexpected should fall back to the 1-100 default.
    assert get_range_for_difficulty("Impossible") == (1, 100)
    assert get_range_for_difficulty("") == (1, 100)


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

def test_parse_valid_integer():
    assert parse_guess("42") == (True, 42, None)


def test_parse_negative_integer():
    assert parse_guess("-5") == (True, -5, None)


def test_parse_zero():
    assert parse_guess("0") == (True, 0, None)


def test_parse_surrounding_whitespace():
    # int() tolerates surrounding whitespace.
    assert parse_guess("  7  ") == (True, 7, None)


def test_parse_float_string_truncates_toward_zero():
    assert parse_guess("3.9") == (True, 3, None)
    assert parse_guess("3.0") == (True, 3, None)
    assert parse_guess("-3.9") == (True, -3, None)


def test_parse_none_is_rejected():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_empty_string_is_rejected():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


@pytest.mark.parametrize("bad", ["abc", "1.2.3", "five", "--3", "12a", "."])
def test_parse_non_numeric_is_rejected(bad):
    ok, value, err = parse_guess(bad)
    assert ok is False
    assert value is None
    assert err == "That is not a number."


# ---------------------------------------------------------------------------
# check_guess  (returns a (outcome, message) tuple)
# ---------------------------------------------------------------------------

def test_check_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_check_too_high_points_player_lower():
    # Regression: a guess above the secret must tell the player to go LOWER.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message
    assert "HIGHER" not in message


def test_check_too_low_points_player_higher():
    # Regression: a guess below the secret must tell the player to go HIGHER.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message
    assert "LOWER" not in message


def test_check_off_by_one_boundaries():
    assert check_guess(51, 50)[0] == "Too High"
    assert check_guess(49, 50)[0] == "Too Low"


def test_check_is_purely_numeric_no_string_glitch():
    # The old bug stringified the secret, making "9" > "85" lexicographically.
    # With integers, 9 is correctly below 85.
    assert check_guess(9, 85)[0] == "Too Low"
    assert check_guess(100, 9)[0] == "Too High"


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

def test_win_score_first_attempt():
    # attempt_number 0 -> 100 - 10*(0+1) = 90
    assert update_score(0, "Win", 0) == 90


def test_win_score_adds_to_existing_total():
    assert update_score(25, "Win", 0) == 115


def test_win_score_floors_at_ten():
    # Large attempt numbers would compute <= 10, so the floor applies.
    assert update_score(0, "Win", 9) == 10
    assert update_score(0, "Win", 20) == 10


def test_win_score_just_above_floor():
    # attempt 7 -> 100 - 80 = 20 (still above the floor)
    assert update_score(0, "Win", 7) == 20


def test_too_high_penalizes_five_regardless_of_attempt_parity():
    # Regression: the old code randomly awarded +5 on even attempts.
    assert update_score(100, "Too High", 1) == 95
    assert update_score(100, "Too High", 2) == 95
    assert update_score(100, "Too High", 3) == 95


def test_too_low_penalizes_five():
    assert update_score(100, "Too Low", 1) == 95
    assert update_score(100, "Too Low", 2) == 95


def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(42, "Mystery", 3) == 42
