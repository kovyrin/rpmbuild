#-------------------------------------------------------------------------------
%define statsd_home /opt/statsd

%define statsd_version 0.6.0
%define ok_version 03
%define statsd_revision d16d744e6424dfd519dc71795a212ad1c08c3114

#-------------------------------------------------------------------------------

Name:           ok-statsd
Version:        %{statsd_version}
Release:        %{ok_version}+%{statsd_revision}
Summary:        Monitoring daemon, that aggregates events received by udp in 10 second intervals
Group:          Applications/Internet
License:        Etsy open source license
URL:            https://github.com/etsy/statsd
Vendor:         Etsy
Packager:       Oleksiy Kovyrin <alexey@kovyrin.net>
Source0:        statsd-%{statsd_revision}.zip
Source1:        statsd.init
BuildArch:      noarch

Requires:       ok-nodejs

#-------------------------------------------------------------------------------
%description
Simple daemon for easy stats aggregation

#-------------------------------------------------------------------------------
%prep
%setup -q -n statsd-master

#-------------------------------------------------------------------------------
%build
echo "Build not needed..."

#-------------------------------------------------------------------------------
%install
# Install js files
%{__mkdir_p} %{buildroot}%{statsd_home}
%{__mkdir_p} %{buildroot}%{statsd_home}/bin
%{__mkdir_p} %{buildroot}%{statsd_home}/lib
%{__mkdir_p} %{buildroot}%{statsd_home}/backends

%{__install} -Dp -m0644 stats.js %{buildroot}%{statsd_home}
%{__install} -Dp -m0755 bin/statsd %{buildroot}%{statsd_home}/bin
%{__install} -Dp -m0644 lib/*.js %{buildroot}%{statsd_home}/lib
%{__install} -Dp -m0644 backends/{console.js,graphite.js} %{buildroot}%{statsd_home}/backends

# Install init script
%{__install} -Dp -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/statsd

# Install default configuration files
%{__install} -Dp -m0644 exampleConfig.js  %{buildroot}%{statsd_home}/config.js

#-------------------------------------------------------------------------------
%pre
getent group statsd >/dev/null || groupadd -r statsd
getent passwd statsd >/dev/null || useradd -r -g statsd -d %{statsd_home} -s /sbin/nologin -c "statsd daemon" statsd
exit 0

#-------------------------------------------------------------------------------
%preun
service statsd stop
exit 0

#-------------------------------------------------------------------------------
%postun
if [ $1 = 0 ]; then
	chkconfig --del statsd
	getent passwd statsd >/dev/null && userdel -r statsd 2>/dev/null
fi
exit 0

#-------------------------------------------------------------------------------
%post
chkconfig --add statsd

#-------------------------------------------------------------------------------
%clean
rm -rf %{buildroot}

#-------------------------------------------------------------------------------
%files
%defattr(-,root,root,-)
%doc LICENSE README.md Changelog.md
%doc examples
%doc exampleConfig.js

%{statsd_home}
%{_initrddir}/statsd

#-------------------------------------------------------------------------------
%changelog
* Tue Jun 25 2013 Dmytro Shteflyuk <kpumuk@kpumuk.info>
- Refactored init script (run from statsd user, use PID files for daemonizing)

* Tue May 14 2013 Oleksiy Kovyrin <alexey@kovyrin.net>
- Upgraded StatsD to 0.6.0 (latest git master)

* Wed Mar 13 2013 Oleksiy Kovyrin <alexey@kovyrin.net>
- Fixed init script, added missing files

* Wed Mar 13 2013 Oleksiy Kovyrin <alexey@kovyrin.net>
- First rpm release of StatsD 0.5.0
