%define mcelog_version 1.0
%define package_revision 01
%define git_revision d2e13bf0bdc72e9d19d63921056b808d5ce8ef62

Name:     ok-mcelog
Version:  %{mcelog_version}
Release:  %{package_revision}+%{git_revision}
Summary:  Tool to translate x86-64 CPU Machine Check Exception data.
Group:    System Environment/Base
License:  GPLv2
ExclusiveArch: x86_64 i686
Source0:  mcelog-%{git_revision}.tgz

# fix start/stop/status/etc functions in mcelog initscript
Patch0:  mcelog-initscript.patch

# add /var/lock/subsys/mcelogd file
Patch1:  mcelog-lockfile.patch

# set some default config options
Patch2:  mcelog-conf.patch


Provides: mcelog
Obsoletes: mcelog

%description
mcelog is a daemon that collects and decodes Machine Check Exception data on x86-64 and x86 machines.

%prep
%setup -q -n mcelog
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
make CFLAGS="$RPM_OPT_FLAGS -fpie -pie"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{1,8}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/mcelog
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers

install mcelog $RPM_BUILD_ROOT%{_sbindir}/mcelog
install mcelog.cron $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly/mcelog.cron

cp mcelog.8 $RPM_BUILD_ROOT%{_mandir}/man8

install -m 755 mcelog.init $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/mcelogd
cp mcelog.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/mcelogd
cp mcelog.conf $RPM_BUILD_ROOT%{_sysconfdir}/mcelog/mcelog.conf

install -p -m755 triggers/cache-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/cache-error-trigger
install -p -m755 triggers/dimm-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/dimm-error-trigger
install -p -m755 triggers/page-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/page-error-trigger
install -p -m755 triggers/socket-memory-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/socket-memory-error-trigger

cd ..
chmod -R a-s $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
chkconfig --add mcelogd

%files
%defattr(-,root,root,-)

%doc README CHANGES
%{_sbindir}/mcelog
%{_sysconfdir}/cron.hourly/mcelog.cron

%attr(0644,root,root) %{_mandir}/*/*

%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/mcelogd

%{_sysconfdir}/sysconfig/mcelogd
%{_sysconfdir}/mcelog/mcelog.conf
%{_sysconfdir}/mcelog/triggers

%changelog
* Tue Jun 13 2013 Oleksiy Kovyrin <alexey@kovyrin.net> 1.0-01+d2e13bf0bdc72e9d19d63921056b808d5ce8ef62
- Pulled the package into OK repo
- Renamed to ok-mcelog
- Updated to upstream git revision d2e13bf0bdc72e9d19d63921056b808d5ce8ef62

* Fri Jan 11 2013 Stephen Veiss <stephen@scribd.com> 2:0.01_187b1aec83
- Renamed to scribd-mcelog
- Updated to upstream git commit 187b1aec83
- Removed patches merged upstream

* Tue Feb 21 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20110718-0.14
- Add --supported option to mcelog; include misc fixes [BZ 795508] - v2
- added missing man page documentation for --supported option

* Tue Feb 21 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20110718-0.13
- Add --supported option to mcelog; include misc fixes [BZ 795508]

* Thu Feb  9 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20110718-0.12
- cron mcelog: mcelog read: No such device at first boot [BZ 784091]

* Wed Feb  1 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20110718-0.11
- Do not support AMD family > 15 in mcelog, patch updated [BZ 746785]

* Tue Jan 31 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20110718-0.10
- Do not print unsupported CPU message in mcelog [BZ 769363]

* Mon Jan 30 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20110718-0.9
- Do not support AMD family > 15 in mcelog [BZ 746785]

* Tue Jan 26 2012 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20110718-0.8
- RHEL6 mcelog: Update README RPM package [BZ 728265]

* Mon Jul 18 2011 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20110718-0.7
- Updated to 1.0pre3 as of Jul 18 2011/cbd4da48 [BZ 699592]
- chkconfig mcelogd on by default [BZ 699592]

* Mon Mar 07 2011 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20101112-0.6
- comment out default error handling in /etc/mcelog/mcelog.conf [BZ 682753]

* Tue Feb 22 2011 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20101112-0.5
- fix type in LOCKFILE location [BZ 614874]

* Tue Nov 16 2010 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20101112-0.4
- add /etc/mcelog/mcelog.conf file [BZ 647066]

* Mon Nov 15 2010 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20101112-0.3
- add /var/lock/subsys/mcelogd lockfile [BZ 614874]

* Mon Nov 15 2010 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3_20101112-0.2
- updated to 1.0pre3 as of Nov 12 2010 [BZ 646568]
- pulled from %{URL}

* Thu Apr 08 2010 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3-0.2
- fixed initscript and added /etc/sysconfig/mcelog (BZ 576284)

* Wed Jan 27 2010 Prarit Bhargava <prarit@redhat.com> 1:1.0pre3-0.1
- updated to 1.0pre3
- added initscript for Predictive Failure Analysis (PFA) which does not
  run by default.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1:0.9pre1-0.2
- Rebuilt for RHEL 6

* Mon Oct 05 2009 Orion Poplawski <orion@cora.nwra.com> - 1:0.9pre1-0.1
- Update to 0.9pre1
- Update URL
- Add patch to update mcelog kernel record length (bug #507026)

* Tue Aug 04 2009 Adam Jackson <ajax@redhat.com> 0.7-5
- Fix %%install for new buildroot cleanout.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.7-2
- fix license tag
- clean this package up

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:0.7-1.22
- Autorebuild for GCC 4.3

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com>
- Rebuild.

* Fri Jun 30 2006 Dave Jones <davej@redhat.com>
- Rebuild. (#197385)

* Wed May 17 2006 Dave Jones <davej@redhat.com>
- Update to upstream 0.7
- Change frequency to hourly instead of daily.

* Thu Feb 09 2006 Dave Jones <davej@redhat.com>
- rebuild.

* Wed Feb  8 2006 Dave Jones <davej@redhat.com>
- Update to upstream 0.6

* Mon Dec 19 2005 Dave Jones <davej@redhat.com>
- Update to upstream 0.5

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild for gcc4

* Wed Feb  9 2005 Dave Jones <davej@redhat.com>
- Update to upstream 0.4

* Thu Jan 27 2005 Dave Jones <davej@redhat.com>
- Initial packaging.

