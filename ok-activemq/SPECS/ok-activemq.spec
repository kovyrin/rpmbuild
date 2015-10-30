%define debug_package %{nil}
%define __jar_repack %{nil}

%define activemq_home /opt/activemq

%define activemq_version 5.10.0
%define ok_version 02

#----------------------------------------------------------------------------------

Name:           ok-activemq
Version:        %{activemq_version}
Release:        %{ok_version}
Summary:        ActiveMQ Server
Group:          Development
License:        Apache
URL:            http://activemq.apache.org/
Vendor:         Apache
Packager:       Oleksiy Kovyrin <alexey@kovyrin.net>
BuildArch:      x86_64

Source0:        apache-activemq-%{activemq_version}-bin.tar.gz
Patch0:         remove-credentials-properties.patch

Requires:       ok-java

%description
Apache ActiveMQ is the most popular and powerful open source
messaging and Integration Patterns server.

%prep
%setup -q -n apache-activemq-%{activemq_version}
%patch0 -p1

%build
echo "Build not needed..."

%install
%{__mkdir_p} %{buildroot}%{activemq_home}
cp -ax * %{buildroot}%{activemq_home}/
rm -rf %{buildroot}%{activemq_home}/{examples,webapps-demo,docs}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE README.txt docs examples

%{activemq_home}
