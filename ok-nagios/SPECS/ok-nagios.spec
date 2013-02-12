%define nagios_version 3.4.4
%define package_revision 02

Name: ok-nagios
Version: %{nagios_version}
Release: %{package_revision}%{?dist}
Summary: Host/service/network monitoring program

Group: Applications/System
License: GPLv2
URL: http://www.nagios.org/
Source0: nagios-%{version}.tar.gz
Source1: nagios.logrotate
# PNG files from the old nagios-0010-Added-several-images-to-the-sample-config.patch
Source10: printer.png
Source11: router.png
Source12: switch.png

Patch1: nagios-0001-from-rpm.patch
Patch2: nagios-0002-SELinux-relabeling.patch
# Sent upstream
Patch3: nagios-0003-Fix-etc-init.d-nagios-status.patch
# Sent upstream
Patch4: nagios-0004-Fix-installation-of-httpd-conf.d-config-file.patch
Patch5: nagios-0005-Install-config-files-too.patch
Patch6: nagios-0006-Do-not-start-service-by-default.patch
# Sent upstream
Patch7: nagios-0007-The-init-script-should-return-2-in-case-of-unknown-c.patch
Patch8: nagios-0008-Fix-path-to-CGI-executables.patch
Patch9: nagios-0009-Fixed-path-to-passwd-file-in-Apache-s-config-file.patch
Patch10: nagios-0010-Added-several-images-to-the-sample-config-revb.patch
Patch11: nagios-0011-Fixed-strange-permissions.patch

BuildRequires: gd-devel > 1.8, mailx, libjpeg-devel, libpng-devel

Requires: httpd
Requires: php
Requires: mailx
Requires(preun): initscripts, chkconfig
Requires(post): initscripts, chkconfig
Requires(postun): initscripts

Requires: ok-nagios-common
Requires: user(nagios)
Requires(pre): user(nagios)
Requires: group(nagios)
Requires(pre): group(nagios)

Provides: nagios
Obsoletes: nagios

Summary: Nagios monitors hosts and services and yells if somethings breaks

%description
Nagios is a program that will monitor hosts and services on your
network.  It has the ability to send email or page alerts when a
problem arises and when a problem is resolved.  Nagios is written
in C and is designed to run under Linux (and some other *NIX
variants) as a background process, intermittently running checks
on various services that you specify.

The actual service checks are performed by separate "plugin" programs
which return the status of the checks to Nagios. The plugins are
available at http://sourceforge.net/projects/nagiosplug.

This package provides the core program, web interface, and documentation
files for Nagios. Development files are built as a separate package.

%package common
Group: Applications/System
Summary: Provides common directories, uid and gid among nagios-related packages
Requires(pre): shadow-utils
Requires(post): shadow-utils
Provides: user(nagios)
Provides: group(nagios)

Provides: nagios-common
Obsoletes: nagios-common

%description common
Provides common directories, uid and gid among nagios-related packages.


%package devel
Group: Applications/System
Summary: Provides include files that Nagios-related applications may compile against
Requires: ok-nagios = %{version}-%{release}
Provides: nagios-devel
Obsoletes: nagios-devel


%description devel
Nagios is a program that will monitor hosts and services on your
network. It has the ability to email or page you when a problem arises
and when a problem is resolved. Nagios is written in C and is
designed to run under Linux (and some other *NIX variants) as a
background process, intermittently running checks on various services
that you specify.

This package provides include files that Nagios-related applications
may compile against.


%prep
%setup -q -n nagios
%patch1 -p1 -b .fedora
%patch2 -p1 -b .selinux_relabel
%patch3 -p1 -b .fix_status_retcode
%patch4 -p1 -b .fix_httpd_conf_d
%patch5 -p1 -b .install_config
%patch6 -p1 -b .dont_start_by_default
%patch7 -p1 -b .return_2
%patch8 -p1 -b .fix_path_to_cgi
%patch9 -p1 -b .fix_path_to_passwd
%patch10 -p1 -b .more_images
%patch11 -p1 -b .fix_perms

install -p -m 0644 %{SOURCE10} %{SOURCE11} %{SOURCE12} html/images/logos/


