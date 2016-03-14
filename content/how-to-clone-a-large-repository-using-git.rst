How to clone a large repository using git
#########################################
:date: 2015-12-28 14:14
:author: Sanyam Khurana
:category: Experience
:slug: how-to-clone-a-large-repository-using-git

So, I was trying to clone the official Mozilla gecko repo and it had
around 455182 commits.

As usual I executed on my terminal:

    git clone https://github.com/mozilla/gecko-dev

Then it took whole night to get cloned. I was awake the whole night. At
5:20 AM, it was around 90% received and then boom, it just crashed.

All the data downloaded of more than 1 GB was wasted.

Well, whatever happens, always happens for good. This provided me an
awesome opportunity to learn how to easily clone large repos.

So, there are two ways around this.

**Do a shallow clone!**
~~~~~~~~~~~~~~~~~~~~~~~

**Wait, what? What is a shallow clone?**

Well, I mean clone the repo but not with all commits. Let's do it for
just latest commit ie only one commit. Later once all the objects are
extracted, we can deepen the clone.

**So, how do you do that in git?**

With the depth parameter as:

    git clone --depth=1 https://github.com/mozilla/gecko-dev

Here I've given depth of 1 commit, and suddenly the 1.5 GB repo became
just around 258 MB to be downloaded.

If you still are stuck, and even this is difficult to clone because of
unstable connection then prefer downloading a bundle, or explore `more
option via this SO
Question <http://stackoverflow.com/questions/3954852/how-to-complete-a-git-clone-for-a-big-project-on-an-unstable-connection>`__

**Once you have shallow clone, you can deepen it.**

    git fetch --depth=100

to fetch 100 commits

or if you want to get all commits then simply use:

    git fetch --unshallow

and that would fetch all the commits and make your repo similar to what
you do in the initial place like using git clone simply.

I hope this would help someone :)
