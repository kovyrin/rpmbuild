%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define __getent   /usr/bin/getent
%define __useradd  /usr/sbin/useradd
%define __userdel  /usr/sbin/userdel
%define __groupadd /usr/sbin/groupadd
%define __touch    /bin/touch
%define __service  /sbin/service

#---------------------------------------------------------------------------------------------------
%define carbon_version 0.9.10
%define ok_version 01
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

Patch0:         carbon-setup.patch
Patch1:         carbon-config.patch

BuildArch:      noarch

BuildRequires:  python python-devel python-setuptools
Requires:       python ok-whisper
Requires:       python-twisted-core >= 8.2

%description
The backend for Graphite. Carbon is a data collection and storage agent.

%prep
%setup -q -n carbon
%patch0 -p1
%patch1 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} -c 'import setuptools; execfile("setup.py")' build

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}

# Create log and var directories
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/carbon-cache
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/carbon-relay
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/carbon-aggregator
%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/carbon

# Install system configuration and init scripts
%{__install} -Dp -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/carbon-cache
%{__install} -Dp -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/carbon-cache
%{__install} -Dp -m0755 %{SOURCE3} %{buildroot}%{_initrddir}/carbon-relay
%{__install} -Dp -m0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/carbon-relay
%{__install} -Dp -m0755 %{SOURCE5} %{buildroot}%{_initrddir}/carbon-aggregator
%{__install} -Dp -m0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/carbon-aggregator

# Install default configuration files
%{__mkdir_p} %{buildroot}%{_sysconfdir}/carbon
%{__install} -Dp -m0644 conf/carbon.conf.example %{buildroot}%{_sysconfdir}/carbon/carbon.conf
%{__install} -Dp -m0644 conf/storage-schemas.conf.example %{buildroot}%{_sysconfdir}/carbon/storage-schemas.conf

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
%{__getent} group carbon >/dev/null || %{__groupadd} -r carbon
%{__getent} passwd carbon >/dev/null || \
    %{__useradd} -r -g carbon -d %{_localstatedir}/lib/carbon \
    -s /sbin/nologin -c "Carbon cache daemon" carbon
exit 0

%preun
%{__service} carbon stop
exit 0

%postun
if [ $1 = 0 ]; then
  %{__getent} passwd carbon >/dev/null && \
      %{__userdel} -r carbon 2>/dev/null
fi
exit 0

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.md conf/*

%{python_sitelib}/*
/usr/bin/*
%{_initrddir}/carbon-cache
%{_initrddir}/carbon-relay
%{_initrddir}/carbon-aggregator

%config %{_sysconfdir}/carbon
%config %{_sysconfdir}/sysconfig/carbon-cache
%config %{_sysconfdir}/sysconfig/carbon-relay
%config %{_sysconfdir}/sysconfig/carbon-aggregator

%attr(-,%name,%name) %{_localstatedir}/lib/carbon
%attr(-,%name,%name) %{_localstatedir}/log/carbon-cache
%attr(-,%name,%name) %{_localstatedir}/log/carbon-relay
%attr(-,%name,%name) %{_localstatedir}/log/carbon-aggregator

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
