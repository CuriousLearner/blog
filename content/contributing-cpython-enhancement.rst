Contributing enhancement patch to CPython
=========================================
:date: 2017-06-20 20:34
:author: Sanyam Khurana
:category: FOSS
:slug: contributing-cpython-enhancement
:tags: foss, python, cpython

I started contributing to `CPython <https://github.com/python/cpython>`_ this year from `PyCon Pune sprints </blog/pycon-pune-2017.html>`_. That was one of the best PyCon I've ever attended. Since then, I've spent some time in going through documentation, core dev-guide and now I'm still reading about internals of the Python programming language.

I recently contributed an enhancement patch to Python 3.7 which might be back-ported to Python 3.6. Let's understand the scenario and the enhancement:

New contributor to Python 3 might use old Python 2 syntax treating ``print`` as a statement rather than a function and then see an error like:

.. code-block:: python

    >>> print "hello"
      File "<stdin>", line 1
        print "hello"
                    ^
    SyntaxError: Missing parentheses in call to 'print'

The task was to improve the error message based on different kinds of user input. This shall ensure that we don't only show error to the user but also suggest the correct syntax to be used as a hint. So after the patch being applied, the error message shall say this:


.. code-block:: python

    >>> print "hello"
      File "<stdin>", line 1
        print "hello"
                    ^
    SyntaxError: Missing parentheses in call to 'print'. Did you mean print("hello")?

Sounds easy? Right? No, we aren't done yet. This was a simple print statement dealing with just a string. Potentially someone can try to print anything. What if someone wants to print a tuple?

.. code-block:: python

    >>> print 4,
      File "<stdin>", line 1
        print 4,
              ^
    SyntaxError: Missing parentheses in call to 'print'. Did you mean print(4, end=" ")?

So, the correct syntax is suggested to the user according to Python3.

Along with this, there are cases when someone adds soft-spaces, or just use excessive whitespace like:

.. code-block:: python

    >>> print    "hello"
      File "<stdin>", line 1
        print    "hello"
                       ^
    SyntaxError: Missing parentheses in call to 'print'. Did you mean print("hello")?

This was the first patch where I had to deal with C code. It was more of reading and understanding what the current code does. I had to do a complete re-write of this patch two times in a span of just 1.5 days (Thanks to Nick and Serhiy for the quick reviews).

Here's why:

The first time I wrote the patch, I used raw C APIs, which means I used ``malloc`` and ``free`` for memory allocation and deallocation for manipulating the string input that was received from the user.

While this might work, but there is already a lot of work done by Python core-devs & they've created an entire `C API layer <https://docs.python.org/3/c-api/>`_. So, in the first review, I was pointed to use this API layer, so I had to re-write the patch. One of the learning I had is that virtually any API can fail. So, it is necessary to always check the results before using them.

Most of the methods from the C-API layer that were used in this patch were dealing with `Unicode objects <https://docs.python.org/3/c-api/unicode.html>`_.

Another important learning was to deallocate the previous memory at each check point (if some of the API call fails and there is no memory allocated on heap then deallocate all the previous allocated memory).

Apart from handling the striping of characters that were input on the shell and detecting the tuple syntax, I also wrote test cases for the new feature. In CPython, most of the test cases are written in Python (except a few). Typically in this use case, we only need to check the functionality of the Python layer, so test cases were written in Python.

Let's see how the added feature does what it is intended to do:

.. code-block:: c

    // Static helper for setting legacy print error message
    static int
    _set_legacy_print_statement_msg(PySyntaxErrorObject *self, Py_ssize_t start)
    {
        PyObject *strip_sep_obj = PyUnicode_FromString(" \t\r\n");
        if (strip_sep_obj == NULL)
            return -1;

        // PRINT_OFFSET is to remove `print ` word from the data.
        const int PRINT_OFFSET = 6;
        Py_ssize_t text_len = PyUnicode_GET_LENGTH(self->text);
        PyObject *data = PyUnicode_Substring(self->text, PRINT_OFFSET, text_len);

        if (data == NULL) {
            Py_DECREF(strip_sep_obj);
            return -1;
        }
        PyObject *new_data = _PyUnicode_XStrip(data, 2, strip_sep_obj);
        Py_DECREF(data);
        Py_DECREF(strip_sep_obj);

        if (new_data == NULL) {
            return -1;
        }
        // gets the modified text_len after stripping `print `
        text_len = PyUnicode_GET_LENGTH(new_data);
        const char *maybe_end_arg = "";
        if (text_len > 0 && PyUnicode_READ_CHAR(new_data, text_len-1) == ',') {
            maybe_end_arg = " end=\" \"";
        }
        PyObject *error_msg = PyUnicode_FromFormat(
            "Missing parentheses in call to 'print'. Did you mean print(%U%s)?",
            new_data, maybe_end_arg
        );
        Py_DECREF(new_data);
        if (error_msg == NULL)
            return -1;

        Py_XSETREF(self->msg, error_msg);
        return 1;
    }

This function returns the following:

  -  1 if the error message is successfully set.
  - -1 in case any of the C-API fails.

So, first we use ``strip_sep_obj`` to define all the symbols that we need to strip from the input received from the user. Next, when we get the string, it would be of the form ``print "Hello"``.

.. code-block:: c

    PyObject *strip_sep_obj = PyUnicode_FromString(" \t\r\n");
    if (strip_sep_obj == NULL)
        return -1;

    // PRINT_OFFSET is to remove `print ` word from the data.
    const int PRINT_OFFSET = 6;

What we're interested in is about the text after the print and space. That accounts for the ``PRINT_OFFSET`` that is set to constant 6.

Next, ``_PyUnicode_XStrip`` uses to strip ``strip_sep_obj`` from the ``data`` we assigned earlier. The 2 in this function is a constant value that implies stripping the input from both sides of the ``data``.

.. code:: c

    PyObject *new_data = _PyUnicode_XStrip(data, 2, strip_sep_obj);

Next, we get the length of the text and check if the input meant to print a tuple by checking the last character from the Unicode buffer to be equal to string literal ``,``.

.. code:: c

    const char *maybe_end_arg = "";
    if (text_len > 0 && PyUnicode_READ_CHAR(new_data, text_len-1) == ',') {
        maybe_end_arg = " end=\" \"";
    }

After setting up the ``maybe_end_arg`` we format the new message and use ``Py_XSETREF`` to set the new ``error_msg`` to the ``PySyntaxErrorObject`` instance.

.. code:: c

    Py_XSETREF(self->msg, error_msg);

`Here is the full patch <https://github.com/python/cpython/commit/3a7f03584ab75afbf5507970711c87042e423bb4>`_ if you want to see. The meaning of each of the methods used can be easily found from the official documentation.

I hope to write about my learning in more detail and also explain about different parts of the programming language in a future post.
