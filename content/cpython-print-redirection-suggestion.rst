Fixing the print redirection suggestion in Python 3.7
=====================================================
:date: 2017-08-20 20:34
:author: Sanyam Khurana
:category: FOSS
:slug: cpython-print-redirection-syntax-suggestion
:tags: foss, python, cpython

If you've been following my contributions to CPython, I recently contributed an enhancement patch to `Python 3.7` about `producing correct suggestion for built-in print function in Python 3 if the old print 2 statement style is used <contributing-cpython-enhancement.html>`_.

The patch also got back-ported to `Python 3.6` and is now available to you folks :) Continuing the development on this new suggestion hint, the next target was to produce the correct hint if anyone uses the old Python 2 redirection syntax like:

.. code-block:: python

    >>> import sys
    >>> print >> sys.stderr, "message"

Here we're trying to redirect the "message" string on the ``Standard Error`` stream in Python.

The current error thrown is a ``TypeError`` like:

.. code-block:: python

    TypeError: unsupported operand type(s) for >>: 'builtin_function_or_method' and '_io.TextIOWrapper'.

We also wanted to display the correct syntax in Python 3 like:

.. code-block:: python

    >>> import sys
    >>> print("message", file=sys.stderr)


When I was working on the patch, we realized that till the time the check is made to throw the ``TypeError`` inside the interpreter, we don't have the relevant information about data passed with the print statement available. So, we decided to throw a generic suggestion which would be a constant expression not depending upon the input from the user.  But it would be good enough to suggest some meaningful modification the user could do to fix the error.  We ended up with the following suggestion hint:

.. code-block:: python

    >>> import sys
    >>> print >> sys.stderr, "message"
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: unsupported operand type(s) for >>: 'builtin_function_or_method' and '_io.TextIOWrapper'. Did you mean "print(<message>, file=<output_stream>)"?

Also included some test cases to verify the new feature. `Here is the full patch <https://github.com/python/cpython/commit/5e2eb35bbed3e84079165e576cdb50ef36e13493>`_ if you want to see. The meaning of each of the methods used can be easily found from the official documentation.

I hope to write about my learning in more detail and also explain about different parts of the programming language in one of the future post.
