Teaching getpass How to Handle Keyboard Shortcuts
#################################################
:date: 2026-03-31 00:00:00
:tags: Python, CPython, Open Source, getpass, Terminal, Contributing
:summary: How I fixed keyboard shortcuts in Python's getpass module when using echo_char, turning a raw character reader into a proper line editor.
:status: published
:lang: en
:author: Sanyam Khurana
:category: Technical
:slug: cpython-getpass-keyboard-shortcuts

**TL;DR:** Python 3.14 added ``echo_char`` support to ``getpass.getpass()``, letting you show ``***`` as you type a password. But it broke keyboard shortcuts like Ctrl+U, Ctrl+W, and Ctrl+A. I `fixed it <https://github.com/python/cpython/pull/141597>`_ by building a small line editor that reads the terminal's own control character mappings and handles them in non-canonical mode.

----

The Problem
***********

Python 3.14 introduced a nice quality-of-life feature for ``getpass``: the ``echo_char`` parameter. Instead of typing into a void, you could do:

.. code-block:: python

    password = getpass.getpass(echo_char='*')

And see ``***`` appear as you type. Great for UX. But there was a catch.

When ``echo_char`` is set, the terminal gets switched to **non-canonical mode**. To understand why that matters, a quick detour on how Unix terminals work.

Unix terminals operate in two modes:

- **Canonical mode** (the default): The terminal driver handles line editing for you. It buffers input until you press Enter, and shortcuts like Ctrl+U (clear line), Ctrl+W (delete word), and backspace just work. Your application never sees the raw keystrokes; it only receives the finished line. This is what happens when you call ``input()`` or ``getpass()`` without ``echo_char``.

- **Non-canonical mode**: The terminal sends every keystroke to your application immediately, one character at a time. No buffering, no line editing, no special handling. Ctrl+U doesn't clear the line; it arrives as the byte ``\x15``. Your application is on its own.

``getpass`` needs non-canonical mode when ``echo_char`` is set because it has to intercept each keystroke, suppress the real character, and print ``*`` instead. You can't do that in canonical mode since the terminal would buffer everything and only hand you the final string.

But here's the trade-off: the moment you switch to non-canonical mode, you lose all the line editing that the terminal was doing for free.

The original implementation only handled backspace and Ctrl+C. Everything else was swallowed or, worse, inserted as garbage into the password. Type ``wrongpassword``, hit Ctrl+U to clear it, type the right one, and you'd end up with ``wrongpassword\x15rightpassword``.

The `issue <https://github.com/python/cpython/issues/138577>`_ was filed in September 2025, shortly after the echo_char feature shipped.

----

What Needed to Happen
*********************

The fix had to do what the terminal normally does, but in Python. That means supporting:

