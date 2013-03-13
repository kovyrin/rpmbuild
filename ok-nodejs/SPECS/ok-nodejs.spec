%define nodejs_version 0.10.0
%define ok_version 01

Name:          ok-nodejs
Version:       %{nodejs_version}
Release:       %{ok_version}
Summary:       Node's goal is to provide an easy way to build scalable network programs.
Group:         Applications/Internet
License:       Copyright Joyent, Inc. and other Node contributors.
URL:           http://nodejs.org
Source0:       http://nodejs.org/dist/node-v%{version}.tar.gz

BuildRequires: python >= 2.4

%description
Node.js is a server-side JavaScript environment that uses an asynchronous
event-driven model. This allows Node.js to get excellent performance based on
the architectures of many Internet applications.

%prep
%setup -q -n node-v%{version}

%build
./configure --prefix=/usr
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE README.md

/usr/bin/node
/usr/bin/npm

/usr/lib/node_modules
/usr/lib/dtrace/node.d

/usr/share/man/man1/node.1.gz

%changelog
* Wed Mar 13 2013 Oleksiy Kovyrin <alexey@kovyrin.net> 0.10.0-01
- Update from upstream

* Tue Mar 5 2013 Oleksiy Kovyrin <alexey@kovyrin.net> 0.8.21-01
- Update from upstream

* Sat Nov 19 2011 Oleksiy Kovyrin <oleksiy.kovyrin@livingsocial.com> 0.6.2-01
- Update from upstream

* Thu Apr 14 2011 Chris Abernethy <cabernet@chrisabernethy.com> 0.4.6-1
- Initial rpm using upstream v0.4.6
