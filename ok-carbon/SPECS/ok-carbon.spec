%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define __getent   /usr/bin/getent
%define __useradd  /usr/sbin/useradd
%define __userdel  /usr/sbin/userdel
%define __groupadd /usr/sbin/groupadd
%define __touch    /bin/touch
%define __service  /sbin/service

#---------------------------------------------------------------------------------------------------
%define carbon_version 0.9.10
%define ok_version 04
%define carbon_revision 728e6a1eafa483bc290c601f777d7aebbc5c8565

Name:           ok-carbon
Version:        %{carbon_version}
Release:        %{ok_version}+%{carbon_revision}
Summary:        Backend data caching and persistence daemon for Graphite
Group:          Applications/Internet
License:        Apache Software License 2.0
URL:            https://launchpad.net/graphite
Vendor:         Chris Davis <chrismd@gmail.com>
Packager:       Dan Carley <dan.carley@gmail.com>

Source0:        carbon-%{carbon_revision}.tar.gz
Source1:        carbon-cache.init
Source2:        carbon-cache.sysconfig
Source3:        carbon-relay.init
Source4:        carbon-relay.sysconfig
Source5:        carbon-aggregator.init
Source6:        carbon-aggregator.sysconfig

BuildArch:      noarch

BuildRequires:  python python-devel python-setuptools
Requires:       python ok-whisper
Requires:       python-twisted-core >= 8.2

%description
The backend for Graphite. Carbon is a data collection and storage agent.

%prep
%setup -q -n carbon

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} -c 'import setuptools; execfile("setup.py")' build

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}

# Install system configuration and init scripts
%{__install} -Dp -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/carbon-cache
%{__install} -Dp -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/carbon-cache
%{__install} -Dp -m0755 %{SOURCE3} %{buildroot}%{_initrddir}/carbon-relay
%{__install} -Dp -m0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/carbon-relay
%{__install} -Dp -m0755 %{SOURCE5} %{buildroot}%{_initrddir}/carbon-aggregator
%{__install} -Dp -m0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/carbon-aggregator

# Create transient files in buildroot for ghosting
%{__mkdir_p} %{buildroot}%{_localstatedir}/lock/subsys
%{__touch} %{buildroot}%{_localstatedir}/lock/subsys/carbon-cache
%{__touch} %{buildroot}%{_localstatedir}/lock/subsys/carbon-relay
%{__touch} %{buildroot}%{_localstatedir}/lock/subsys/carbon-aggregator

%{__mkdir_p} %{buildroot}%{_localstatedir}/run
%{__touch} %{buildroot}%{_localstatedir}/run/carbon-cache.pid
%{__touch} %{buildroot}%{_localstatedir}/run/carbon-relay.pid
%{__touch} %{buildroot}%{_localstatedir}/run/carbon-aggregator.pid

%pre
%{__getent} group graphite >/dev/null || %{__groupadd} -r graphite
%{__getent} passwd graphite >/dev/null || %{__useradd} -r -g graphite -d /opt/graphite -s /sbin/nologin -c "Graphite Daemons" graphite
exit 0

%preun
%{__service} carbon stop
exit 0

%postun
if [ $1 = 0 ]; then
  %{__getent} passwd graphite >/dev/null && %{__userdel} -r graphite 2>/dev/null
fi
exit 0

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.md conf/*

/opt/graphite/bin
/opt/graphite/lib
%{_initrddir}/carbon-cache
%{_initrddir}/carbon-relay
%{_initrddir}/carbon-aggregator

%config /opt/graphite/conf/*
%config %{_sysconfdir}/sysconfig/carbon-cache
%config %{_sysconfdir}/sysconfig/carbon-relay
%config %{_sysconfdir}/sysconfig/carbon-aggregator

%attr(-,graphite,graphite) /opt/graphite/storage

%ghost %{_localstatedir}/lock/subsys/carbon-cache
%ghost %{_localstatedir}/run/carbon-cache.pid
%ghost %{_localstatedir}/lock/subsys/carbon-relay
%ghost %{_localstatedir}/run/carbon-relay.pid
%ghost %{_localstatedir}/lock/subsys/carbon-aggregator
%ghost %{_localstatedir}/run/carbon-aggregator.pid

%changelog
* Fri Jun 1 2012 Ben P <ben@g.megatron.org> - 0.9.10-1
- New upstream version.

* Fri Feb 17 2012 Justin Burnham <justin@jburnham.net> - 0.9.9-4
- Standardized naming to make things more specific.
- Old carbon init script is now called carbon-cache.
- Adding carbon-relay and carbon-aggregator support.

* Wed Nov 2 2011 Dan Carley <dan.carley@gmail.com> - 0.9.9-3
- Correct python-twisted-core dependency from 0.8 to 8.0

* Mon Oct 17 2011 Dan Carley <dan.carley@gmail.com> - 0.9.9-2
- Fix config for relocated data directories.

* Sat Oct 8 2011 Dan Carley <dan.carley@gmail.com> - 0.9.9-1
- New upstream version.

* Mon May 23 2011 Dan Carley <dan.carley@gmail.com> - 0.9.8-2
- Repackage with minor changes.
- Require later version of python-twisted-core to fix textFromEventDict error.

* Tue Apr 19 2011 Chris Abernethy <cabernet@chrisabernethy.com> - 0.9.8-1
- Update source to upstream v0.9.8
- Minor updates to spec file

* Thu Mar 17 2011 Daniel Aharon <daharon@sazze.com> - 0.9.7-1
- Add dependencies, description, init script and sysconfig file.