- **Ctrl+A** / **Ctrl+E**: Move cursor to start/end of line
- **Ctrl+U**: Kill entire line
- **Ctrl+K**: Kill from cursor to end of line
- **Ctrl+W**: Erase previous word
- **Ctrl+V**: Literal next (insert the next character raw, even if it's a control character)
- **Backspace/DEL**: Delete character before cursor

And crucially, these mappings shouldn't be hardcoded. Different terminals can remap control characters via ``termios`` settings. If someone has remapped their kill character from Ctrl+U to something else, the fix should respect that.

----

The Implementation
******************

The patch started small and grew. The reviewer, `Bénédikt Tran <https://github.com/picnixz>`_ (picnixz), pushed for a cleaner architecture early on, suggesting a dispatcher-based approach instead of a chain of ``if/elif`` statements. That feedback shaped the final design.

The core of the fix is a ``_PasswordLineEditor`` class that manages cursor position, character insertion, and control character dispatch:

.. code-block:: python

    class _PasswordLineEditor:
        def __init__(self, stream, echo_char, ctrl_chars, prompt=""):
            self.stream = stream
            self.echo_char = echo_char
            self.prompt = prompt
            self.password = []
            self.cursor_pos = 0
            self.eof_pressed = False
            self.literal_next = False
            self.ctrl = ctrl_chars
            self.dispatch = {
                ctrl_chars['SOH']: self.handle_move_start,      # Ctrl+A
                ctrl_chars['ENQ']: self.handle_move_end,        # Ctrl+E
                ctrl_chars['VT']: self.handle_kill_forward,     # Ctrl+K
                ctrl_chars['KILL']: self.handle_kill_line,      # Ctrl+U
                ctrl_chars['WERASE']: self.handle_erase_word,   # Ctrl+W
                ctrl_chars['ERASE']: self.handle_erase,         # DEL
                ctrl_chars['BS']: self.handle_erase,            # Backspace
                ctrl_chars['LNEXT']: self.handle_literal_next,  # Ctrl+V
                ctrl_chars['EOF']: self.handle_eof,             # Ctrl+D
                ctrl_chars['INTR']: self.handle_interrupt,      # Ctrl+C
                '\x00': self.handle_nop,                        # ignore NUL
            }

The dispatch table maps control characters to handler methods. Each handler manipulates ``self.password`` (a list, not a string, because we need middle-of-line insertions) and ``self.cursor_pos``, then refreshes the display. The prompt is tracked too, since ``refresh_display`` needs to redraw it when clearing the line.

The control character values come from ``_get_terminal_ctrl_chars()``, which reads the terminal's ``termios`` settings before switching to non-canonical mode:

.. code-block:: python

    def _get_terminal_ctrl_chars(fd):
        ctrl = dict(_POSIX_CTRL_CHARS)
        try:
            old = termios.tcgetattr(fd)
            cc = old[6]  # Control characters array
        except (termios.error, OSError):
            return ctrl
        # BS, SOH, ENQ, VT are not in the termios control characters
        # array, so we only override the ones that are configurable.
        for name in ('ERASE', 'KILL', 'WERASE', 'LNEXT', 'EOF', 'INTR'):
            cap = getattr(termios, f'V{name}')
            if cap < len(cc):
                ctrl[name] = cc[cap].decode('latin-1')
        return ctrl

This means if your terminal maps KILL to something other than Ctrl+U, the line editor picks that up automatically. POSIX defaults are used as fallback.

----

The Tricky Parts
****************

**Display refresh with cursor tracking.** When you're showing ``*****`` and the user deletes a character in the middle, you can't just ``\b \b``. You need to redraw the whole line and reposition the cursor. The ``refresh_display`` method handles this by writing ``\r``, clearing the full width (prompt + previous password length), rewriting the prompt and echo characters, then moving the cursor back with ``\b``.

**IEXTEN matters too.** It's not enough to just disable ``ICANON``. The ``IEXTEN`` flag enables implementation-defined input processing like ``LNEXT`` (Ctrl+V). If you leave it on, the terminal driver intercepts Ctrl+V before your code ever sees it. The fix disables both ``ICANON`` and ``IEXTEN`` so the line editor gets full control.

**Ctrl+V (literal next).** This one is subtle. Ctrl+V tells the terminal "treat the next character as a literal, even if it's a control character." So Ctrl+V followed by Ctrl+C should insert a literal ``\x03`` into the password, not raise ``KeyboardInterrupt``. The implementation uses a ``literal_next`` flag that bypasses all dispatch logic for exactly one character.

**Word boundaries for Ctrl+W.** Erasing a word means scanning backwards past spaces, then past non-spaces. Sounds simple until you consider multiple consecutive spaces, words at the start of the line, or an empty buffer. Each edge case needed its own test.

----

The Review
**********

Bénédikt's initial review pushed the patch in a better direction. The first version was a chain of ``if/elif`` blocks, and he flagged it as hard to extend. The refactor to a class with a dispatch table made the code cleaner and easier to add new shortcuts to in the future.

The patch went through several rounds over a few months. The implementation was small, but the test suite grew significantly: 30+ new test cases covering every shortcut, edge case, and combination.

----

What Changed
************

**Before** (Python 3.14 with ``echo_char``):

- Ctrl+U → inserts ``\x15`` into password
- Ctrl+W → inserts ``\x17`` into password
- Ctrl+A → inserts ``\x01`` into password
- Only backspace and Ctrl+C worked

**After** (Python 3.15):

- Full line editing: cursor movement, word deletion, line kill, kill-forward
- Ctrl+V for literal insertion of control characters
- Terminal-aware control character mappings via ``termios``
- Proper display refresh with cursor tracking

----

Takeaways
*********

**Non-canonical mode means you own everything.** The moment you call ``tcsetattr`` with ``~ICANON`` and ``~IEXTEN``, you've told the terminal "I'll handle it." And you'd better actually handle it, or your users will notice immediately.

**Reviewer feedback can reshape a patch for the better.** The dispatcher approach wasn't in my first draft. Bénédikt pushed for it, and the result is code that's much easier to maintain and extend.

**Test the combinations, not just the individual shortcuts.** Ctrl+A followed by Ctrl+K followed by typing new text is a different beast than testing each in isolation. The test suite covers these sequences because that's how people actually use a terminal.

You can find `the full PR here <https://github.com/python/cpython/pull/141597>`_.


`CuriousLearner <https://www.github.com/CuriousLearner>`_
