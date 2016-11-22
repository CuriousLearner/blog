Contributing more to Marionette and Firefox UI Tests
####################################################
:date: 2016-10-06 00:53
:author: Sanyam Khurana
:category: FOSS
:slug: contributing-marionette-firefox-ui-tests
:tags: mozilla, marionette, python

If you don't know about Marionette; you can read my `previous blog post here </getting-started-marionette.html>`_.

I've been recently given some follow-up bugs by my mentor. I've just finished up fixing this bug:
`Add support for callbacks to restart() and quit() methods of Marionette <https://bugzilla.mozilla.org/show_bug.cgi?id=1298800>`_. Now I've picked up a follow up bug to `Add a test to quit firefox <https://bugzilla.mozilla.org/show_bug.cgi?id=1298803>`_.

While trying to fix this bug, I reported two bugs in the Marionette component (`Bug 1309556 <https://bugzilla.mozilla.org/show_bug.cgi?id=1309556>`_, `Bug 1309141 <https://bugzilla.mozilla.org/show_bug.cgi?id=1309141>`_) which blocks my current bug. So, I'll be first fixing up my reported bugs and then come back to this follow up bug which is assigned to me.

Till now, the journey in contributing to Marionette has been really awesome and I learned quite a lot of things. I got a chance to read a lot of code and I'm really impressed by the writing styles of the developers. The code base is very neat and definitely good for people who want to see some real test cases in action (something which was not being explained in those *Testing 101 talks*) and also improve upon their Python skills.

I would like to thank Henrik [:whimboo] who is my mentor and guided me so patiently & helped in resolving all my doubts. I'm also reading more about `mach` command line tool and `marionette` in general.

I recently also came accross ``Firefox Puppeteer`` which is a library built upon the existing ``Marionette Python Client``. More appropriately; you can write ``Firefox UI tests`` for the ``chrome components`` using ``Puppetteer``.


I'm still to read more about this and I hope at that point of time I'll be able to join all the *learning dots* and explain it all in my next blog post.