%build
%configure \
    --prefix=%{_datadir}/nagios \
    --exec-prefix=%{_localstatedir}/lib/nagios \
    --with-init-dir=%{_initrddir} \
    --with-cgiurl=/cgi-bin/ \
    --with-htmlurl=/ \
    --with-lockfile=%{_localstatedir}/run/nagios.pid \
    --libdir=%{_libdir}/nagios \
    --with-nagios-user=nagios \
    --with-nagios-grp=nagios \
    --bindir=%{_sbindir} \
    --libexecdir=%{_libdir}/nagios/plugins \
    --sysconfdir=%{_sysconfdir}/nagios-server \
    --localstatedir=%{_localstatedir}/log/nagios \
    --datadir=%{_datadir}/nagios/html \
    --with-gd-lib=%{_libdir} \
    --with-gd-inc=%{_includedir} \
    --disable-embedded-perl \
    --with-perlcache \
    --with-template-objects \
    --with-template-extinfo \
    STRIP=/bin/true
make %{?_smp_mflags} all

sed -i -e "s| package Embed::Persistent;|#\!%{_bindir}/perl\npackage Embed::Persistent;|" p1.pl
sed -i -e "s|NagiosCmd=/var/log/nagios/rw/nagios.cmd|NagiosCmd=/var/lib/nagios/rw/nagios.cmd|" daemon-init
sed -i -e "s|command_file=/var/log/nagios/rw/nagios.cmd|command_file=/var/lib/nagios/rw/nagios.cmd|" sample-config/nagios.cfg
echo >> html/stylesheets/common.css


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} INIT_OPTS="" INSTALL_OPTS="" COMMAND_OPTS="" \
     CGIDIR="%{_libdir}/nagios/cgi-bin" CFGDIR="%{_sysconfdir}/nagios-server" \
     install install-init install-commandmode install-config install-exfoliation

# Create configs directory
install -d -m 0755 %{buildroot}%{_sysconfdir}/nagios-server

# Install header-file
install -D -m 0644 include/locations.h %{buildroot}%{_includedir}/nagios/locations.h

# Install logrotate rule
install -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/nagios

# Make room for event-handlers
install -d -m 0755 %{buildroot}%{_libdir}/nagios/plugins/eventhandlers

install -d -m 0775 %{buildroot}%{_localstatedir}/lib/nagios/rw
install -d -m 0775 %{buildroot}%{_localstatedir}/lib/nagios


%clean
rm -rf %{buildroot}


%pre common
getent group nagios >/dev/null || groupadd -r nagios
getent passwd nagios >/dev/null || useradd -r -g nagios -d %{_localstatedir}/spool/nagios -s /sbin/nologin nagios
exit 0


%preun
if [ $1 = 0 ]; then
    /sbin/service nagios stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del nagios || :
fi


%post
%{_sbindir}/usermod -a -G nagios apache || :
/sbin/chkconfig --add nagios || :



