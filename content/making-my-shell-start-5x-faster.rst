How I made my shell start 5x faster (2s to 350ms)
#################################################
:date: 2026-07-14 09:30:00
:tags: zsh, shell, performance, dotfiles, profiling, mise, nvm
:summary: My interactive shell took two seconds to start. I profiled it instead of guessing, found three culprits, and got it to 350ms. Here is the method and the numbers.
:status: published
:lang: en
:author: Sanyam Khurana
:category: Technical
:slug: making-my-shell-start-5x-faster

Every new terminal tab paused for about two seconds before it gave me a
prompt. On its own that is nothing. Multiplied across every tab, every
day, for years, it is a papercut I had simply stopped noticing.

I decided to fix it properly. Not by copying someone's "fast zsh" gist,
but by measuring what my own shell was actually spending time on and
cutting the biggest offenders. This post is the method and the results.

Rule zero: measure, do not guess
================================

The single most common mistake with shell startup is optimising the
thing you assume is slow. So the first step is a stopwatch, not an edit.

For wall-clock time, I timed a full login plus interactive shell, which
is what iTerm actually spawns::

    for i in 1 2 3; do /usr/bin/time zsh -l -i -c exit; done

That flag combination is the whole point, because it decides how much of
the startup actually runs:

- ``-l`` runs zsh as a *login* shell, so it sources the login files
  (``.zprofile``, ``.zlogin``) on top of the interactive ones.
- ``-i`` runs it as *interactive*, which is what pulls in ``.zshrc``,
  the prompt, history, completion, and plugins. Drop it and zsh skips
  ``.zshrc`` entirely and you measure almost nothing.
- ``-c exit`` hands it a command to run and quit, instead of sitting at
  a prompt waiting for input.

Together they reproduce exactly what a new terminal tab does, then exit
immediately, so the wall-clock number is almost entirely startup cost
and nothing else.

The numbers were embarrassing::

    2.52 real
    1.99 real
    1.99 real

Roughly two seconds. A snappy zsh starts in under 200ms, so I was an
order of magnitude off.

Wall-clock time tells you *that* it is slow. It does not tell you
*where*. For that, zsh ships a profiler, ``zsh/zprof``::

    zsh -i -c 'zmodload zsh/zprof; source ~/.zshrc; zprof'

``zprof`` prints every function your startup called, ranked by time.
Mine was blunt about it:

- ``nvm_auto``: 1180ms, a full **58% of startup**
- ``compdump``: 275ms, **14%**, and it was running twice

Two findings accounted for nearly three-quarters of the cost. That is
the whole game. Everything else was noise.

Culprit 1: nvm, the usual suspect
=================================

``nvm`` is notorious for exactly this. Sourcing ``nvm.sh`` triggers
``nvm_auto``, which resolves and activates a Node version on every
single shell. Over a second, gone, before I have typed anything.

The lazy fix is to defer nvm until first use. The better fix, in my
case, was to notice I did not need nvm at all. I had already moved to
``mise`` for runtime management, and mise already had the exact Node
version nvm was pointing at. nvm was a second tool doing a job something
else already did.

So nvm came out entirely. The root-cause fix was a deletion, not a
workaround::

    # node is managed by mise (activated below); nvm removed to keep startup fast.

That one removal bought back the full 1180ms.

Culprit 2: conda activating on every shell
==========================================

conda was doing something subtler. Its init block runs a Python
subprocess on every startup to evaluate its shell hook, then
auto-activates the ``base`` environment. I was paying for a Python
interpreter launch just to open a terminal, and my ``python3`` was
coming from Homebrew anyway.

I did not want to lose the ``conda`` command, just its startup tax. The
answer is a lazy shim: define ``conda`` as a shell function that, on
first call, replaces itself with the real thing::

    conda() {
      unset -f conda
      eval "$('/opt/homebrew/Caskroom/miniconda/base/bin/conda' 'shell.zsh' 'hook')"
      conda "$@"
    }

