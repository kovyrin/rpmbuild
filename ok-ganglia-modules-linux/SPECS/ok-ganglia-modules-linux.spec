%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define ganglia_modules_linux_version 1.3.4
%define package_revision 01

Summary: Ganglia Distributed Monitoring System
Name: ok-ganglia-modules-linux
Version: %{ganglia_modules_linux_version}
Release: %{package_revision}
License: BSD
URL: http://ganglia.info/
Vendor: Ganglia Development Team <ganglia-developers@lists.sourceforge.net>
Group: System Environment/Base
Source: ganglia-modules-linux-%{version}.tar.gz

BuildRequires: apr-devel, ok-ganglia

Requires: apr
Provides: ganglia

%description
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

%prep
%setup -n ganglia-modules-linux-%{version}

%build
./configure --prefix=/opt/ganglia CFLAGS="`apr-1-config --cflags --includes` -I/opt/ganglia/include -L/opt/ganglia/lib" --enable-shared --disable-static
%__make %{?_smp_mflags}

%install
# Flush any old RPM build root
%__rm -rf $RPM_BUILD_ROOT

# Install ganglia
%__make DESTDIR=$RPM_BUILD_ROOT install

%files
%defattr(-,root,root)
/opt/ganglia/lib/ganglia

%clean
%__rm -rf $RPM_BUILD_ROOT

%changelog
* Mon May 6 2013 Oleksiy Kovyrin <alexey@kovyrin.net>
- Initial release for ganglia-plugins-linux 1.3.4.
