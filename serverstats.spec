#include	/usr/lib/rpm/macros.perl
Summary:	Simple tool for creating graphs using rrdtool
Name:		serverstats
Version:	0.8.2
Release:	0.1
License:	GPL/LGPL ?
Group:		Applications/System
Source0:	http://download.berlios.de/serverstats/%{name}-%{version}.tar.bz2
# Source0-md5:	e17ec7aef1029c06aeaf53becf15dd67
Source1:	%{name}.cron
URL:		http://serverstats.berlios.de/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php-cli
Requires:	rrdtool >= 1.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	/var/lib/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_webappdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Serverstats is a simple tool for creating graphs using rrdtool.

Serverstats does not have any features to manage the created rrd-files,
if you change anything you have to delete and recreate the files. Perhaps
you can avoid this using third-party-tools. Also there is no frontend
managing your graphs and sources. You will have to use your $EDITOR.
Serverstats is build to be configured once and then run and run and ...

I created this because Cacti was much to overloaded and I disliked that
it depends on a database.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/cron.d,%{_appdir},%{_webappdir},%{_pkglibdir}/{cache,graph,rrd}}

install *.php *.css $RPM_BUILD_ROOT%{_appdir}
cp -R sources lang includes $RPM_BUILD_ROOT%{_appdir}

# configs:
install config.sample/*.php $RPM_BUILD_ROOT%{_webappdir}
ln -s %{_webappdir} $RPM_BUILD_ROOT%{_appdir}/config

ln -s %{_pkglibdir}/cache $RPM_BUILD_ROOT%{_appdir}/cache
ln -s %{_pkglibdir}/graph $RPM_BUILD_ROOT%{_appdir}/graph
ln -s %{_pkglibdir}/rrd $RPM_BUILD_ROOT%{_appdir}/rrd

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
%dir %attr(750,root,http) %{_webapps}/%{_webapp}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/*.php
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/apache.conf
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/httpd.conf
%dir %{_appdir}
%{_appdir}/*.css
%{_appdir}/detail.php
%{_appdir}/graph.php
%{_appdir}/index.php
%{_appdir}/init.php
%attr(750,stats,stats) %{_appdir}/update.php
%{_appdir}/includes
%{_appdir}/lang
%{_appdir}/sources
%dir %{_pkglibdir}
%dir %attr(750,stats,http) %{_pkglibdir}/cache
%dir %attr(750,http,http) %{_pkglibdir}/graph
%dir %attr(750,stats,http) %{_pkglibdir}/rrd
# symlinks:
%{_appdir}/cache
%{_appdir}/config
%{_appdir}/graph
%{_appdir}/rrd
