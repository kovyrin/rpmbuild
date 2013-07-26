%define hadoop_lib_dir /usr/lib/hadoop/lib
%define hive_lib_dir /usr/lib/hive/lib

%define hadoop_version 2.0.0+1357
%define hive_version 0.10.0+121

%define json_serde_version 1.1.6
%define ok_version 03
%define git_revision e338a179f429f37dbf98695c2952183333a142cb

#----------------------------------------------------------------------------------

Name:           ok-hive-json-serde
Version:        %{json_serde_version}
Release:        %{ok_version}+%{git_revision}
Summary:        Read - Write JSON SerDe for Apache Hive.
Group:          Development
License:        GPLv3
URL:            https://github.com/kovyrin/Hive-JSON-Serde
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
JsonSerde - a read/write SerDe for JSON Data
AUTHOR: Roberto Congiu <rcongiu@yahoo.com>

Serialization/Deserialization module for Apache Hadoop Hive

This module allows hive to read and write in JSON format (see http://json.org for more info).

Features:
* Read data stored in JSON format
* Convert data to JSON format when INSERT INTO table
* arrays and maps are supported
* nested data structures are also supported

%prep
%setup -q -n Hive-JSON-Serde-master

%build
JAVA_HOME=/usr/java/default /opt/maven/bin/mvn package

%install
rm -rf %{buildroot}

# Install java lib to both hive and hadoop lib dirs
install -D -m 644 target/json-serde-%{version}.jar %{buildroot}%{hadoop_lib_dir}/json-serde-%{version}.jar
install -D -m 644 target/json-serde-%{version}.jar %{buildroot}%{hive_lib_dir}/json-serde-%{version}.jar

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.txt

%{hive_lib_dir}
%{hadoop_lib_dir}
