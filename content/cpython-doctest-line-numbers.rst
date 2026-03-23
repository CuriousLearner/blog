Fixing Doctest's "line None" Problem
#####################################
:date: 2025-12-13 00:00:00
:tags: Python, CPython, Open Source, doctest, Debugging, Contributing
:summary: How I fixed a 10-year-old CPython bug that made doctest report "line None" for __test__ dictionary strings, making failures nearly impossible to locate.
:status: published
:lang: en
:author: Sanyam Khurana
:category: Technical
:slug: cpython-doctest-line-numbers

**TL;DR:** I fixed `a CPython bug <https://github.com/python/cpython/issues/69113>`_ that had been open since **August 2015**. When doctests were defined in a module's ``__test__`` dictionary as triple-quoted strings, Python would report ``"line None"`` on failure. No line number. No way to find the failing test without manually hunting through the file. The fix landed in CPython in December 2025.

----

The Bug
*******

Python's ``doctest`` module lets you define tests in a module's ``__test__`` dictionary:

.. code-block:: python

    __test__ = {
        'basic_math': """
        >>> 2 + 2
        4
        >>> 3 * 7
        21
        """,
    }

This is a perfectly valid way to organize doctests, especially when you want to test things that don't naturally belong in a function's docstring. The problem? When one of these tests failed, you'd see something like this:

.. code-block:: text

    File "my_module.py", line None, in my_module.__test__.basic_math
    Failed example:
        2 + 2
    Expected:
        5
    Got:
        4

``line None``. That's it. No line number. In a small file, you can eyeball it. In a large module with multiple ``__test__`` entries, you're scrolling and guessing.

This issue was `first reported in 2015 <https://bugs.python.org/issue24925>`_ on the old ``bugs.python.org`` tracker. R. David Murray (bitdancer), one of CPython's core developers, even uploaded a patch back then. Another contributor uploaded a fix in 2018. A `PR was opened in 2019 <https://github.com/python/cpython/pull/17553>`_. But nothing made it through to merge. Ten years of "someone should fix this."

----

Why It Was Tricky
*****************

The ``doctest`` module already knows how to find line numbers for most things. Functions, classes, methods: it inspects the object, looks up the source, and matches the ``def`` or ``class`` line. Straightforward.

But ``__test__`` dictionary values are just strings. Python doesn't track where a string literal was defined in the source file. There's no ``__line__`` attribute on a ``str``. So ``_find_lineno`` (the internal method responsible for this) would hit its fallback case and return ``None``.

The challenge is: how do you figure out where a string lives in the source file, when Python itself doesn't tell you?

----

The Fix
*******

The approach is a search-and-match strategy. Take a non-blank line from the test string, find it in the source file, and verify that the surrounding lines match too (to handle duplicates).

Here's the core logic added to ``Lib/doctest.py``:

.. code-block:: python

    if isinstance(obj, str) and source_lines is not None:
        obj_lines = obj.splitlines(keepends=True)
        # Skip the first line (may be on same line as opening quotes)
        # and any blank lines to find a meaningful line to match.
        start_index = 1
        while (start_index < len(obj_lines)
               and not obj_lines[start_index].strip()):
            start_index += 1
        if start_index < len(obj_lines):
            target_line = obj_lines[start_index]
            for lineno, source_line in enumerate(source_lines):
                if source_line == target_line:
                    # Verify subsequent lines also match
                    for i in range(start_index + 1, len(obj_lines) - 1):
                        source_idx = lineno + i - start_index
                        if source_idx >= len(source_lines):
                            break
                        if obj_lines[i] != source_lines[source_idx]:
                            break
                    else:
                        return lineno - start_index

A few things worth noting:

**Why skip the first line?** Because triple-quoted strings often start on the same line as the opening ``"""``. The first "line" of the string might be empty or might share a source line with the dictionary key. Starting from the second line gives a cleaner match.

**Why verify subsequent lines?** Because a line like ``>>> x = 1`` could appear in multiple test entries. By checking that the lines *after* the match also correspond, we avoid false positives. This is especially important when a module has several ``__test__`` entries with similar content.

**Why use** ``splitlines(keepends=True)`` **?** The source lines include their newline characters. If we stripped them during splitting, the comparison would fail on every line. Small detail, easy to get wrong.

----

The Tests
*********

The patch includes two test cases:

**1. Basic line number detection:** Create a module with a ``__test__`` dictionary, run the doctest finder, and verify that the reported line number is not ``None`` and points to the right place.

**2. Multi-line matching with duplicates:** Two ``__test__`` entries that share the same first line (``>>> x = 1``) but differ later. The test verifies that each entry gets a *different* line number, confirming that the multi-line matching logic works.

The existing test suite also needed updates. Several expected outputs in ``test_DocTestSuite_errors`` and ``test_testmod_errors`` previously asserted ``line None`` or ``line ?``. Those now assert actual line numbers like ``line 37`` and ``line 39``. Seeing those assertions change from ``None`` to real numbers was satisfying.

----

The Review
**********

The PR was reviewed by `R. David Murray <https://github.com/bitdancer>`_ (bitdancer), who had originally uploaded a patch for this same issue back in 2015. We went back and forth on the approach and some style nits, and after a few iterations, he approved it.


----

The Before and After
********************

**Before:**

.. code-block:: text

    File "sample.py", line None, in sample.__test__.bad
    Failed example:
        2 + 2

**After:**

.. code-block:: text

    File "sample.py", line 37, in sample.__test__.bad
        >>> 2 + 2
    Failed example:
        2 + 2

A small change in the output. A big difference when you're debugging a failing test suite at midnight.

----

Takeaways
*********

**"line None" was a papercut, not a showstopper.** Nobody's production was down because of this. But thousands of developers hit this annoyance over the years and silently worked around it. Fixing papercuts matters.

**The fix was already attempted multiple times.** A patch in 2015, another in 2018, a PR in 2019. Sometimes the hard part isn't writing the code. It's shepherding it through review, keeping it rebased, and showing up until it lands.

**String matching as a fallback is pragmatic, not perfect.** In theory, a test string could be constructed dynamically and never appear in the source file. The fix handles the common case (triple-quoted string literals) and gracefully falls back to ``None`` for everything else. Perfect is the enemy of shipped.

You can find `the full PR here <https://github.com/python/cpython/pull/141624>`_.


`CuriousLearner <https://www.github.com/CuriousLearner>`_
