%define hadoop_lib_dir /usr/lib/hadoop/lib
%define hive_lib_dir /usr/lib/hive/lib

%define hadoop_version 2.0.0+1518
%define hive_version 0.10.0+214

%define rank_udf_version 1.0.0
%define ok_version 02
%define git_revision 827fffc4c74a2eaa56f6937073ce38dc1b186bb7

#----------------------------------------------------------------------------------

Name:           ok-hive-rank-udf
Version:        %{rank_udf_version}
Release:        %{ok_version}+%{git_revision}
Summary:        The Rank Generic UDF in Hive
Group:          Development
License:        GPLv3
URL:            https://github.com/kovyrin/hive-rank
Packager:       Oleksiy Kovyrin <alexey@kovyrin.net>
Source0:        master.zip
BuildArch:      noarch

BuildRequires:  maven
BuildRequires:  ok-java
BuildRequires:  hadoop = %{hadoop_version}

Requires:       ok-java
Requires:       hadoop = %{hadoop_version}
Requires:       hive = %{hive_version}

%description
The Rank Generic UDF in Hive

%prep
%setup -q -n hive-rank-master

%build
JAVA_HOME=/usr/java/default /opt/maven/bin/mvn package -Dmaven.test.skip=true

%install
rm -rf %{buildroot}

# Install java lib to both hive and hadoop lib dirs
install -D -m 644 target/hive-rank-%{version}-SNAPSHOT.jar %{buildroot}%{hadoop_lib_dir}/hive-rank-%{version}.jar
install -D -m 644 target/hive-rank-%{version}-SNAPSHOT.jar %{buildroot}%{hive_lib_dir}/hive-rank-%{version}.jar

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc NOTICE.txt README.md

%{hive_lib_dir}
%{hadoop_lib_dir}
