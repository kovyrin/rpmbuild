%define mysql_connector_version 5.1.35
%define ok_version 01
#----------------------------------------------------------------------------------

Name:           ok-mysql-connector-java
Version:        %{mysql_connector_version}
Release:        %{ok_version}
Summary:        MySQL Connector/J is the official JDBC driver for MySQL
Group:          Development
License:        GPLv2
URL:            http://www.mysql.com/downloads/connector/j/5.1.html
Vendor:         Oracle
Packager:       Oleksiy Kovyrin <alexey@kovyrin.net>
Source0:        mysql-connector-java-%{mysql_connector_version}.tar.gz
BuildArch:      noarch

Requires:       ok-java
Provides:       mysql-connector-java
Obsoletes:      mysql-connector-java

%description
MySQL Connector/J is the official JDBC driver for MySQL.

%prep
%setup -q -n mysql-connector-java-%{mysql_connector_version}

%build
echo "Build not needed..."

%install
# Install js files
%{__mkdir_p} %{buildroot}/usr/share/java

%{__install} -Dp -m0644 mysql-connector-java-%{mysql_connector_version}-bin.jar %{buildroot}/usr/share/java/mysql-connector-java.jar

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES COPYING README README.txt
%doc docs

/usr/share/java
