%define hadoop_lib_dir /usr/lib/hadoop/lib
%define hadoop_version 2.0.0+1357

%define hadoop_lzo_version 0.4.18
%define ok_version 01
%define git_revision c774424f055148c8e19330adcd53515c27e86d40

#----------------------------------------------------------------------------------

Name:           ok-hadoop-lzo
Version:        %{hadoop_lzo_version}
Release:        %{ok_version}+%{git_revision}%{?dist}
Summary:        Patched, refactored version of code.google.com/hadoop-gpl-compression for hadoop 0.20
Group:          Development
License:        GPLv3
URL:            https://github.com/cloudera/hadoop-lzo
Vendor:         Cloudera
Packager:       Oleksiy Kovyrin <alexey@kovyrin.net>
Source0:        master.zip

BuildRequires:  ant
BuildRequires:  gcc
BuildRequires:  lzo-devel
BuildRequires:  ok-java
BuildRequires:  hadoop = %{hadoop_version}

Requires:       lzo
Requires:       ok-java
Requires:       hadoop = %{hadoop_version}

%description
Apache hadoop_lzo is a Java library and command-line tool whose mission is to drive processes
described in build files as targets and extension points dependent upon each other.

%prep
%setup -q -n hadoop-lzo-master

%build
JAVA_HOME=/usr/java/default /opt/ant/bin/ant clean compile-native test jar

%install
rm -rf %{buildroot}

# Install java lib
install -D -m 644 build/hadoop-lzo-%{version}-SNAPSHOT.jar %{buildroot}%{hadoop_lib_dir}/hadoop-lzo-%{version}-SNAPSHOT.jar

# Create native libs dir
install -d -m 0755 %{buildroot}%{hadoop_lib_dir}/native

# Install native libs
cp -ax build/native/Linux-amd64-64/lib/* %{buildroot}%{hadoop_lib_dir}/native/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README.md

%{hadoop_lib_dir}
