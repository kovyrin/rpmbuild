%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

#----------------------------------------------------------------------------------
%define thrift_home /opt/thrift

%define thrift_version 0.9.0
%define package_revision 02

#---------------------------------------------------------------------------------
Name:           ok-thrift
License:        Apache License v2.0
Group:          Development
Summary:        RPC and serialization framework
Version:        %{thrift_version}
Release:        %{package_revision}
URL:            http://thrift.apache.org/
Source0:        thrift-%{thrift_version}.tar.gz
Source1:        thrift.conf

BuildRequires:  gcc >= 3.4.6
BuildRequires:  gcc-c++
BuildRequires:  byacc
BuildRequires:  boost-devel
BuildRequires:  flex
BuildRequires:  libevent-devel
BuildRequires:  libtool
BuildRequires:  zlib-devel
BuildRequires:  glib2-devel
BuildRequires:  python-devel


BuildRoot:      %{_topdir}/INSTALL/%{name}-%{version}

Requires:       python-devel
Requires:       boost-devel
Requires:       glib2-devel
Requires:       libevent-devel
Requires:       zlib-devel

%description
Thrift is a software framework for scalable cross-language services
development. It combines a powerful software stack with a code generation
engine to build services that work efficiently and seamlessly between C++,
Java, C#, Python, Ruby, Perl, PHP, Objective C/Cocoa, Smalltalk, Erlang,
Objective Caml, and Haskell.

#---------------------------------------------------------------------------------
%files
%defattr(-,root,root)
%{thrift_home}
/etc/ld.so.conf.d/thrift.conf
%{python_sitearch}

#---------------------------------------------------------------------------------
%prep
%setup -q -n thrift-%{thrift_version}

#---------------------------------------------------------------------------------
%build
./configure --prefix=%{thrift_home} \
  --enable-static=yes \
  --with-libevent \
  --with-zlib \
  --with-cpp \
  --with-c_glib \
  --with-python \
  --without-java \
  --without-perl \
  --without-php \
  --without-php_extension \
  --without-csharp \
  --without-ruby \
  --without-erlang \
  CFLAGS='-g -O2' CXXFLAGS='-g -O2'

# Fails with more than one process
make -j1

#---------------------------------------------------------------------------------
%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%__install -d -m 0755 $RPM_BUILD_ROOT/etc/ld.so.conf.d
%__install -m 0644 $RPM_SOURCE_DIR/thrift.conf $RPM_BUILD_ROOT/etc/ld.so.conf.d/thrift.conf

#---------------------------------------------------------------------------------
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
%__rm -rf $RPM_BUILD_ROOT

%changelog
* Tue May 7 2013 Oleksiy Kovyrin <alexey@kovyrin.net>
- Initial release for thrift 0.9.0.
