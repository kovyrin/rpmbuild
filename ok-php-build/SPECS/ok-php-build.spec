%define phpbuild_version 0.0.1
%define phpbuild_revision 3a79fa10a747d83c7073ba961f40272158b0fc98
%define package_revision 01

#---------------------------------------------------------------------------------
Name:           ok-php-build
License:        GPL v2
Group:          Development
Summary:        Builds PHP so that multiple versions can be used in parallel.
Version:        %{phpbuild_version}
Release:        %{package_revision}+%{phpbuild_revision}
Source0:        php-build-%{phpbuild_revision}.tar.gz

BuildRequires:  php
BuildRequires:  php-devel
BuildRequires:  php-cli
BuildRequires:  git
BuildRequires:  curl

Requires:       php php-cli php-devel
Requires:       libmcrypt libmcrypt-devel
Requires:       libtidy libtidy-devel
Requires:       re2c

%description
php-build builds multiple PHP versions from source, and this fully automatic.

#---------------------------------------------------------------------------------
%files
%defattr(-,root,root)
/usr

#---------------------------------------------------------------------------------
%prep
%setup -n php-build

#---------------------------------------------------------------------------------
%install
rm -rf %{buildroot}

# Install it
PREFIX=%{buildroot}/usr ./install.sh

#install -D -m 755 ./phpbuild %{buildroot}%{phpbuild_home}/bin/phpbuild-%{phpbuild_version}
#install -D -m 755 $RPM_SOURCE_DIR/phpbuild.init %{buildroot}/etc/rc.d/init.d/phpbuild
#install -D -m 755 $RPM_SOURCE_DIR/generate-phpbuild-config %{buildroot}%{phpbuild_home}/conf/generate-phpbuild-config

#---------------------------------------------------------------------------------
%clean
rm -rf %{buildroot}
