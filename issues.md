# Issues Found – radio_schedule.py (SRN PES1UG24AM383)

Before: Pylint 2.41/10, Bandit 3 issues (1 Low, 2 Medium), Flake8 4 issues.
After: Pylint 10.00/10, Bandit 0 issues, Flake8 0 issues.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection (B608) | Security (Medium) | 11 | `addSlot` built the INSERT with `%` string formatting, so a show/host name like `x'); DROP TABLE slots;--` is executed as SQL. | Used a parameterised query: `VALUES (?, ?, ?, ?)` with a values tuple. |
| Use of `eval` (B307 / W0123) | Security (Medium) | 21 | `overlapFree` ran `eval()` on a caller-supplied string, allowing arbitrary code execution. | Replaced with an `ast`-based evaluator that only allows numbers, `+ - * /` and comparisons; anything else returns False. |
| Hardcoded password (B105) | Security (Low) | 5 | `STUDIO_PASSWORD = "onair2024"` stored a secret in source control. | Read it from the `STUDIO_PASSWORD` environment variable via `os.environ.get`. |
| Broad exception (W0718) | Bug / Quality | 22 | `except Exception` swallowed every error, hiding real bugs. | Catch only `SyntaxError`, `ValueError`, `ZeroDivisionError`. |
| Global state out of sync | Bug | 6, 10, 12, 27 | `booked_minutes` was a global that `removeSlot` never decremented, and `morningShows` returned `[]` whenever it was 0, so results could be wrong after removing slots. | Removed the global; `morning_shows` now simply queries the database, the single source of truth. |
| Naming (C0103) | Style | 6, 9, 15, 19, 26, 31 | camelCase function names and a non-constant global name. | Renamed to `add_slot`, `slot_label`, `overlap_free`, `morning_shows`, `remove_slot`. |
| Missing docstrings (C0114/C0116) | Documentation | 1, 9, 15, 19, 26, 31, 35 | No module or function docstrings. | Added a docstring to the module and each function. |
| f-string (C0209) | Style | 11, 16 | `%` and `.format()` used where f-strings are clearer. | Used an f-string in `slot_label`; the SQL line became parameterised. |
| Multiple statements (E701 / C0321) | Style | 27 | `if ...: return ...` on a single line. | Removed with the rewrite of `morning_shows` (split across lines). |
| Line too long (E501 / C0301) | Style | 4, 11, 27 | Lines of 118, 135 and 110 characters (limit 79). | Wrapped long strings and calls across lines. |
| Code runs on import | Design | 43 | `main()` was called at module level, so importing the file ran the demo. | Added `if __name__ == "__main__":` guard. |
