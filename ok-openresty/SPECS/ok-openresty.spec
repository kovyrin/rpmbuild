%define openresty_home /opt/openresty

%define openresty_version 1.7.10.2
%define openresty_revision 01

#---------------------------------------------------------------------------------
Name:           ok-openresty
License:        GPL v2
Group:          Development
Summary:        Full-fledged web application server based on the standard Nginx core
Version:        %{openresty_version}
Release:        %{openresty_revision}
URL:            http://openresty.org/
Source0:        ngx_openresty-%{version}.tar.gz
Source1:        nginx-openresty.init
Source2:        nginx-openresty.sysconfig

BuildRequires:  perl
BuildRequires:  gcc >= 3.4.6
BuildRequires:  readline-devel
BuildRequires:  zlib-devel
BuildRequires:  pcre-devel
BuildRequires:  openssl-devel

Requires:       zlib
Requires:       pcre
Requires:       openssl
Requires:       readline

Provides:      openresty

%description
OpenResty (aka. ngx_openresty) is a full-fledged web application server by bundling the standard Nginx core,
lots of 3rd-party Nginx modules, as well as most of their external dependencies.

%prep
%setup -n ngx_openresty-%{version}

%build
./configure  --prefix=%{openresty_home} \
             --user=nginx \
             --group=nginx \
             --with-http_ssl_module \
             --with-http_gzip_static_module \
             --with-http_stub_status_module \
             --with-luajit \
             --with-debug

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install
mv %{buildroot}%{openresty_home}/nginx/conf %{buildroot}%{openresty_home}/nginx/conf.example

install -D -m 755 $RPM_SOURCE_DIR/nginx-openresty.init %{buildroot}/etc/rc.d/init.d/nginx-openresty
install -D -m 644 $RPM_SOURCE_DIR/nginx-openresty.sysconfig %{buildroot}/etc/sysconfig/nginx-openresty

%pre
# Add the "nginx" user
getent group nginx >/dev/null || groupadd -r nginx
getent passwd nginx >/dev/null || \
    useradd -r -g nginx -s /sbin/nologin \
        -d /opt/openresty -c "nginx user" nginx
exit 0

%post
# Register the service
/sbin/chkconfig --add nginx-openresty

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{openresty_home}
/etc/rc.d/init.d/nginx-openresty
/etc/sysconfig/nginx-openresty

%changelog
* Fri Jul 10 2015 Oleksiy Kovyrin <alexey@kovyrin.net> - 1.7.10.2-01
- New upstream release.

* Mon May 20 2013 Oleksiy Kovyrin <alexey@kovyrin.net> - 1.2.7.8-05
- Do not touch configs in /opt/openresty/nginx/conf.

* Fri May 17 2013 Oleksiy Kovyrin <alexey@kovyrin.net> - 1.2.7.8-03
- Initial release for ngx_openresty 1.2.7.8.
