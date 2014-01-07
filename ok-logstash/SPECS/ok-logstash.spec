# do not repack jar files
%define __os_install_post %{nil}
%define __jar_repack %{nil}

# do not build debug packages
%define debug_package %{nil}

#---------------------------------------------------------------------------------------------------
%define base_install_dir /opt/logstash

%define logstash_version 1.1.13
%define package_revision 02

Name:           ok-logstash
Version:        %{logstash_version}
Release:        %{package_revision}%{?dist}
Summary:        Logstash is a tool for managing events and logs.

Group:          System Environment/Daemons
License:        Apache License, Version 2.0
URL:            http://logstash.net
Source0:        http://semicomplete.com/files/logstash/logstash-%{version}-flatjar.jar
Source1:        logstash.init
Source2:        logstash.logrotate
Source3:        logstash.sysconfig

Requires:       java

Requires(post): chkconfig initscripts
Requires(pre):  chkconfig initscripts
Requires(pre):  shadow-utils

%description
Logstash is a tool for managing events and logs

%prep
true

%build
true

%install
rm -rf $RPM_BUILD_ROOT

%{__mkdir} -p %{buildroot}%{base_install_dir}
%{__mkdir} -p %{buildroot}%{base_install_dir}/lib
%{__install} -m 755 %{SOURCE0} %{buildroot}%{base_install_dir}/lib/logstash.jar

# config dir
%{__mkdir} -p %{buildroot}%{_sysconfdir}/logstash/conf.d

# plugins & patterns
%{__mkdir} -p %{buildroot}%{base_install_dir}/plugins
%{__mkdir} -p %{buildroot}%{_sysconfdir}/patterns

# logs
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/logstash
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/logstash

# sysconfig and init
%{__mkdir} -p %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/logstash
%{__install} -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/logstash

%{__mkdir} -p %{buildroot}%{_localstatedir}/run/logstash
%{__mkdir} -p %{buildroot}%{_localstatedir}/lock/subsys/logstash
%{__mkdir} -p %{buildroot}%{base_install_dir}/tmp

%pre
# create logstash group
if ! getent group logstash >/dev/null; then
        groupadd -r logstash
fi

# create logstash user
if ! getent passwd logstash >/dev/null; then
        useradd -r -g logstash -d %{base_install_dir} \
            -s /sbin/nologin -c "Logstash" logstash
fi

%post
/sbin/chkconfig --add logstash

%preun
if [ $1 -eq 0 ]; then
  /sbin/service logstash stop >/dev/null 2>&1
  /sbin/chkconfig --del logstash
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{base_install_dir}
%dir %{base_install_dir}/plugins
%dir %{_sysconfdir}/patterns

%{_sysconfdir}/rc.d/init.d/logstash
%{_sysconfdir}/logrotate.d/logstash

%config(noreplace) %{_sysconfdir}/sysconfig/logstash

%{base_install_dir}/lib/*

%defattr(-,logstash,logstash,-)
%{_localstatedir}/run/logstash
%{base_install_dir}/tmp
%dir %{_localstatedir}/log/logstash


%changelog
* Fri Jan 6 2014 Oleksiy Kovyrin <alexey@kovyrin.net> - 1.1.13-02
- Updated upstream version to 1.1.13
- Replaced startup script with a better one

* Fri May 24 2013 Oleksiy Kovyrin <alexey@kovyrin.net> - 1.1.12-01
- Added to ok packages, updated upstream version to 1.1.12

* Fri Jan 11 2013 Aaron Blew <aaronblew@gmail.com> - 1.1.9-3
- Package update
- Allow overwriting the user/group via sysconfig file

* Mon Nov  5 2012 Dan Carley <dan.carley@gmail.com> - 1.1.0.1-2
- Fix variable handling of default log level.
- Document available log levels.

* Fri May  4 2012 Maksim Horbul <max@gorbul.net> - 1.1.0-1
- Initial package
