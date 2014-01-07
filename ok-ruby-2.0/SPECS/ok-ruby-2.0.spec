%define ruby_version  2.0.0
%define ruby_patch    p353
%define ok_release    02

Name:       ok-ruby-2.0
Version:    %{ruby_version}%{ruby_patch}
Release:    %{ok_release}%{?dist}
License:    Ruby License/GPL - see COPYING
URL:        http://www.ruby-lang.org/
Source0:    ftp://ftp.ruby-lang.org/pub/ruby/2.0/ruby-%{ruby_version}-%{ruby_patch}.tar.gz
Summary:    An interpreter of object-oriented scripting language
Group:      Development/Languages

#BuildRoot:  BUILDROOT
#%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: ruby(abi) = 2.0
Provides: ruby(abi) = 1.9
Provides: ruby-irb
Provides: ruby-rdoc
Provides: ruby-libs
Provides: ruby-devel
Provides: rubygems

Obsoletes: ok-ruby-1.9
Obsoletes: ruby
Obsoletes: ruby-libs
Obsoletes: ruby-irb
Obsoletes: ruby-rdoc
Obsoletes: ruby-devel
Obsoletes: rubygems

BuildRequires: readline readline-devel ncurses ncurses-devel
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
autoconf

%build
export CFLAGS="$RPM_OPT_FLAGS -Wall -fno-strict-aliasing -march=core2 -mtune=generic -O3 -pipe"

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
* Fri Nov 22 2013 Oleksiy Kovyrin <alexey@kovyrin.net> - 2.0.0-p353-1
- Updated ruby to 2.0.0-p353. First 2.0 build.

* Sat Apr 27 2013 Oleksiy Kovyrin <alexey@kovyrin.net> - 1.9.3-p385-1
- Updated ruby and the patches to 1.9.3-p385.

* Fri Feb 8 2013 Oleksiy Kovyrin <alexey@kovyrin.net> - 1.9.3-p327-1
- Initial release for Ruby 1.9.3-p327 with falcon-gc patch.
