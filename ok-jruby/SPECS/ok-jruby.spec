# do not repack jar files
%define __arch_install_post %{nil}
%define __os_install_post %{nil}
%define __jar_repack %{nil}

# do not build debug packages
%define debug_package %{nil}

#---------------------------------------------------------------------------------------------------
Name: ok-jruby
Version: 1.7.19
Release: 3%{?dist}
License: EPL/GPL/LGPL
Group: Development/Languages
URL: http://jruby.org
Summary: A Java implementation of the Ruby language
Source0:  http://jruby.org.s3.amazonaws.com/downloads/%{version}/jruby-bin-%{version}.tar.gz
Requires: ok-java

Provides: jruby
Obsoletes: jruby

%description
A Java implementation of the Ruby language

%prep
%setup -q -n jruby-%{version}

%build
echo "No building required..."

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/opt
cp -r $RPM_BUILD_DIR/jruby-%{version} $RPM_BUILD_ROOT/opt/jruby

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/jruby
cp -r $RPM_BUILD_DIR/jruby-%{version}/docs/* $RPM_BUILD_ROOT/%{_docdir}/jruby

mkdir -p $RPM_BUILD_ROOT/usr/local/bin
ln -sf /opt/jruby/bin/jruby   $RPM_BUILD_ROOT/usr/local/bin/jruby
ln -sf /opt/jruby/bin/jgem    $RPM_BUILD_ROOT/usr/local/bin/jgem
ln -sf /opt/jruby/bin/jirb    $RPM_BUILD_ROOT/usr/local/bin/jirb
ln -sf /opt/jruby/bin/jrubyc  $RPM_BUILD_ROOT/usr/local/bin/jrubyc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc %{_docdir}/jruby
/opt/jruby

/usr/local/bin/jruby
/usr/local/bin/jgem
/usr/local/bin/jirb
/usr/local/bin/jrubyc

%changelog
* Sun Feb 8 2015 Oleksiy Kovyrin <alexey@kovyrin.net> 1.7.19-3
- Upstream upgrade
- Do not fuck with symlinks from post-scripts
* Wed Jan 8 2014 Simon Thulbourn <simon.thulbourn@bbc.co.uk> 1.7.9-1
- Initial release