%files
%dir %{_libdir}/nagios/plugins/eventhandlers
%dir %{_libdir}/nagios/cgi-bin
%dir %{_datadir}/nagios
%dir %{_datadir}/nagios/html
%doc %{_datadir}/nagios/html/docs
%doc Changelog INSTALLING LICENSE README UPGRADING
%{_datadir}/nagios/html/[^d]*
%{_sbindir}/*
%{_libdir}/nagios/cgi-bin/*cgi
%{_initrddir}/nagios
%config(noreplace) %{_sysconfdir}/logrotate.d/nagios
%config(noreplace) %{_sysconfdir}/nagios-server/*cfg
%config(noreplace) %{_sysconfdir}/nagios-server/objects/*cfg
%attr(0750,root,nagios) %dir %{_sysconfdir}/nagios-server/objects
%attr(2775,nagios,nagios) %dir %{_localstatedir}/lib/nagios/rw
%attr(0750,nagios,nagios) %dir %{_localstatedir}/log/nagios
%attr(0750,nagios,nagios) %dir %{_localstatedir}/log/nagios/archives
%attr(0750,nagios,nagios) %dir %{_localstatedir}/log/nagios/spool/
%attr(0750,nagios,nagios) %dir %{_localstatedir}/log/nagios/spool/checkresults


%files common
%dir %{_sysconfdir}/nagios-server
%dir %{_libdir}/nagios
%dir %{_libdir}/nagios/plugins
%attr(0755,nagios,nagios) %dir %{_localstatedir}/lib/nagios


%files devel
%{_includedir}/nagios


%changelog
* Sun Jan 13 2013 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.4.4-1
- Update to 3.4.4; CVE-2012-6096 (#893269)
- Refactored the patch nagios-0010-Added-several-images-to-the-sample-config.patch
  as patch can't create binary files (#875362).
  The old patch10 was replaced by nagios-0010-Added-several-images-to-the-sample-config-revb.patch
  and the PNG files included as sources 10, 11, and 12.

* Tue Dec  4 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.4.3-1
- Upgrade to 3.4.3

* Sat Nov 10 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.4.2-1
- Upgrade to 3.4.2

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 3.4.1-2
- Perl 5.16 rebuild

* Mon Jun 25 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.4.1-1
- Upgrade to 3.4.1 (#835047)
- Dropped nagios-0012-Fixed-html-rss-install-files.patch

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 3.3.1-4
- Perl 5.16 rebuild

* Fri Feb 10 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.3.1-3
- Move the nagios-common's usermod line to the main nagios package (#627527).

* Fri Feb 10 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.3.1-2
- Add php to the requirements list (#519371, et al.).

* Tue Feb  7 2012 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.3.1-1
- Upgrade to 3.3.1 (#732329);
  includes fixes for CVE-2011-1523 and CVE-2011-2179 (#690880, #690881, #709874).
- Make nagios-common own the /usr/lib{,64}/nagios/plugins directories (#756839).
- Change the ownership of /etc/nagios to the nagios-common package (#756839).
- Retab (tabs -> spaces).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 3.2.3-12
- Rebuild for new libpng

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.2.3-11
- Perl mass rebuild

* Wed Mar 23 2011 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.2.3-10
- Rebuild against new mysql.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Peter Lemenkov <lemenkov@gmail.com> - 3.2.3-8
- Fixed strange permission on executables (see rhbz #672074)
- Dropped permissions on directories with log-files (see rhbz #672074)

* Tue Nov 23 2010 Peter Lemenkov <lemenkov@gmail.com> - 3.2.3-7
- Finally fixed path to CGI (rhbz #653291)
- Added runtime dependency - mailx (see rhbz #655541)
- Added more images to the sample config

* Thu Nov 18 2010 Peter Lemenkov <lemenkov@gmail.com> - 3.2.3-6
- Fixed path to passwd file in Apache's config file

* Tue Nov 16 2010 Peter Lemenkov <lemenkov@gmail.com> - 3.2.3-5
- Fix building on EL-5

* Mon Nov 15 2010 Peter Lemenkov <lemenkov@gmail.com> - 3.2.3-4
- Fix path to CGI (rhbz #653291)

* Wed Nov  3 2010 Peter Lemenkov <lemenkov@gmail.com> - 3.2.3-3
- Disable stripping of binaries (see rhbz #648223).

* Wed Oct 27 2010 Peter Lemenkov <lemenkov@gmail.com> - 3.2.3-2
- Accidentally forgotten patches added back

* Tue Oct 26 2010 Peter Lemenkov <lemenkov@gmail.com> - 3.2.3-1
- Ver. 3.2.3
- Further cleanups in spec-file

* Wed Sep 29 2010 jkeating - 3.2.2-2
- Rebuilt for gcc bug 634757

* Sat Sep 11 2010 Peter Lemenkov <lemenkov@gmail.com> - 3.2.2-1
- Ver. 3.2.2 (rhbz #629439).
- Cleanup spec-file
- Ensure that %%{_sysconfdir}/httpd/conf.d/nagios.conf points to
  the actual passwd file (see rhbz #576571).

* Tue Aug 24 2010 Adam Tkac <atkac redhat com> - 3.2.1-6
- rebuild

* Wed Jun  9 2010 Peter Lemenkov <lemenkov@gmail.com> - 3.2.1-5
- Removed obsoletes: nagios < 3.2.1-2

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.2.1-4
- Mass rebuild with perl-5.12.0

* Mon May 17 2010 Peter Lemenkov <lemenkov@gmail.com> - 3.2.1-3
- Fixed severe issue with uninstalling main nagios package while
  updating (see rhbz #590709 for details).

* Sun Apr 25 2010 Peter Lemenkov <lemenkov@gmail.com> - 3.2.1-2
- Created 'common' subpackage for gid/uid and common directory

* Sat Mar 13 2010 Peter Lemenkov <lemenkov@gmail.com> - 3.2.1-1
- Upgrade to 3.2.1 (#572587).
- Fixed SELinux patch (#573119).

* Thu Feb 25 2010 Peter Lemenkov <lemenkov@gmail.com> - 3.2.0-4
- The package builds now with distro CFLAGS, CXXFLAGS (see bz #520979)
- Fixed returning status for init-script (see bz #546561)
- Fixed selinux issue with writing of PID-file (see bz #548638 and bz #539963)
- Fixed build on EPEL (see bz #526817)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.2.0-3
- rebuild against perl 5.10.1

* Mon Aug 17 2009 Mike McGrath <mmcgrath@redhat.com> - 3.2.0-2
- s/datarootdir/datadir/

* Sun Aug 16 2009 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.2.0-1
- Upgrade to 3.2.0 (#517210).

* Fri Jul 24 2009 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.1.2-3
- Corrected the package version in the last two changelog entries (#499853)
- Using configure --datarootdir option instead of --datadir (#499853)
  (fixes the physical_html_path value in cgi.cfg)
- Fixes permissions to the new php configuration file config.inc.php (#499853)
- Re-enables the httpd requirement as its removal caused several problems
  (see #487411 for more information)

* Wed Jul 15 2009 Mike McGrath <mmcgrath@redhat.com> 3.1.2-2
- Release bump for rebuild

* Mon Jun 29 2009  Robert M. Albrecht <fedora@romal.de> 3.1.1-1
- Upstream released a new version

* Mon Jun 22 2009 Mike McGrath <mmcgrath@redhat.com> - 3.0.6-4
- Removing httpd requires for #487411

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 11 2009  Robert M. Albrecht <fedora@romal.de> 3.0.6-2
- I messed my CVS up

* Tue Dec 02 2008  Robert M. Albrecht <fedora@romal.de> 3.0.6-1
- Upstream released a new version

* Mon Nov 24 2008 Mike McGrath <mmcgrath@redhat.com> 3.0.5-1
- Upstream released a new version

* Mon Oct 20 2008 Robert M. Albrecht <romal@gmx.de> 3.0.4-3
- Fixed a typo introduced in fixing Bugzilla 461087

* Mon Oct 20 2008 Robert M. Albrecht <romal@gmx.de> 3.0.4-2
- Bugzilla 461087 wrong path for icons

* Mon Oct 20 2008 Robert M. Albrecht <romal@gmx.de> 3.0.4-1
- Upstream released 3.0.4
- Fixed two typos in nagios.spec

* Sun Sep 28 2008 Mike McGrath <mmcgrath@redhat.com> 3.0.3-9
- License fix

* Mon Jul 23 2008 Robert M. Albrecht <romal@gmx.de> 3.0.3-8
- Matthew Jurgens provided a script and Readme for upgrading your config to Release 3

* Mon Jul 22 2008 Robert M. Albrecht <romal@gmx.de> 3.0.3-7
- Added summary
- Added german translations

* Tue Jul 10 2008 Robert M. Albrecht <romal@gmx.de> 3.0.3-6
- disabled conf.d in nagios.conf for now

* Tue Jul 10 2008 Robert M. Albrecht <romal@gmx.de> 3.0.3-5
- Killed BuildRequirements for unsupported Fedora releases

* Wed Jul 02 2008 Robert M. Albrecht <romal@gmx.de> 3.0.3-4
- renamed preconfigured passwd to .htpasswd to enable Apaches .ht* protection
- added default .htpasswd with user nagiosadmin password nagiosadmin

* Tue Jul 01 2008 Robert M. Albrecht <romal@gmx.de> 3.0.3-3
- Added Apache style conf.d
- Added a working example config named internet.cfg
- The object folder was created twice

* Tue Jul 01 2008 Robert M. Albrecht <romal@gmx.de> 3.0.3-2
- Fixed folder /var/log/nagios/spool/checkresults
- silenced rpmlint (tabs, spaces)
- silenced rpmlint (configure missing libdir)

* Sun Jun 29 2008 Robert M. Albrecht <romal@gmx.de> 3.0.3-1
- Upstream released 3.0.3

* Sun Jun 22 2008 Robert M. Albrecht <romal@gmx.de> 3.0.2-1
- Upstream released 3.0.2

* Mon May 26 2008 Shawn Starr <shawn.starr@rogers.com> 2.12-3
- Fix spec seems to break for Fedora 10+

* Fri May 23 2008 Shawn Starr <shawn.starr@rogers.com> 2.12-2
- Put back fix for Bugzilla #233887

* Fri May 23 2008 Shawn Starr <shawn.starr@rogers.com> 2.12-1
- Upstream released 2.12
- Fixes CVE-2007-5803 XSS issues, Bugzilla #445512

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.11-3
- add Requires for versioned perl (libperl.so)
- get rid of pointless file Requires

* Mon Mar 17 2008 Mike McGrath <mmcgrath@redhat.com> 2.11-2
- Upstream released new version
- Added perl-ExtUtils-Embed

* Tue Feb 12 2008 Mike McGrath <mmcgrath@redhat.com> 2.10-6
- Rebuild for gcc43

* Thu Nov 29 2007 Mike McGrath <mmcgrath@redhat.com> 2.10-5
- Upstream released 2.10
- Renamed cfg-sample configs to just .cfg
- Added BR of perl-devel, libjpeg-devel, libpng-devel

* Wed Sep 26 2007 Mike McGrath <mmcgrath@redhat.com> 2.9-5
- rebuild for koji test

* Sat Sep 08 2007 Mike McGrath <mmcgrath@redhat.com> 2.9-4
- rebuild

* Wed Aug 22 2007 Mike McGrath <mmcgrath@redhat.com> 2.9-3
- Rebuild for ppc32 and license

* Tue Jul 10 2007 Mike McGrath <mmcgrath@redhat.com> 2.9-2
- Release bump

* Fri Jun 29 2007 Mike McGrath <mmcgrath@redhat.com> 2.9-1
- Upstream released 2.9

* Tue Feb 06 2007 Mike McGrath <imlinux@gmail.com> 2.7-2
- Upstream released 2.7

* Thu Nov 30 2006 Mike McGrath <imlinux@gmail.com> 2.6-1
- Upstream released 2.6

* Thu Sep 07 2006 Mike McGrath <imlinux@gmail.com> 2.5-3
- Release bump for mass rebuild

* Wed Aug 02 2006 Mike McGrath <imlinux@gmail.com> 2.5-2
- Fixed default permissions for private and the resource file

* Fri Jul 14 2006 Mike McGrath <imlinux@gmail.com> 2.5-1
- Upstream released 2.5

* Mon Jun 26 2006 Mike McGrath <imlinux@gmail.com> 2.4-2
- Added /usr/bin/nagiostats bz# 194461

* Sun Jun 04 2006 Mike McGrath <imlinux@gmail.com> 2.4-1
- Upstream released 2.4
- Cleaned up changelog

* Mon May 15 2006 Mike McGrath <imlinux@gmail.com> 2.3.1-1
- Bug fix for HTTP content_length header integer overflow in CGIs
- Updates no longer remove Nagios from starting up on reboot

* Tue May 09 2006 Mike McGrath <imlinux@gmail.com> 2.3-3
- updates to the init script that prevented nagios from shutting down

* Wed May 03 2006 Mike McGrath <imlinux@gmail.com> 2.3-1
- Upstream released 2.3
- Bug fix for negative HTTP content_length header in CGIs
- Added missing links for notes_url and action_url to service column of status detail page 

* Tue May 02 2006 Mike McGrath <imlinux@gmail.com> 2.2-3
- Upstream released 2.2

* Tue Feb 21 2006 Mike McGrath <imlinux@gmail.com> 2.0-1
- Upstream released 2.0 (changes below)
- Fix for segfault in timed event queue
- Removed length limitations for object vars/vals
- Updated config.sub and config.guess to versions from automake-1.9
- Doc updates

* Sat Feb 04 2006 Mike McGrath <imlinux@gmail.com> 2.0-0.2.rc2
- Fixed default options in Apache config

* Fri Jan 27 2006 Mike McGrath <imlinux@gmail.com> 2.0-0.1.rc2
- Using 2.0rc2 tarball

* Thu Jan 26 2006 Mike McGrath <imlinux@gmail.com> 1.3-15
- Fixed usermod -a issue, Bugzilla #49609

* Sun Jan 15 2005 Mike McGrath <imlinux@gmail.com> 1.3-14
- Fedora friendly spec file

* Sat May 31 2003 Karl DeBisschop <kdebisschop@users.sourceforge.net> (1.1-1)
- Merge with CVS for 1.1 release

* Fri May 30 2003 Karl DeBisschop <kdebisschop@users.sourceforge.net> (1.0-4)
- cmdgrp was not always getting created
- patches for cmd.cgi and history.cgi

* Sat May 24 2003 Karl DeBisschop <kdebisschop@users.sourceforge.net> (1.0-3)
- patches for doco and PostgreSQL timestamp
- make sure all files are packaged (otherwise, will not build on RH9)

* Sat May 17 2003 Karl DeBisschop <kdebisschop@users.sourceforge.net> (1.0-2)
- patch for file descriptor leak

* Fri Oct 04 2002 Karl DeBisschop <kdebisschop@users.sourceforge.net>
- merge many improvements from Ramiro Morales <rm-rpms@gmx.net>
  (macros for PERF_EXTERNAL and EMBPERL, cleanup pre/post scripts,
  nnmmsg logger macro, include eventhandlers, convertcfg, mini_epn)
- use LSB-standard /etc/init.d/nagios startup location

* Tue Aug 13 2002 Karl DeBisschop <kdebisschop@users.sourceforge.net>
- INSTALL was renamed INSTALLING
- p1.pl script included in package
- web server restarted because Red Hat 7.3 init does not do 'reload'

* Fri Jun 14 2002 Ethan Galstad <nagios@nagios.org) (1.0b4)
- Modified requirements to work when installed using KickStart (Jeff Frost)
- Changed method used for checking for user/group existence (Jeff Frost)

* Tue May 15 2002 Ethan Galstad <nagios@nagios.org) (1.0b1)
- Updated to work with new sample template-based config files (Darren Gamble)

* Sun Feb 17 2002 Ole Gjerde <gjerde@ignus.com> (1.0a4)
- Fixed spec file to work with Nagios

* Wed Jan 17 2001 Karl DeBisschop <kdebisschop@users.sourceforge.net> (0.0.7a5-1)
- switch from /usr/libexec to /usr/lib because linux FHS has no libexec
- use global macro to set location of init script
- fold htaccess.sample into contrib directory of tarball

* Fri Nov 03 2000 Karl DeBisschop <kdebisschop@users.sourceforge.net> (0.0.6-1)
- Rebuild with final sources

* Wed Sep 06 2000 Karl DeBisschop <kdebisschop@users.sourceforge.net> (0.0.6b5-1)
- Create separate cgi, html, and devel packages
- Include commands.cfg

* Sun Aug 27 2000 Karl DeBisschop <kdebisschop@users.sourceforge.net> (0.0.6b5-1)
- beta 5

* Sun Jul 23 2000 Karl DeBisschop <kdebisschop@users.sourceforge.net> (0.0.6b3-2)
- fixes for daemon-init, multi-OS RPM building

* Wed Jul 12 2000 Karl DeBisschop <kdebisschop@users.sourceforge.net> (0.0.6b3-1)
- beta 3

* Sun Jun 25 2000 Karl DeBisschop <kdebisschop@users.sourceforge.net> (0.0.6b2-3)
- true beta2 sources

* Sat Jun 24 2000 Karl DeBisschop <kdebisschop@users.sourceforge.net> (0.0.6b2-2)
- cleanup spec, still using pre-beta2 sources

* Sat Jun 24 2000 Karl DeBisschop <kdebisschop@users.sourceforge.net> (0.0.6b2-1)
- mandrake merge using pre-beta2 sources (many thanks to Stefan van der Eijk <s.vandereijk@chello.nl>)

* Wed Jun 14 2000 Karl DeBisschop <kdebisschop@users.sourceforge.net> (0.0.6b1-1)
- add stylesheet diffs

* Mon Jun 12 2000 Karl DeBisschop <kdebisschop@users.sourceforge.net> (0.0.6b1-1)
- adapt for 0.0.6b1

* Mon Jun 05 2000 Karl DeBisschop <kdebisschop@users.sourceforge.net> (0.0.5-4)
- add traceroute.cgi and htaccess.sample
- move placement of docs (in files) to avoid group warnings
- change www user and group to nobody and add warning

* Mon Jun 05 2000 Karsten Weiss <knweiss@gmx.de> (0.0.5-3)
- official group name
- improved user detection

* Tue Oct 19 1999 Mike McHenry <mmchen@minn.net) (0.0.4-2)
- Fixed init.d scripts to better fit new Redhat init.d script formats

* Fri Sep 03 1999 Mike McHenry <mmchen@minn.net> (0.0.4-1)
- Upgraded package from 0.0.4b4 to 0.0.4

* Mon Aug 16 1999 Mike McHenry <mmchen@minn.net>
- First RPM build (0.0.4b4)

# vim:set ai ts=4 sw=4 sts=4 et:
