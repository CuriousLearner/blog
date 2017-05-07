Mercurial commands list for contributing to Mozilla
====================================================
:date: 2017-05-07 21:15
:author: Sanyam Khurana
:category: Experience
:slug: mozilla-mercurial-commands
:tags: mozilla, remo, mozilla-rep


Most of the Mozilla's project uses Mercurial as a version control tool. I've worked in different projects of Mozilla and I found that most people still prefer git over mercurial and use `git-cinnabar <https://github.com/glandium/git-cinnabar>`__ as a bridge to do all version control stuff in git and then prepare mercurial ready patches.

Although this approach is quite good and people like me who are more familiar with git should do it this way. But, I wanted to get acquainted with Mercurial as a version control tool and tried to do it the hard way (Most of the time my mentors were not able to help me since they used git and I used Mercurial). Mercurial works on basis of changesets. In this blog post, I'm keeping notes of various common commands that would help me and anyone navigate their way using mercurial.

These notes assume that you've basic familarity with various terminologies used in DVCS such as git. I've also mentioned analogies to how both version control systems work. (Something that took me time to figure out).

Mercurial Commands
------------------

Mercurial works on basis of changesets. Here are the common commands that you can use throughout Mozilla's projects:

``Pull changes from remote repository to local``

No! This is not same as ``git pull``! Read out the next command to understand the analogy.

.. code:: bash

    hg pull

``Always update to the tip of repo``

.. code:: bash

    hg update


**Note** : This is different from ``git pull``. ``git pull`` essentially does ``git fetch`` i.e. fetch remote changes to local and then do ``git merge`` which updates the local copy of your code.

So, ``git pull`` = ``git fetch`` + ``git merge``

But in case of mercurial, ``hg pull`` just fetches remote changes to local. It does not however update your working copy. If you want to update your local copy, then you should do ``hg update``.


``Update to specific revision of the repo``

Here we update to revision 0 with `-r` option. `r` stands for `revision`.

.. code:: bash

    hg update -r 0

``See file a.txt at revision 0``

.. code:: bash

    hg cat -r 0 a.txt


``See difference from revision 0 to 1 in file a.txt``

.. code:: bash

    hg diff -r 0:1 a.txt

``hg outgoing: What all changes are waiting to be pushed next``

.. code:: bash

    hg outgoing

``hg incoming: Changes that are waiting to be brought in to your local from remote repository``

You can see if there are changes on the remote and see their diff with respect to your working copy.

.. code:: bash

    hg incoming


``Difference between rollback and revert``

.. code:: bash

    If not committed then:
        hg revert
    else:
        hg rollback

``hg backout: To backout a changeset that has been added to tree. Analogous to git revert.``

In essence, what it does is, it looks at the changeset, figures out the opposite, and does that to your current working directory.

.. code:: bash

    hg backout -r 2 --merge

``Limit the logs you see``

By default hg log streams from tip till end. While working on large projects such as that of Mozilla with more than million commits, it is messy to let it just stream while you just wanted to see latest commits.

With -l option you define how many changesets you want to see. That's for displaying first 3 commits.

.. code:: bash

    hg log -l 3


I hope this shall help people who have familarity with git and are playing around with mercurial.

I'll be updating this post with more commands soon. If you think there is some important command that is not here, please mention that in comments and I'll add it here.
