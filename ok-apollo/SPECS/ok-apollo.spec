%define apollo_home /opt/apollo

%define apollo_version 1.6
%define ok_version 01

#----------------------------------------------------------------------------------

Name:           ok-apollo
Version:        %{apollo_version}
Release:        %{ok_version}
Summary:        ActiveMQ Apollo Server
Group:          Development
License:        Apache
URL:            http://activemq.apache.org/apollo
Vendor:         Apache
Packager:       Oleksiy Kovyrin <alexey@kovyrin.net>
Source0:        apache-apollo-%{apollo_version}-unix-distro.tar.gz
BuildArch:      noarch

Requires:       ok-java

%description
ActiveMQ Apollo is a faster, more reliable, easier to maintain 
messaging broker built from the foundations of the original ActiveMQ. 

%prep
%setup -q -n apache-apollo-%{apollo_version}

%build
echo "Build not needed..."

%install
%{__mkdir_p} %{buildroot}%{apollo_home}
cp -ax * %{buildroot}%{apollo_home}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE readme.html docs

%{apollo_home}
