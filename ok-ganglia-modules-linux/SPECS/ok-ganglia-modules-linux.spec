%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define ganglia_modules_linux_version 1.3.4
%define git_revision 2f14f6b3eb7305649c0dcea8b12d478cc1048289
%define package_revision 06

Summary: Ganglia Distributed Monitoring System
Name: ok-ganglia-modules-linux
Version: %{ganglia_modules_linux_version}
Release: %{package_revision}+%{git_revision}
License: BSD
URL: http://ganglia.info/
Vendor: Ganglia Development Team <ganglia-developers@lists.sourceforge.net>
Group: System Environment/Base
Source: ganglia-modules-linux-%{version}-%{git_revision}.tar.gz

BuildRequires: apr-devel, ok-ganglia

Requires: apr
Provides: ganglia

%description
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

%prep
%setup -n ganglia-modules-linux

%build
mkdir m4 && autoreconf --install
./configure --prefix=/opt/ganglia CFLAGS="`apr-1-config --cflags --includes` -I/opt/ganglia/include -L/opt/ganglia/lib" --enable-shared --disable-static
%__make %{?_smp_mflags}

# Update config files with correct lib path
%__sed -i 's|/usr/lib/ganglia|/opt/ganglia/lib/ganglia|g' conf.d/*.conf

%install
# Flush any old RPM build root
%__rm -rf $RPM_BUILD_ROOT

# Install ganglia modules
%__make DESTDIR=$RPM_BUILD_ROOT install

# Install configuration files
install -D -m 644 conf.d/mod_fs.conf       %{buildroot}/opt/ganglia/etc/conf.d/mod_fs.conf
install -D -m 644 conf.d/mod_io.conf       %{buildroot}/opt/ganglia/etc/conf.d/mod_io.conf
install -D -m 644 conf.d/mod_multicpu.conf %{buildroot}/opt/ganglia/etc/conf.d/mod_multicpu.conf

%files
%defattr(-,root,root)
/opt/ganglia/lib/ganglia
/opt/ganglia/etc/conf.d

%clean
%__rm -rf $RPM_BUILD_ROOT

%changelog
* Mon May 6 2013 Oleksiy Kovyrin <alexey@kovyrin.net>
- Added configuration files for the modules.

* Mon May 6 2013 Oleksiy Kovyrin <alexey@kovyrin.net>
- Initial release for ganglia-plugins-linux 1.3.4.
