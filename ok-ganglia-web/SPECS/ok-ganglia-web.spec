%define ganglia_web_version 3.5.4
%define package_revision 02

Summary: Ganglia Distributed Monitoring System Web Interface
Name: ok-ganglia-web
Version: %{ganglia_web_version}
Release: %{package_revision}
License: BSD
URL: http://ganglia.info/
Vendor: Ganglia Development Team <ganglia-developers@lists.sourceforge.net>
Group: System Environment/Base
Source: ganglia-web-%{version}.tar.gz
BuildArch: noarch

BuildRequires: make

Requires: make
Requires: rsync
Requires: httpd
Requires: php
Requires: rrdtool
Requires: ok-ganglia

Provides: ganglia-web
Obsoletes: ganglia-web

%description
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This package provides a web frontend to display the XML tree published by
ganglia, and to provide historical graphs of collected metrics. This website is
written in the PHP language.

%prep
%setup -n ganglia-web-%{version}

%build
sed -i 's|/var/www/html/gweb|/opt/ganglia-web|g' Makefile
sed -e 's|@varstatedir@|/var/lib|' conf_default.php.in > conf_default.php

%install
# Flush any old RPM build root
%__rm -rf $RPM_BUILD_ROOT

# Create ganglia-web home directory
%__install -d -m 0755 $RPM_BUILD_ROOT/opt/ganglia-web

# Copy files there
cp -ax * $RPM_BUILD_ROOT/opt/ganglia-web/


# Create /var directories
%__install -d -m 0755 $RPM_BUILD_ROOT/var/lib/ganglia/dwoo
%__install -d -m 0755 $RPM_BUILD_ROOT/var/lib/ganglia/dwoo/cache
%__install -d -m 0755 $RPM_BUILD_ROOT/var/lib/ganglia/dwoo/compiled
%__install -d -m 0755 $RPM_BUILD_ROOT/var/lib/ganglia/conf

# Copy configs to dest dir
cp -ax conf/* $RPM_BUILD_ROOT/var/lib/ganglia/conf

%files
%defattr(-,root,root)
/opt/ganglia-web
/var/lib/ganglia/conf

%defattr(-,apache,apache)
/var/lib/ganglia/conf
/var/lib/ganglia/dwoo

%clean
%__rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Feb 14 2013 Oleksiy Kovyrin <alexey@kovyrin.net>
- Initial release for Ganglia Web 3.5.4.
