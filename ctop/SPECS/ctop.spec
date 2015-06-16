%define ctop_release    4
# do not build debug packages
%define debug_package %{nil}

Name:       ctop
Release:    %{ctop_release}%{?dist}
Version:    1
License:    The MIT License
URL:        https://github.com/hailocab/ctop
Source0:    https://github.com/hailocab/ctop/archive/ctop.tar.gz
Summary:    CTOP ("Top for Cassandra")
Group:      System administration tools

Provides: ctop = %version.%{ctop_release}

Obsoletes: ctop

BuildRequires: golang

%description
CTOP is a tool which allows you to quickly find out what's happening on a machine running Cassandra. It is particularly useful on a cluster with multiple-tenants, multiple-applications, and large numbers of tables. If you suspect that the performance is not good, then you can use this to figure out which table is giving you trouble.

%prep
%setup

%build
# set env vars
export GOPATH=`pwd`
export GOBIN=`pwd`/bin

# patch port
sed -i -e 's/var portNumber = "8081"/var portNumber = "17104"/' main.go

# get dependencies and build
go get
go build

%install
mkdir -p $RPM_BUILD_ROOT/usr/bin
cp ctop-%{version} $RPM_BUILD_ROOT/usr/bin/ctop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(755, root, root) /usr/bin/ctop

%changelog
* Mon Mar 23 2015 Vadzim Tonka <vtonko@swiftype.com> - 1.4
- Initial release.
