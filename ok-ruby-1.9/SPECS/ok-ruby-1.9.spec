%define ruby_version  1.9.3
%define ruby_patch    p327

Name:       ok-ruby-1.9
Version:    %{ruby_version}%{ruby_patch}
Release:    01%{?dist}
License:    Ruby License/GPL - see COPYING
URL:        http://www.ruby-lang.org/
Source0:    ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-%{ruby_version}-%{ruby_patch}.tar.gz
Summary:    An interpreter of object-oriented scripting language
Group:      Development/Languages

Patch0:     falcon.diff
Patch1:     falcon-gc.diff

#BuildRoot:  BUILDROOT
#%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: ruby(abi) = 1.9
Provides: ruby-irb
Provides: ruby-rdoc
Provides: ruby-libs
Provides: ruby-devel
Provides: rubygems

Obsoletes: ruby
Obsoletes: ruby-libs
Obsoletes: ruby-irb
Obsoletes: ruby-rdoc
Obsoletes: ruby-devel
Obsoletes: rubygems

BuildRequires: readline  readline-devel ncurses ncurses-devel
BuildRequires: gdbm gdbm-devel glibc-devel tcl-devel gcc unzip openssl-devel
BuildRequires: db4-devel byacc make libffi-devel
BuildRequires: libyaml libyaml-devel

Requires: libyaml openssl

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.

%prep
%setup -n ruby-%{ruby_version}-%{ruby_patch}
%patch1 -p1
autoconf

%build
export CFLAGS="$RPM_OPT_FLAGS -Wall -fno-strict-aliasing -march=core2 -mtune=generic -O2 -pipe"

%configure \
  --enable-shared \
  --disable-rpath \
  --includedir=%{_includedir}/ruby \
  --libdir=%{_libdir}

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_bindir}
%{_includedir}
%{_datadir}
%{_libdir}

%changelog
* Fri Feb 8 2013 Oleksiy Kovyrin <alexey@kovyrin.net> - 1.9.3-p327-1
- Initial release for Ruby 1.9.3-p327 with falcon-gc patch.