Now conda costs nothing until the day I actually type ``conda``, which
is rare. No base environment auto-activation, no Python subprocess at
launch.

Culprit 3: compinit running three times
=======================================

``compinit`` is what powers tab completion. It scans your completion
directories and writes a cache. You need it exactly once per shell.
Mine ran three times: once inside oh-my-zsh, once via ``bashcompinit``
for a Terraform completion, and once more from a block Docker's
installer had appended to my ``.zshrc``.

Three scans, three cache rebuilds, 275ms. The fix was to keep
oh-my-zsh's single ``compinit`` and delete the redundant one. The only
subtlety: Docker's completions had to be added to ``fpath`` *before*
oh-my-zsh runs its compinit, so I moved that one line up rather than
leaving a second init behind it.

While I was in there, I found ``zsh-syntax-highlighting`` had been
cloned but never activated, because I had no ``plugins=()`` array at
all. So I got live syntax highlighting essentially for free, plus
``zsh-autosuggestions``, the fish-style ghost-text completion I had been
missing.

The results
===========

Same three-run measurement, after the changes::

    0.38 real
    0.36 real
    0.36 real

From roughly 2.0s to 0.36s. About 5.5x faster.

Where it went:

- nvm removed (mise already owned Node): ~1180ms
- conda lazy-loaded instead of eager base activation: one Python
  subprocess per shell
- compinit deduplicated from three runs to one: ~130ms

No feature lost. Node still works, conda still works, completions still
work, and now there is syntax highlighting and autosuggestions that were
not there before.

What I would tell my past self
==============================

The technique matters more than my specific fixes, because your slow
shell is almost certainly slow for different reasons than mine.

1. **Time it before you touch it.** ``/usr/bin/time zsh -l -i -c exit``.
   You cannot claim a win you did not measure.
2. **Profile, do not theorise.** ``zprof`` will name the guilty function
   in one command. Attack the biggest bar first and ignore the rest.
3. **Prefer deletion to cleverness.** My largest win was removing a tool
   I had stopped needing, not tuning it. The second largest was deleting
   two redundant init calls. Lazy-loading came third.
4. **Verify the win, and verify nothing broke.** Re-run the timer, then
   confirm the commands you removed still resolve.

The whole thing took an evening and turned a two-second papercut into
something I no longer notice, which is exactly where a shell should be.

While I had the dotfiles open I kept pulling the thread, and ended up
deleting around 1500 lines of accumulated cruft: vendored copies of
tools that are a ``brew install`` away, scripts whose upstream APIs had
died years ago, a custom zsh theme that Powerlevel10k had quietly
superseded, and a Fedora provisioning script I had not run in close to a
decade. Startup speed was the reason I opened the drawer. A much
cleaner drawer was the bonus.

Oh, and yes, I looked at fish. It has genuinely nicer defaults. But
everything I would switch for was two ``brew install`` lines away in
zsh, without rewriting a decade of POSIX shell functions. I stayed.

Everything is in the open
=========================

My dotfiles are public, so here are the actual diffs if you want to read
past the prose:

- `The core startup fix <https://github.com/CuriousLearner/dotfiles/commit/1d8146dc545157d33b9798d4ad26f943a7637bd8>`_: nvm removal, lazy conda, and the compinit deduplication.
- `Switching the installer from nvm to mise <https://github.com/CuriousLearner/dotfiles/commit/87539620e9e6e73f8925355558a672f9f6a8e56c>`_.
- `Adding autosuggestions and activating syntax highlighting <https://github.com/CuriousLearner/dotfiles/commit/2a3d0a255d4c614e20bc0f2e9dd378ca5ebad27e>`_.
- `Binding Option-Right for one-word accept <https://github.com/CuriousLearner/dotfiles/commit/8989ae5a4e80c16c258c793d46498506bc6314e9>`_.

The whole repo lives at `github.com/CuriousLearner/dotfiles <https://github.com/CuriousLearner/dotfiles>`_.
