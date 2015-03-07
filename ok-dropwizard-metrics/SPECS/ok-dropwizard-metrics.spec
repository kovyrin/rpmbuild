%define metrics_home /opt/dropwizard-metrics

%define metrics_version 3.1.0
%define ok_version 01

#----------------------------------------------------------------------------------

Name:           ok-dropwizard-metrics
Version:        %{metrics_version}
Release:        %{ok_version}
Summary:        Java library which gives you unparalleled insight into what your code does in production.
Group:          Development
License:        Apache
URL:            http://metrics.dropwizard.io/
Packager:       Oleksiy Kovyrin <alexey@kovyrin.net>
Source0:        https://github.com/dropwizard/metrics/archive/v%{metrics_version}.tar.gz
BuildArch:      noarch

BuildRequires:  maven
BuildRequires:  ok-java

Requires:       ok-java

%description
Metrics provides a powerful toolkit of ways to measure the behavior of
critical components in your production environment.

With modules for common libraries like Jetty, Logback, Log4j, Apache HttpClient,
Ehcache, JDBI, Jersey and reporting backends like Ganglia and Graphite, Metrics
provides you with full-stack visibility.

%prep
%setup -q -n metrics-%{metrics_version}

%build
JAVA_HOME=/usr/java/default /opt/maven/bin/mvn package -Dmaven.test.skip=true

%install
rm -rf %{buildroot}

# Collect all jars and shove them into the home directory
for jar in `find . -type f -name 'metrics-*-%{metrics_version}.jar'`; do
  jar_name=`basename $jar`
  no_version_jar_name=`echo $jar_name | sed 's/-%{metrics_version}//'`

  install -D -m 644 $jar %{buildroot}%{metrics_home}/$jar_name
  ln -s $jar_name %{buildroot}%{metrics_home}/$no_version_jar_name
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE README.md

%{metrics_home}
