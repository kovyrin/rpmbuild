%define hadoop_lib_dir /usr/lib/hadoop/lib
%define hive_lib_dir /usr/lib/hive/lib

%define cdh_major_version 5
%define cdh_version       5.4.4
%define hadoop_version    2.6.0-cdh%{cdh_version}
%define hive_version      1.1.0-cdh%{cdh_version}

%define json_serde_version 1.3
%define jar_version %{json_serde_version}
%define ok_version 02
%define git_revision f5d416a36b169458a34fd8032992f0e751f4a154

#----------------------------------------------------------------------------------

Name:           ok-hive-json-serde-cdh%{cdh_version}
Version:        %{json_serde_version}
Release:        %{ok_version}+%{git_revision}
Summary:        Read - Write JSON SerDe for Apache Hive.
Group:          Development
License:        BSD
URL:            https://github.com/rcongiu/Hive-JSON-Serde
Packager:       Oleksiy Kovyrin <alexey@kovyrin.net>
Source0:        master.zip
Patch0:         SerDeSpecAnnotation.patch
BuildArch:      noarch

BuildRequires:  maven
BuildRequires:  ok-java

Requires:       ok-java

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
%patch0 -p1

%build
JAVA_HOME=/usr/java/default \
  /opt/maven/bin/mvn \
    -Pcdh%{cdh_major_version} \
    -Dcdh%{cdh_major_version}.version=%{cdh_version} \
    -Dcdh%{cdh_major_version}.hive.version=%{hive_version} \
    -Dcdh%{cdh_major_version}.hadoop.version=%{hadoop_version} \
    clean package

%install
rm -rf %{buildroot}

# Install java lib to both hive and hadoop lib dirs
install -D -m 644 json-serde/target/json-serde-%{jar_version}-jar-with-dependencies.jar %{buildroot}%{hadoop_lib_dir}/json-serde-%{version}-cdh%{cdh_version}.jar
install -D -m 644 json-serde/target/json-serde-%{jar_version}-jar-with-dependencies.jar %{buildroot}%{hive_lib_dir}/json-serde-%{version}-cdh%{cdh_version}.jar

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.md

%{hive_lib_dir}
%{hadoop_lib_dir}
