%define mx4j_home /opt/mx4j

%define mx4j_version 3.0.2
%define ok_version 01

#----------------------------------------------------------------------------------

Name:           ok-mx4j
Version:        %{mx4j_version}
Release:        %{ok_version}
Summary:        Open Source implementation of the Java Management Extensions technology
Group:          Development
License:        Apache
URL:            http://mx4j.apache.org/
Vendor:         Apache
Packager:       Oleksiy Kovyrin <alexey@kovyrin.net>
Source0:        mx4j-%{mx4j_version}.zip
BuildArch:      noarch

Requires:       ok-java

%description
MX4J is an Open Source implementation of the Java Management Extensions technology, 
for both JSR 3 (JMX) and JSR 160 (JMX Remote API).

%prep
%setup -q -n mx4j-%{version}

%build
echo "Build not needed..."

%install
%{__mkdir_p} %{buildroot}%{mx4j_home}
cp -ax lib/* %{buildroot}%{mx4j_home}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc docs examples Apache-LICENSE.txt  BUILD-HOWTO.txt  Jetty-LICENSE.txt  Jython-LICENSE.txt  LICENSE.txt  README.txt  RELEASE-NOTES-%{mx4j_version}.txt

%{mx4j_home}
