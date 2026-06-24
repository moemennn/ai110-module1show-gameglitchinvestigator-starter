# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.**

  A number-guessing game built with Streamlit. The app picks a secret number within a range that depends on the chosen difficulty (Easy 1–20, Normal 1–100, Hard 1–50). The player submits guesses and gets a "higher/lower" hint after each one, has a limited number of attempts, and earns a score based on how quickly they win.

- [x] **Detail which bugs you found.**

  1. **Backwards hints** — `check_guess` told the player to "Go HIGHER!" when their guess was *too high*, and "Go LOWER!" when it was *too low* (the messages were swapped).
  2. **New Game button didn't work** — it only reset `attempts` and `secret`. Because `status` was never reset, the game stayed in the "won"/"lost" state and immediately stopped after a new game. It also left the old `score`/`history` and hardcoded the range to `1–100` regardless of difficulty.
  3. **Secret number "had commitment issues"** — on every even-numbered attempt the secret was converted to a string (`str(secret)`), so an `int` guess was compared against a `str`. This produced wrong/lexicographic comparisons (e.g. `"9" > "85"`) and inconsistent hints.
  4. **Attempts off-by-one** — `attempts` started at `1` instead of `0`, so "Attempts left" was always one short.
  5. **Hardcoded range text** — the guess prompt always said "between 1 and 100" even on Easy/Hard.
  6. **Inconsistent scoring** — `update_score` randomly *added* 5 points on some "Too High" guesses (based on attempt parity) instead of applying a consistent penalty.
  7. **Logic in the wrong file** — all four logic functions lived in `app.py` while `logic_utils.py` held only `NotImplementedError` stubs.
  8. **Broken tests** — the existing tests compared `check_guess`'s `(outcome, message)` tuple against a bare string, so they failed.

- [x] **Explain what fixes you applied.**

  1. Fixed the hint directions: "Too High" → "📉 Go LOWER!", "Too Low" → "📈 Go HIGHER!".
  2. Made New Game reset `attempts`, `secret`, `score`, `status`, and `history`, and draw the new secret from the current difficulty's range.
  3. Removed the `str(secret)` conversion so comparisons are always integer-vs-integer.
  4. Initialized `attempts` at `0` to fix the "Attempts left" count.
  5. Used the actual `{low}`–`{high}` range in the guess prompt.
  6. Made `update_score` apply a flat −5 penalty for both "Too High" and "Too Low".
  7. Moved `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` into `logic_utils.py` and imported them into `app.py`, separating game logic from the UI.
  8. Fixed the existing tests and expanded the suite to 29 tests covering all four functions, their edge cases, and regression checks for each bug above.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User enters a guess of 50
2. Game returns "Too Low"
3. User enters a guess of 75 → "Too High"
4. Score updates correctly after each guess
5. Game ends after the correct guess

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
================================================================= test session starts =================================================================
platform darwin -- Python 3.11.13, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/moemen/Desktop/AI110/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.14.0
collected 29 items                                                                                                                                    

tests/test_game_logic.py .............................                                                                                          [100%]

================================================================= 29 passed in 0.04s ==================================================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
