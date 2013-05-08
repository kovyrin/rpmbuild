%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
#----------------------------------------------------------------------------------
%define thrift_home /opt/thrift

%define thrift_version 0.9.0
%define package_revision 02

#---------------------------------------------------------------------------------
Name:           ok-fb303
License:        Apache License v2.0
Group:          Development
Summary:        Project FB303: The Facebook Bassline
Version:        %{thrift_version}
Release:        %{package_revision}
URL:            http://developers.facebook.com/thrift
Source0:        thrift-%{thrift_version}.tar.gz
Patch0:         0001-Thrift-1668-Compile-error-in-contrib-fb303-thrift-TD.patch

BuildRequires:  gcc >= 3.4.6
BuildRequires:  gcc-c++
BuildRequires:  byacc
BuildRequires:  boost-devel
BuildRequires:  flex
BuildRequires:  libevent-devel
BuildRequires:  libtool
BuildRequires:  zlib-devel
BuildRequires:  ok-thrift = %{thrift_version}

BuildRoot:      %{_topdir}/INSTALL/%{name}-%{version}

Requires:       boost-devel
Requires:       ok-thrift = %{thrift_version}

%description
A standard interface to monitoring, dynamic options and configuration,
uptime reports, activity, etc.

#---------------------------------------------------------------------------------
%files
%defattr(-,root,root)
/opt/fb303
%{python_sitelib}

#---------------------------------------------------------------------------------
%prep
%setup -q -n thrift-%{thrift_version}
%patch0 -p1

#---------------------------------------------------------------------------------
%build
cd contrib/fb303

./bootstrap.sh \
    --prefix=/opt/fb303 \
    --with-thriftpath=%{thrift_home} \
    --enable-static \

make -j1

%install
rm -rf %{buildroot}
cd contrib/fb303

make DESTDIR=%{buildroot} install

#---------------------------------------------------------------------------------
%clean
rm -rf %{buildroot}
