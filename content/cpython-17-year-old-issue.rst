Fixing a 17-Year-Old CPython Issue
###################################
:date: 2025-12-12 00:00:00
:tags: Python, CPython, Open Source, readline, C, Contributing
:summary: How I picked up a CPython issue from 2008, wrote a C extension patch, and got it merged into Python's stdlib 17 years later.
:status: published
:lang: en
:author: Sanyam Khurana
:category: Technical
:slug: cpython-17-year-old-issue

**TL;DR:** I fixed `a CPython issue <https://github.com/python/cpython/issues/48752>`_ that had been open since **December 2008**. The patch adds ``readline.get_pre_input_hook()`` to Python's standard library. It was reviewed by Victor Stinner and merged into CPython in December 2025.

----

The Issue
*********

Back in December 2008, a developer named Conrad Irwin `opened a feature request <https://bugs.python.org/issue4502>`_ on Python's bug tracker. The ask was simple: Python's ``readline`` module had ``set_pre_input_hook()`` to register a callback, but no way to **retrieve** the current hook. If you wanted to temporarily override the hook and restore it later, you were out of luck.

The original issue even came with a patch. A diff against ``Modules/readline.c``. Clean, focused, and ready to go.

And then... nothing. For **17 years**.

The issue sat there. It migrated from ``bugs.python.org`` (the old Roundup tracker) to GitHub when CPython moved its issue tracking. It collected dust. Not because it was controversial or hard, but because nobody picked it up.

----

Why I Picked It Up
******************

I've been a `CPython contributor <https://github.com/python/cpython/commits?author=CuriousLearner>`_ for a while, and I keep an eye on older issues that have clear value but just need someone to do the work. This one caught my attention because:

1. **The use case was real.** Any application that wraps ``readline`` (think custom REPLs, debugging tools, or CLI frameworks) might need to save and restore hooks. Without a getter, you're either stomping on someone else's hook or maintaining your own shadow state.

2. **The API gap was obvious.** Python's ``readline`` module already had ``get_startup_hook()`` paired with ``set_startup_hook()``. But ``set_pre_input_hook()`` had no matching getter. It was just... missing.

3. **The fix was well-scoped.** No design debates needed. No deprecations. No backwards compatibility concerns. Just add the getter function.

----

The Patch
*********

The change touched five files:

**1. The C implementation** (``Modules/readline.c``)

This is where the actual function lives. The implementation is straightforward: look up the stored hook in the module state and return it (or ``None`` if no hook is set).

.. code-block:: c

    static PyObject *
    readline_get_pre_input_hook_impl(PyObject *module)
    {
        readlinestate *state = get_readline_state(module);
        if (state->pre_input_hook == NULL) {
            Py_RETURN_NONE;
        }
        return Py_NewRef(state->pre_input_hook);
    }

Nothing fancy. But if you've never worked with CPython internals, a few things stand out:

- ``get_readline_state(module)`` retrieves the module's internal state. CPython modules store their state in a struct rather than global variables (this matters for sub-interpreters and free-threading).
- ``Py_NewRef()`` increments the reference count before returning. If you forget this, you get a use-after-free. If you do it wrong, you get a memory leak. Reference counting is the thing that makes C extension work feel like defusing a bomb.
- ``Py_RETURN_NONE`` is a macro that increments ``None``'s refcount and returns it. Yes, even ``None`` is reference-counted.

**2. Argument Clinic** (``Modules/clinic/readline.c.h``)

CPython uses `Argument Clinic <https://devguide.python.org/development-tools/clinic/>`_, a preprocessor that auto-generates argument parsing boilerplate from a DSL. You write a short spec in a comment block:

.. code-block:: c

    /*[clinic input]
    readline.get_pre_input_hook

    Get the current pre-input hook function.
    [clinic start generated code]*/

And Clinic generates the ``PyMethodDef`` entry, the docstring, and the wrapper function. It's one of those things that makes contributing to CPython less painful than you'd expect.

**3. Tests** (``Lib/test/test_readline.py``)

Every CPython patch needs tests. The test covers the basics: no hook set returns ``None``, setting a hook and retrieving it returns the same function object.

.. code-block:: python

    def test_get_pre_input_hook(self):
        original_hook = readline.get_pre_input_hook()
        self.addCleanup(readline.set_pre_input_hook, original_hook)

        readline.set_pre_input_hook(None)
        self.assertIsNone(readline.get_pre_input_hook())

        def my_hook():
            pass

        readline.set_pre_input_hook(my_hook)
        self.assertIs(readline.get_pre_input_hook(), my_hook)

Note the ``addCleanup`` call. Always restore state in tests, especially when you're poking at module-level singletons.

**4. Documentation** (``Doc/library/readline.rst``)

Added the function signature and description to the official docs, with a ``.. versionadded:: next`` directive (which gets replaced with the actual version number at release time).

**5. NEWS entry** (``Misc/NEWS.d/...``)

CPython uses `blurb <https://github.com/python/blurb>`_ for changelogs. Each change gets a small ``.rst`` file in ``Misc/NEWS.d/`` that gets compiled into the final changelog.

----

The Review
**********

The PR was reviewed by `Victor Stinner <https://github.com/vstinner>`_, one of CPython's most active core developers. There were a couple of rounds of feedback, mostly around the implementation details. The whole process, from opening the PR to getting it merged, took about three weeks. Not bad for a 17-year-old issue.

----

What I Learned (Again)
***********************

I've contributed to CPython before, but every patch reinforces the same lessons:

**Old issues are gold.** The bug tracker is full of valid, well-scoped issues that just need someone to show up. You don't need to find a new problem. Sometimes the best contribution is finishing what someone else started.

**The CPython codebase is more approachable than people think.** Yes, it's C. Yes, reference counting is tricky. But the patterns are consistent, Argument Clinic handles the boilerplate, and the `devguide <https://devguide.python.org/>`_ walks you through every step.

**Small patches matter.** This wasn't a new feature that'll make headlines. It's a getter function. But it fills a real gap, and every Python developer who builds a custom REPL or CLI tool might benefit from it. Not every contribution needs to be a PEP.

----

If you've been thinking about contributing to CPython, don't wait for the perfect issue. Find something old, something simple, something useful. And just start.

The `CPython Developer Guide <https://devguide.python.org/>`_ is your friend.

You can find `the full PR here <https://github.com/python/cpython/pull/141586>`_.


`CuriousLearner <https://www.github.com/CuriousLearner>`_
