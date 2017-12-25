Improving class instantiation error message logic in Python 3.7
===============================================================
:date: 2017-12-11 20:34
:author: Sanyam Khurana
:category: FOSS
:slug: cpython-improve-error-message-logic-for-class-instantiation
:tags: foss, python, cpython

Many folks ask me why I contribute to CPython. I think it is a special feeling which cannot be expressed in words. Even if you just fix a typo in the doc, believe me, you've actually helped a lot of developers and companies all over the world. Your (small) changes matters a lot. They make huge impact in FOSS world :)

While browsing through bugs on `bugs.python.org <https://bugs.python.org>`_ , I found a bug reported by a teacher who requested to enhance the error message logic as he described in one of the blog posts on his blog on `Favorite Terrible Python Error Message <https://blog.lerner.co.il/favorite-terrible-python-error-message/>`_. The ``object_new`` and ``object_init`` currently have "object" hardcoded in the error messages they raise for excess parameters. It is thus difficult for anyone facing that error to know what is going on.

Nick explained really well about the `comment in the bug <https://bugs.python.org/issue31506#msg302439>`_ which I'm stating here:

.. code-block:: python

    >>> class C: pass
    ...
    >>> C(10)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: object() takes no parameters
    >>> c = C()
    >>> c.__init__(10)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: object.__init__() takes no parameters


    This hardcoding makes sense for the case where that particular method has been overridden, and the interpreter is reporting an error in the subclass's call up to the base class, rather than in the call to create an instance of the subclass:

.. code-block:: python

    >>> class D:
    ...     def __init__(self, *args):
    ...         return super().__init__(*args)
    ...
    >>> D(10)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 3, in __init__
    TypeError: object.__init__() takes no parameters


    However, it's misleading in the case where object_new is reporting an error because it knows object_init hasn't been overridden (or vice-versa), and hence won't correctly accept any additional arguments: in those cases, it would be far more useful to report "type->tp_name" in the error message, rather than hardcoding "object".

I thus started working on the patch to detect the cases when ``excess_args`` are supplied and show the correct error message.

    Now the error messages in `object.__new__` and `object.__init__` aim
    to point the user more directly at the name of the class being instantiated
    in cases where they *haven't* been overridden (on the assumption that
    the actual problem is a missing `__new__` or `__init__` definition in the
    class body).

    When they *have* been overridden, the errors still report themselves as
    coming from the object, on the assumption that the problem is with the call
    up to the base class in the method implementation, rather than with the
    way the constructor is being called.

If you're interested, you can see the whole `patch here <https://github.com/python/cpython/commit/780acc89bccf9999332d334a27887684cc942eb6>`_.
I hope this patch would help all those kids and all the new and old folks playing with Python to learn about how objects are created and instantiated. It always feels great to make (small) changes. Helping in improving Python one patch at a time :)
