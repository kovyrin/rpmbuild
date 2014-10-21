# do not repack jar files
%define __os_install_post %{nil}
%define __jar_repack %{nil}

# do not build debug packages
%define debug_package %{nil}

#---------------------------------------------------------------------------------------------------
%define base_install_dir /opt/kestrel

%define kestrel_version 2.4.1
%define scala_version 2.9.2
%define package_revision 01

Name:           ok-kestrel
Version:        %{kestrel_version}
Release:        %{package_revision}
Summary:        Kestrel is a simple, distributed message queue written on the JVM

Group:          Development
Vendor:         Twitter
License:        Apache License, Version 2.0
URL:            http://twitter.github.io/kestrel
Source0:        http://twitter.github.io/kestrel/download/kestrel-%{version}.zip

BuildArch:      noarch

Requires:       ok-java

%description
Kestrel is a simple, distributed message queue written on the JVM, based on Blaine Cook's "starling".
Each server handles a set of reliable, ordered message queues, with no cross communication,
resulting in a cluster of k-ordered ("loosely ordered") queues. Kestrel is fast, small, and reliable.

%prep
%setup -q -n kestrel-%{version}

%build
true

%install
rm -rf %{buildroot}

%{__mkdir} -p %{buildroot}%{base_install_dir}

# Kestrel files
cp -ax kestrel_%{scala_version}-%{version}.jar %{buildroot}%{base_install_dir}/kestrel-%{version}.jar
cp -ax libs %{buildroot}%{base_install_dir}/
cp -ax scripts %{buildroot}%{base_install_dir}/

# Configs
%{__mkdir} -p %{buildroot}%{base_install_dir}/config/examples
cp -ax config/* %{buildroot}%{base_install_dir}/config/examples/

# Logs
%{__mkdir} -p %{buildroot}/var/log/kestrel

# sysconfig and init
#%{__mkdir} -p %{buildroot}%{_sysconfdir}/rc.d/init.d
#%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
#%{__install} -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/kestrel
#%{__install} -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/kestrel

# Run
%{__mkdir} -p %{buildroot}/var/run/kestrel
%{__mkdir} -p %{buildroot}/var/lock/subsys/kestrel

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

%{base_install_dir}

%dir /var/log/kestrel
%dir /var/run/kestrel
%dir /var/lock/subsys/kestrel

%changelog
* Fri Mar 28 2014 Oleksiy Kovyrin <alexey@kovyrin.net> - 2.4.1-01
- Initial package release for 2.4.1
