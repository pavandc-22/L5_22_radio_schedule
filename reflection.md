# Reflection

(The handout lists reflection questions without the wording, so these answer the standard four for this lab.)

**1. Which issues were the easiest and which the hardest to fix?**
Style issues (naming, docstrings, line length) were easiest because the tools say exactly what to change. The hardest was `eval`: just deleting it breaks `overlap_free`, so I had to write a small `ast`-based evaluator that keeps the same behaviour for inputs like `"7 + 1 <= 13"` while rejecting anything unsafe.

**2. Did the tools report any false positives, or miss anything?**
Bandit's hardcoded-password warning (B105) was valid here, even though the variable was never used, because the secret would still be in the repo history. The tools did not directly flag the logic bug where `booked_minutes` was never reduced by `removeSlot`; I found that by reading the code after Pylint pointed at the `global` statement. Static analysis points you to suspicious places but does not replace review.

**3. How could these tools be integrated into a real workflow?**
Run Flake8 and Pylint as pre-commit hooks and in CI on every pull request, and fail the build on Bandit Medium/High findings or a Pylint score below a threshold (e.g. 9.5). This catches problems before code review so reviewers can focus on design and logic.

**4. What tangible improvements did you see in the code?**
Pylint went from 2.41 to 10.00, Bandit from 3 findings to 0, and Flake8 from 4 to 0. More importantly, the code is safer (no SQL injection, no `eval`, no secret in source), more predictable (no global state), more readable (consistent names and docstrings), and importable without side effects.
