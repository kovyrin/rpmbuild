%define google_auth_version github
%define package_revision 01

Name:           ok-google-authenticator
Version:        %{google_auth_version}
Release:        %{package_revision}%{?dist}
Summary:        One-time passcode support using open standards
Group:          Security
License:        ASL 2.0
URL:            http://code.google.com/p/google-authenticator/
Source0:        libpam-google-authenticator-%{version}-source.tar.bz2

Requires:       pam
Requires:       qrencode

BuildRequires:  pam-devel
BuildRequires:  qrencode-devel

Provides:       google-authenticator
Obsoletes:      google-authenticator

%description
The Google Authenticator package contains a pluggable authentication
module (PAM) which allows login using one-time passcodes conforming to
the open standards developed by the Initiative for Open Authentication
(OATH) (which is unrelated to OAuth).

Passcode generators are available (separately) for several mobile
platforms.

These implementations support the HMAC-Based One-time Password (HOTP)
algorithm specified in RFC 4226 and the Time-based One-time Password
(TOTP) algorithm currently in draft.

%prep
%setup -q -n libpam-google-authenticator-github

%build
make CFLAGS="${CFLAGS:-%optflags}" LDFLAGS=-ldl %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_lib}/security
install -m0755 pam_google_authenticator.so $RPM_BUILD_ROOT/%{_lib}/security/pam_google_authenticator.so

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
install -m0755 google-authenticator $RPM_BUILD_ROOT/%{_bindir}/google-authenticator

%files
/%{_lib}/security/*
%{_bindir}/google-authenticator

%doc FILEFORMAT README totp.html

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun May 12 2013 Oleksiy Kovyrin <alexey@kovyrin.net> - 0.1-01
- Initial release
