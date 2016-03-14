Bootstrap Modal Scroll Bug on Chrome [Easy-Fix]
###############################################
:date: 2016-01-13 00:55
:author: Sanyam Khurana
:category: Experience
:slug: bootstrap-modal-scroll-bug-on-chrome-easy-fix

As usual, I was contributing more to the PyDelhi Conference project and
saw that the code of conduct was really occupying a large space and
wasn't looking good. I contacted theskumar on IRC and we decided to make
some changes in the FAQ as well as Code of Conduct section.

Quick enough I decided to have modals to be used for displaying the
short and long version of code of conduct. I did it as well as the other
task of modifying the FAQ section.

I told theskumar about it. Since it was around 2 AM, everyone was
sleeping. Next day, I got a reply from theskumar that the modal was not
scrolling on the mobile.

I tried quickly on my mobile and it worked. I asked him about the
browser he was using, and he told me that it was Chrome. I tried that on
firefox and it was working.

I then tried it on my desktop on both firefox and chrome. In firefox,
both on mobile and desktop it was working fine, but in chrome, both on
mobile and desktop, it was not scrolling.

I started searching, and got to the official bootstrap repo on github,
where I found various issues, and this was a known bug on chrome.

I got to StackOverflow in search of alternatives, and then kept on
applying it. But no success. Either the content of the body moves, or
the whole page hanged.

I reached out Apoorva mam, and then she helped me. The solution was to
have a scroll bar implemented in the modal keeping it's height fixed.

So, we just added this to CSS:

| .modal-body {
|  position: relative;
|  padding: 20px;
|  height: 200px;
|  overflow-y: scroll;
|  }

and it's working!

I hope this would help someone who is still figuring out about scrolling
bug on chrome.
