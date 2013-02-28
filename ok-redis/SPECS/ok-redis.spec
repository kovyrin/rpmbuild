%define redis_home /opt/redis
%define redis_version 2.6.10
%define redis_revision 01

#---------------------------------------------------------------------------------
Name:           ok-redis
License:        New BSD License
Group:          Development
Summary:        A persistent key-value database with built-in net interface written in ANSI-C for Posix systems
Version:        %{redis_version}
Release:        %{redis_revision}
URL:            http://code.google.com/p/redis/
Source0:        redis-%{version}.tar.gz
Source1:        redis.init

BuildRequires:  gcc >= 3.4.6
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  zlib-devel

%description
Redis is an advanced key-value store. It is similar to memcached but the dataset is not volatile,
and values can be strings, exactly like in memcached, but also lists, sets, and ordered sets.
All this data types can be manipulated with atomic operations to push/pop elements, add/remove
elements, perform server side union, intersection, difference between sets, and so forth.
Redis supports different kind of sorting abilities.

#---------------------------------------------------------------------------------
%prep
%setup -n redis-%{version}

%build
make %{?_smp_mflags} PREFIX=%{redis_home}

%install
rm -rf %{buildroot}

for i in benchmark check-aof check-dump cli server; do
    install -D -m 755 $RPM_BUILD_DIR/redis-%{redis_version}/src/redis-$i %{buildroot}%{redis_home}/bin/redis-$i
done

install -D -m 644 $RPM_BUILD_DIR/redis-%{redis_version}/redis.conf %{buildroot}%{redis_home}/conf/redis.conf
install -d -m 0755 %{buildroot}%{redis_home}/var

install -D -m 755 $RPM_SOURCE_DIR/redis.init %{buildroot}/etc/rc.d/init.d/redis

sed -i -e "s/daemonize no/daemonize yes/g" %{buildroot}%{redis_home}/conf/redis.conf
sed -i -e "s/\/var\/run/\/opt\/redis\/var/g" %{buildroot}%{redis_home}/conf/redis.conf
sed -i -e "s/logfile stdout/logfile \/opt\/redis\/var\/redis.log/g" %{buildroot}%{redis_home}/conf/redis.conf
sed -i -e "s/dir \./dir \/opt\/redis\/var/g" %{buildroot}%{redis_home}/conf/redis.conf

%clean
rm -rf %{buildroot}

%pre
/usr/sbin/groupadd -f redis
getent passwd redis || /usr/sbin/useradd -c "Redis Server" -s /sbin/nologin -g redis -r -d %{redis_home} redis || :

%files
%defattr(-,redis,redis)
%{redis_home}

%defattr(-,root,root)
/etc/rc.d/init.d/redis
