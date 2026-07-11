---
paths:
  - "src/**/*.py"
---

# Docstrings

**Write docstrings in the basic Sphinx format. Apply these rules strictly whenever code is written or edited.**

Format (not NumPy, not Google):

```
"""First line explaining the main goal.

If needed, a short paragraph explaining how it works. Keep it as short as possible — only mandatory information.

:Example: (only for functions and methods, only if genuinely useful)
    >>>

:param parameter: explain the purpose or why it is required.
:returns: ...
:raises ExceptionType: ...
"""
```

Rules:
- **No subject pronoun.** Never write "this function", "this method", "this class". Prefer the implicit subject: "Initializes the application", not "This function initializes the application". Applies to all descriptions, including `:param`, `:returns:`, `:raises:`.
- **Third-person singular verb** for every function/method first line: "Sums the elements", not "Sum the elements".
- **Lowercase** for all `:param`, `:returns:`, and `:raises:` descriptions.
- **Short first line** capturing the general behaviour. One sentence only.
- **Module docstrings** as short as possible. Do not enumerate the module's contents unless strictly necessary.
- **No redundancy.** Do not repeat what the code or the name already says clearly.
- Add a `:Example:` block only when the usage is non-obvious.
