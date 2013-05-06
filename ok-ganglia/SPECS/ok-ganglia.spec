%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define ganglia_version 3.5.0
%define package_revision 06

Summary: Ganglia Distributed Monitoring System
Name: ok-ganglia
Version: %{ganglia_version}
Release: %{package_revision}
License: BSD
URL: http://ganglia.info/
Vendor: Ganglia Development Team <ganglia-developers@lists.sourceforge.net>
Group: System Environment/Base
Source: ganglia-%{version}.tar.gz

BuildRequires: libpng-devel, libart_lgpl-devel, gcc-c++, python-devel, libconfuse-devel, make, pcre-devel, autoconf, automake, libtool, pkgconfig
BuildRequires: rrdtool, expat
BuildRequires: expat-devel, rrdtool-devel, freetype-devel, apr-devel

Requires: python, libconfuse, apr

Provides: ganglia
Provides: ganglia-devel
Provides: ganglia-gmond
Provides: ganglia-gmetad
Provides: gmond-python

Obsoletes: ganglia
Obsoletes: ganglia-devel
Obsoletes: ganglia-gmond
Obsoletes: ganglia-gmetad
Obsoletes: gmond-python

%description
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

%prep
%setup -n ganglia-%{version}

%build
./configure --with-gmetad --with-python=/usr --enable-status --prefix=/opt/ganglia --enable-graphite
%__make %{?_smp_mflags}

%post
/sbin/chkconfig --add gmetad
/sbin/chkconfig --add gmond
/sbin/ldconfig

%preun
/sbin/chkconfig --del gmetad
/sbin/chkconfig --del gmond

%install
# Flush any old RPM build root
%__rm -rf $RPM_BUILD_ROOT

# Install ganglia
%__make DESTDIR=$RPM_BUILD_ROOT install

# Create the RRDs directory
%__install -d -m 0755 $RPM_BUILD_ROOT/var/lib/ganglia/rrds

# Install startup scripts
%__install -D -m 0755 $RPM_SOURCE_DIR/gmond.init $RPM_BUILD_ROOT/etc/rc.d/init.d/gmond
%__install -D -m 0755 $RPM_SOURCE_DIR/gmetad.init $RPM_BUILD_ROOT/etc/rc.d/init.d/gmetad
%__install -D -m 0644 gmetad/gmetad-default $RPM_BUILD_ROOT/etc/sysconfig/gmetad

# Install ld.so config
%__install -D -m 0644 $RPM_SOURCE_DIR/ganglia-ld-so.conf $RPM_BUILD_ROOT/etc/ld.so.conf.d/ganglia.conf

# Create config directories
%__install -d -m 0755 $RPM_BUILD_ROOT/opt/ganglia/etc
%__install -d -m 0755 $RPM_BUILD_ROOT/opt/ganglia/etc/conf.d

# Install configs
gmond/gmond -t > $RPM_BUILD_ROOT/opt/ganglia/etc/gmond.conf
%__cp -f gmetad/gmetad.conf $RPM_BUILD_ROOT/opt/ganglia/etc/gmetad.conf
%__cp -f gmond/modules/conf.d/* $RPM_BUILD_ROOT/opt/ganglia/etc/conf.d

# Do some cleanup of installed files
rm -f $RPM_SOURCE_DIR/opt/ganglia/etc/conf.d/*.in
rm -f $RPM_SOURCE_DIR/opt/ganglia/etc/conf.d/example.*

%files
%defattr(-,root,root)
/opt/ganglia
/etc/rc.d/init.d/gmond
/etc/rc.d/init.d/gmetad
/etc/sysconfig/gmetad
/etc/ld.so.conf.d/ganglia.conf

%defattr(-,nobody,nobody)
%dir /var/lib/ganglia

%clean
%__rm -rf $RPM_BUILD_ROOT

%changelog
* Mon May 3 2013 Oleksiy Kovyrin <alexey@kovyrin.net>
- Updated startup scripts to use pid files for process management.

* Mon Mar 4 2013 Oleksiy Kovyrin <alexey@kovyrin.net>
- Enable graphite integration.

* Mon Feb 11 2013 Oleksiy Kovyrin <alexey@kovyrin.net>
- Initial release for Ganglia 3.5.0.

* Mon Feb 11 2013 Oleksiy Kovyrin <alexey@kovyrin.net>
- Initial release for Ganglia 3.5.0.
