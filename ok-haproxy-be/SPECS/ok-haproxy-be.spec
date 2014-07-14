%define haproxy_home /opt/haproxy-be

%define haproxy_version 1.5.2
%define ok_revision 06

#---------------------------------------------------------------------------------
Name:           ok-haproxy-be
License:        GPL v2
Group:          Development
Summary:        The Reliable, High Performance TCP/HTTP Load Balancer
Version:        %{haproxy_version}
Release:        %{ok_revision}
URL:            http://haproxy.1wt.eu/
Source0:        haproxy-%{haproxy_version}.tar.gz
Source1:        haproxy.init
#Source2:        generate-haproxy-config

BuildRequires:  gcc >= 3.4.6
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  zlib-devel
BuildRequires:  pcre-devel
BuildRequires:  openssl-devel

Requires:       zlib
Requires:       pcre
Requires:       openssl

%description
The Reliable, High Performance TCP/HTTP Load Balancer

#---------------------------------------------------------------------------------
%files
%defattr(-,root,root)
%{haproxy_home}
/etc/rc.d/init.d/haproxy-be

#---------------------------------------------------------------------------------
%prep
%setup -n haproxy-%{version}

#---------------------------------------------------------------------------------
%build
make TARGET=linux26 PREFIX=%{haproxy_home} USE_PCRE=1 USE_REGPARM=1 CPU=native ARCH=x86_64

%install
rm -rf %{buildroot}

install -D -m 755 ./haproxy %{buildroot}%{haproxy_home}/bin/haproxy-%{haproxy_version}
install -D -m 755 $RPM_SOURCE_DIR/haproxy.init %{buildroot}/etc/rc.d/init.d/haproxy-be
#install -D -m 755 $RPM_SOURCE_DIR/generate-haproxy-config %{buildroot}%{haproxy_home}/conf/generate-haproxy-config

#---------------------------------------------------------------------------------
%post
ln -sf %{haproxy_home}/bin/haproxy-%{haproxy_version} %{haproxy_home}/bin/haproxy-be

#---------------------------------------------------------------------------------
%clean
rm -rf %{buildroot}

%changelog
* Mon Jul 14 2014 Oleksiy Kovyrin <alexey@kovyrin.net> - haproxy-1.5.2-06
- Do not start the process if it already running
- Do not try to stop the process if it is down
* Mon Jul 14 2014 Oleksiy Kovyrin <alexey@kovyrin.net> - haproxy-1.5.2-05
- Upgraded to the latest stable version from upstream
- Fixed status command in the init script
* Wed Mar 26 2014 Oleksiy Kovyrin <alexey@kovyrin.net> - be-master-55ec6bde6f18bfdcde08d2b1883f4ed9a11a2a04-03
- Added better restart/reload/force-restart actions to init script
* Mon Mar 17 2014 Oleksiy Kovyrin <alexey@kovyrin.net> - be-master-55ec6bde6f18bfdcde08d2b1883f4ed9a11a2a04-02
- Upgraded to the latest master: git revision 55ec6bde6f18bfdcde08d2b1883f4ed9a11a2a04
* Fri Jan 24 2014 Anton Koshevoy <nowarry@gmail.com> - be-dev21
- Upgraded haproxy to be-dev21.
* Thu Aug 22 2013 Oleksiy Kovyrin <alexey@kovyrin.net> - 1.4.24-01
- Upgraded haproxy to 1.4.24.
