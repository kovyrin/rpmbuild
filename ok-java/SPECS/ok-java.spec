# These should match oracle java version/release
%define java_version 1.7.0_15
%define java_release fcs
%define java_epoch 2000

# Our specific package version
%define package_revision 01

#---------------------------------------------------------------------------------
Name:           ok-java
BuildArch:      noarch
License:        New BSD License
Group:          Development
Summary:        An umbrella package for Oracle java packages with correct provides and ldconfig
Version:        %{java_version}
Release:        %{java_release}+%{package_revision}
Source0:        java.conf

# Depend on oracle jdk package
Requires:       jdk = %{java_epoch}:%{java_version}-%{java_release}

# Missing provides from jdk
Provides:       libjvm.so()(64bit)

# Provide java so that openjdk does not get installed as a depenency for ant and other java pkgs
Provides:       java
Provides:       java-devel

# Remove openjdk crap
Obsoletes:      libgcj
Obsoletes:      java-1.6.0-openjdk
Obsoletes:      java-1.7.0-openjdk

%description
Use this package to install and configure Oracle java.

#---------------------------------------------------------------------------------
%install
rm -rf %{buildroot}

install -D -m 755 $RPM_SOURCE_DIR/java.conf %{buildroot}/etc/ld.so.conf.d/java.conf

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%files
%defattr(-,root,root)
/etc/ld.so.conf.d/java.conf
