%define maven_home /opt/maven

%define maven_version 3.0.5
%define ok_version 01

#----------------------------------------------------------------------------------

Name:           ok-maven
Version:        %{maven_version}
Release:        %{ok_version}
Summary:        Apache maven build tool
Group:          Development
License:        Apache
URL:            http://maven.apache.org/
Vendor:         Apache
Packager:       Oleksiy Kovyrin <alexey@kovyrin.net>
Source0:        apache-maven-%{maven_version}-bin.tar.gz
BuildArch:      noarch

Requires:       ok-java

Provides:       maven
Obsoletes:      maven

%description
Apache Maven is a software project management and comprehension tool. Based on the
concept of a project object model (POM), Maven can manage a project's build, reporting
and documentation from a central piece of information.

%prep
%setup -q -n apache-maven-%{version}

%build
echo "Build not needed..."

%install
%{__mkdir_p} %{buildroot}%{maven_home}
cp -ax * %{buildroot}%{maven_home}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.txt LICENSE.txt NOTICE.txt

%{maven_home}
