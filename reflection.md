# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

It looked like any other guessing game. Nothing seemed wrong with it. But when I started playing I got a lot of different bugs.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

The hints were backwards and the history was wierd.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 1 | Go Lower | Go higher | no error |
| 16 | go higher | go lower | no error| 
| start new game | start a new game with new number | it doesnt | no error|

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

To fix the scoring system


- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

None really



---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I would see the fixes suggested and see if it makes sense to me and ran teh game after

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  I really jut ran the game and did no tests
- Did AI help you design or understand any tests? How?

yes it did help me build new edge cases testing and make sure everything

Summary
Refactor — moved the four logic functions to their right place:

get_range_for_difficulty, parse_guess, check_guess, update_score now live in logic_utils.py (no more NotImplementedError stubs).
app.py imports them at the top and keeps only the Streamlit UI code.
Bug fixes applied along the way:

Backwards hints — "Too High" now says "📉 Go LOWER!" and "Too Low" says "📈 Go HIGHER!" (logic_utils.py:43-46).
New Game button — now resets status, score, and history (not just attempts/secret) and uses the difficulty's range instead of hardcoded 1-100 (app.py). This was the reason it appeared dead after a win/loss.
String-comparison glitch — removed the str(secret) conversion on even attempts, so comparisons are always int-vs-int (app.py).
Attempts off-by-one — initial attempts is now 0, so "Attempts left" reads correctly.
Hardcoded range text — the info banner now shows the actual {low}–{high} for the difficulty.
Inconsistent scoring — "Too High" and "Too Low" now both apply a flat −5 (the old code randomly gave +5 on some "Too High" guesses).
Verified: both files parse, the import resolves, and assertions confirm ranges, parsing, correct hint directions, and scoring all behave.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Imagine your Streamlit app is a script that gets executed from top to bottom every time the user interacts with it.

For example, if a user:

clicks a button,
types in a text box,
changes a slider,

Streamlit doesn't just run the code related to that widget—it reruns the entire script.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?

Plan ahead and have a olution design then fix

  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?

Maybe tell it to tell me what each fix is supposed to do before recommdening it

- In one or two sentences, describe how this project changed the way you think about AI generated code.

I should never take it for granted and use differnt models to evaluate it
