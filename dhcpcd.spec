Summary:	DHCP Client Daemon
Name:		dhcpcd
Version:	6.9.0
Release:	1
License:	BSD
Group:		Networking/Daemons
#Source0Download: http://developer.berlios.de/project/filelist.php?group_id=4229
Source0:	http://roy.marples.name/downloads/dhcpcd/%{name}-%{version}.tar.bz2
# Source0-md5:	374fcac1877078a2fc0ef8cd1617a869
Source1:	%{name}@.service
Source2:	%{name}.service
Source3:	%{name}-tmpfiles.conf
URL:		http://roy.marples.name/dhcpcd
BuildRequires:	udev-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
dhcpcd is an implementation of the DHCP client specified in
draft-ietf-dhc-dhcp-09 (when -r option is not specified) and RFC1541
(when -r option is specified).

%prep
%setup -q

%build
%configure \
	--dbdir=%{_sharedstatedir}/dhcpcd	\
	--rundir=/run
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}@.service
install -D %{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service
install -D %{SOURCE3} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

touch $RPM_BUILD_ROOT%{_sysconfdir}/dhcpcd.{enter-hook,exit-hook}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/dhcpcd

%dir %{_libexecdir}
%dir %{_libexecdir}/dev
%dir %{_libexecdir}/dhcpcd-hooks
%dir %{_sharedstatedir}/dhcpcd

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*-hook
%attr(755,root,root) %{_libexecdir}/dhcpcd-hooks/*
%attr(755,root,root) %{_libexecdir}/dhcpcd-run-hooks
%attr(755,root,root) %{_libexecdir}/dev/*.so
%{systemdtmpfilesdir}/%{name}.conf
%{systemdunitdir}/%{name}@.service
%{systemdunitdir}/%{name}.service
%{_mandir}/man?/dhcpcd*.*

