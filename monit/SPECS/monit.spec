Name: monit
Version: 5.10
Release: 1
Summary: MONIT. Barking at daemons.

Group: Applications/Internet
License: AGPL
URL: http://mmonit.com/monit/
Source0: monit-%{version}-linux-x64.tar.gz
Source1: monit-init

%define debug_package %{nil}

%description
Monit is a small Open Source utility for managing and monitoring Unix systems.

%prep
%setup -T -b 0

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/monit.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/init.d

install -m 755 bin/monit $RPM_BUILD_ROOT%{_bindir}/monit

cp man/man1/monit.1 $RPM_BUILD_ROOT%{_mandir}/man1

install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/monit
install -m 700 conf/monitrc $RPM_BUILD_ROOT%{_sysconfdir}/monitrc

%files
%defattr(-,root,root)
%{_sysconfdir}/init.d/monit
%{_bindir}/monit
%{_mandir}/man1/monit.1.gz
%{_sysconfdir}/monitrc

%post
chkconfig --add monit

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Nov 7 2014 Vadzim Tonka <vadim@swiftype.com> - 5.10-1
- Initial build
