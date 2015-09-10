Name:           go-srpm-macros
Version:        2
Release:        2%{?dist}
Summary:        RPM macros for building Golang packages for various architectures
Group:          Development/Libraries
License:        GPLv3+
Source0:        macros.go-srpm
BuildArch:      noarch
# for install command
BuildRequires:  coreutils

%description
The package provides macros for building projects in Go
on various architectures.

%prep
# nothing to prep, just for hooks

%build
# nothing to build, just for hooks

%install
install -m 644 -D "%{SOURCE0}" \
    '%{buildroot}%{_rpmconfigdir}/macros.d/macros.go-srpm'

%files
%{_rpmconfigdir}/macros.d/macros.go-srpm

%changelog
* Sat Aug 29 2015 jchaloup <jchaloup@redhat.com> - 2-2
- Add -ldflags $LDFLAGS to go build/test macro

* Sun Aug 23 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2-1
- aarch64 now has golang

* Tue Jul 07 2015 jchaloup <jchaloup@redhat.com> - 1-1
- Initial commit
  resolves: #1241156
