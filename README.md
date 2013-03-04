What is This?
-------------

This repo contains my own (or copied from someone else's and modified) custom RPM packages I use in
different infrastructures I need to operate.


Why Did You Create This?
------------------------

After working for many companies over the last decade and spending the first month of my work basically
building 3rd-party software full time I've decided to do it once, store the recipes on Github and use
them whenever and wherever I needed. As a bonus I'll keep improving the recipes and fixing bugs in them
over time instead of creating them from scratch every time.

**Disclaimer:** This is not an opensource project, no bug reports will be accepted for the stuff in this repo,
I do not guarantee license purity of this stuff and do not give any guarantees. If you want to ise it -
feel free to. If you have a patch - feel free to send a pull request.


Why Those Weird "ok-" Prefixes?
-------------------------------

Don't want any collisions with existing packages and, as you may have guessed, I want to eternalize my initials
in all those package names. :smile:


Why Do You Install Software to /opt Directory?
----------------------------------------------

Because I do not really care for LFS conventions and do whatever I think is easier to operate plus I
really don't like pulling software into a dozen different pieces scattered over the system just to make
it LFS-compliant (look at any graphite specs out there and you'll understand what I mean).


How to Use This?
----------------

Each directory here represents an RPM package, go to any package directory and run `rake`.
The results will be located in `RPMS`/`SRPMS` directories. You can run `rake -T` to get more
information about available tasks.
