%define ant_home /opt/ant

%define ant_version 1.9.1
%define ok_version 01

#----------------------------------------------------------------------------------

Name:           ok-ant
Version:        %{ant_version}
Release:        %{ok_version}
Summary:        Apache Ant build tool
Group:          Development
License:        Apache
URL:            http://ant.apache.org/
Vendor:         Apache
Packager:       Oleksiy Kovyrin <alexey@kovyrin.net>
Source0:        apache-ant-%{ant_version}-bin.tar.gz
BuildArch:      noarch

Requires:       ok-java

Provides:       ant
Obsoletes:      ant

%description
Apache Ant is a Java library and command-line tool whose mission is to drive processes
described in build files as targets and extension points dependent upon each other.

%prep
%setup -q -n apache-ant-%{version}

%build
echo "Build not needed..."

%install
%{__mkdir_p} %{buildroot}%{ant_home}
cp -ax * %{buildroot}%{ant_home}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc INSTALL KEYS LICENSE NOTICE WHATSNEW

%{ant_home}
