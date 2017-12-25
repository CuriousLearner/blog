The cycle of creating bugs and patching them
============================================
:date: 2017-12-15 20:34
:author: Sanyam Khurana
:category: FOSS
:slug: cpython-contribution-print-enhancement
:tags: foss, python, cpython

I write patches, which creates more bugs; then I go and patch them again. The cycle continues...

If you've been following up my recent contributions on the CPython code-base, sometime back I added an enhancement patch to the code-base which presents the user a suggestion on the correct syntax hint for calling built-in ``print`` function in Python 3.6 & 3.7 if it is used as an old style ``print`` statement.

Recently a `bug was filed <https://bugs.python.org/issue32028>`_ for that new feature. I am more than excited to hear this news (because people have already started using the feature I added to Python programming language :))

    When the following code is executed by Python 3.6.3 inside of a ``.py`` file:

.. code-block:: python

    def f():
        print '%d' % 2


    , then Python gives the following error message:

.. code-block:: python

    SyntaxError: Missing parentheses in call to 'print'. Did you mean print(int '%d' % 2)?


So, the issue with the earlier patch was this as Nick suggested:

    Given the symptoms (stripping 4 spaces + "pr" from the start of the line, leaving "int " behind), it looks like we're not stripping the leading whitespace when determining the text to include in the suggested print() call.

When I got some time to work on this, it took me just 5 mins to re-patch it for the first version of the patch. (That is the fastest I've done in any bug in CPython, probably because the earlier patch was written by me.)

So, after review, we also did a bit of refactoring to that patch. It was already approved a few weeks ago but still waiting to be merged. Here is the `updated patch <https://github.com/python/cpython/pull/4688/files>`_ if you want to see.
