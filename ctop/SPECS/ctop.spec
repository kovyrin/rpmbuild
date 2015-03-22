%define ctop_release    4

Name:       ctop
Version:    1
Release:    %{ctop_release}%{?dist}
License:    The MIT License
URL:        https://github.com/hailocab/ctop
Source0:    https://github.com/hailocab/ctop/archive/1.4.tar.gz
Summary:    CTOP ("Top for Cassandra")
Group:      System administration tools

Provides: ctop = 1.4

Obsoletes: ctop

BuildRequires: golang
BuildRequires: ok-mx4j

Requires: ok-mx4j

%description
CTOP is a tool which allows you to quickly find out what's happening on a machine running Cassandra. It is particularly useful on a cluster with multiple-tenants, multiple-applications, and large numbers of tables. If you suspect that the performance is not good, then you can use this to figure out which table is giving you trouble.

%prep
%setup -n ctop
#autoconf

%build
GOPATH=`pwd` GOBIN=`pwd`/bin go build

%install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
ctop
%{_includedir}
%{_datadir}
%{_libdir}

%changelog
* Fri Nov 22 2013 Oleksiy Kovyrin <alexey@kovyrin.net> - 2.0.0-p353-1
- Updated ruby to 2.0.0-p353. First 2.0 build.

* Sat Apr 27 2013 Oleksiy Kovyrin <alexey@kovyrin.net> - 1.9.3-p385-1
- Updated ruby and the patches to 1.9.3-p385.

* Fri Feb 8 2013 Oleksiy Kovyrin <alexey@kovyrin.net> - 1.9.3-p327-1
- Initial release for Ruby 1.9.3-p327 with falcon-gc patch.
