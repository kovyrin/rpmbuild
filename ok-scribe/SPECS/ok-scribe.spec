%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
#----------------------------------------------------------------------------------
%define scribe_home /opt/scribe

%define scribe_version 2.2
%define package_revision 01
%define scribe_revision 7359a099ed64278849909b363b7f2f0ba059808d

#----------------------------------------------------------------------------------
Name:             ok-scribe
Version:          %{scribe_version}
Release:          %{package_revision}+%{scribe_revision}
Summary:          A server for aggregating log data streamed in real time

Group:            Development/Libraries
License:          ASL 2.0
URL:              https://github.com/facebook/scribe
Source0:          scribe-master-%{scribe_revision}.tar.gz
Source1:          scribed.init

BuildRoot:        %{_topdir}/INSTALL/%{name}-%{version}

BuildRequires:    automake
BuildRequires:    boost-devel
BuildRequires:    ok-fb303
BuildRequires:    ok-thrift
BuildRequires:    libevent-devel
BuildRequires:    python-devel

Requires:         boost
Requires:         python
Requires:         ok-thrift
Requires:         ok-fb303
Requires:         libevent
Requires(post):   chkconfig

#----------------------------------------------------------------------------------
%description
Scribe is a server for aggregating log data streamed in real time from a large
number of servers. It is designed to be scalable, extensible without
client-side modification, and robust to failure of the network or any specific
machine.

#----------------------------------------------------------------------------------
%prep
%setup -q -n scribe-master

#----------------------------------------------------------------------------------
%build
./bootstrap.sh --prefix=%{scribe_home} \
               --with-thriftpath=/opt/thrift \
               --with-fb303path=/opt/fb303 \
               --with-boost-filesystem=boost_filesystem \
               --enable-static \
               CXXFLAGS="-DHAVE_INTTYPES_H" CPPFLAGS="-DHAVE_NETINET_IN_H"

 %{__make} %{?_smp_mflags}
# BOOST_FILESYSTEM_VERSION=2

#----------------------------------------------------------------------------------
%install
rm -rf %{buildroot}

%{__make} DESTDIR=%{buildroot} install

# Install configs and bin scripts manually
install -D -m 755 ./examples/scribe_ctrl %{buildroot}%{scribe_home}/bin/scribe_ctrl
install -D -m 755 ./examples/scribe_cat %{buildroot}%{scribe_home}/bin/scribe_cat
install -D -m 644 ./examples/example1.conf %{buildroot}%{scribe_home}/conf/default.conf
install -D -m 755 $RPM_SOURCE_DIR/scribed.init %{buildroot}/etc/rc.d/init.d/scribed

#----------------------------------------------------------------------------------
%pre
/usr/sbin/groupadd -f scribe
getent passwd scribe || /usr/sbin/useradd -c "Scribe Log Server" -s /sbin/nologin -g scribe -r -d %{scribe_home} scribe || :

%__install -d -m 0777 -o scribe -g scribe /var/log/scribe
%__install -d -m 0755 -o scribe -g scribe /var/run/scribe

#----------------------------------------------------------------------------------
%clean
rm -rf %{buildroot}

#----------------------------------------------------------------------------------
%files
%defattr(-,scribe,scribe,-)
%{scribe_home}
%{python_sitelib}

%defattr(0755,root,root)
/etc/rc.d/init.d/scribed
