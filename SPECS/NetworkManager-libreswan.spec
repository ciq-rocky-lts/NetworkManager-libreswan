%global nm_version        1:1.2.0
%global nma_version       1.2.0

Summary:   NetworkManager VPN plug-in for IPsec VPN
Name:      NetworkManager-libreswan
Version:   1.2.4
Release:   2.1%{?dist}
License:   GPLv2+
URL:       http://www.gnome.org/projects/NetworkManager/
Group:     System Environment/Base
Source0:   https://download.gnome.org/sources/NetworkManager-libreswan/1.2/%{name}-%{version}.tar.xz

Patch0:    0001-translations-rh1383163.patch

Patch1000: 1000-ipsec-conf-escaping-cve-2024-9050.patch

BuildRequires: gtk3-devel
BuildRequires: libnl3-devel
BuildRequires: NetworkManager-devel >= %{nm_version}
BuildRequires: NetworkManager-glib-devel >= %{nm_version}
BuildRequires: NetworkManager-libnm-devel >= %{nm_version}
BuildRequires: libnm-gtk-devel >= %{nma_version}
BuildRequires: libnma-devel >= %{nma_version}
BuildRequires: libsecret-devel
BuildRequires: intltool gettext

Requires: NetworkManager >= %{nm_version}
Requires: dbus
Requires: /usr/sbin/ipsec

Provides: NetworkManager-openswan = %{version}-%{release}
Obsoletes: NetworkManager-openswan < %{version}-%{release}

%global _privatelibs libnm-libreswan-properties[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%description
This package contains software for integrating the libreswan VPN software
with NetworkManager and the GNOME desktop

%package -n NetworkManager-libreswan-gnome
Summary: NetworkManager VPN plugin for libreswan - GNOME files
Group:   System Environment/Base

Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: shared-mime-info

Provides: NetworkManager-openswan-gnome = %{version}-%{release}
Obsoletes: NetworkManager-openswan-gnome < %{version}-%{release}

%description -n NetworkManager-libreswan-gnome
This package contains software for integrating VPN capabilities with
the libreswan server with NetworkManager (GNOME files).

%prep
%setup -q
%patch0 -p1

%patch1000 -p1

%build
%configure \
        --disable-static \
        --enable-more-warnings=yes \
        --with-dist-version=%{version}-%{release}
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la

%find_lang %{name}

%post
update-desktop-database &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :

%files -f %{name}.lang
%{_libdir}/NetworkManager/libnm-vpn-plugin-libreswan.so
%{_sysconfdir}/dbus-1/system.d/nm-libreswan-service.conf
%{_prefix}/lib/NetworkManager/VPN/nm-libreswan-service.name
%{_libexecdir}/nm-libreswan-service
%{_libexecdir}/nm-libreswan-service-helper
%doc AUTHORS ChangeLog NEWS
%license COPYING

%files -n NetworkManager-libreswan-gnome
%{_libexecdir}/nm-libreswan-auth-dialog
%{_libdir}/NetworkManager/libnm-*-properties.so
%{_libdir}/NetworkManager/libnm-vpn-plugin-libreswan-editor.so
%dir %{_datadir}/gnome-vpn-properties/libreswan
%{_datadir}/gnome-vpn-properties/libreswan/nm-libreswan-dialog.ui
%{_sysconfdir}/NetworkManager/VPN/nm-libreswan-service.name
%{_datadir}/appdata/network-manager-libreswan.metainfo.xml


%changelog
* Wed Nov 13 2024 Matt Hink <mhink@ciq.com> - 1.2.4-2.1
- Fix CVE-2024-9050

* Mon May 29 2017 Lubomir Rintel <lrintel@redhat.com> - 1.2.4-2
- po: update Japanese translation (rh #1383163)

* Thu Jun 30 2016 Thomas Haller <thaller@redhat.com> - 1.2.4-1
- Update to 1.2.4 release
- Move base VPN plugin library to base libreswan package
- Don't require nm-connection-editor anymore

* Wed Apr 27 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.2.0-1
- Update to 1.2.0 release

* Wed Mar 30 2016 Lubomir Rintel <lrintel@redhat.com> - 1.2.0-0.1.beta3
- Update to 1.2-beta3:
- Added support for main exchange type (rh #1292912)
- A device libreswan is unable listen on no longer aborts connection (rh #1285367)
- Added import/export support (rh #1129878)
- Replace NetworkManager-openswan (rh #1264552)

* Mon Oct 26 2015 Lubomir Rintel <lrintel@redhat.com> - 1.0.6-3
- Fix the pty hangup patch (rh #1271973)

* Fri Oct 23 2015 Lubomir Rintel <lrintel@redhat.com> - 1.0.6-2
- Fix recovery after failures (rh #1271973)

* Thu Aug 27 2015 Lubomir Rintel <lrintel@redhat.com> - 1.0.6-1
- Update to a newer upstream release (rh #1243057)

* Fri Feb 28 2014 Avesh Agarwal <avagarwa@redhat.com> - 0.9.8.0-5
Resolves: rhbz#1069526
- Rename to NetworkManager-libreswan

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.9.8.0-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.9.8.0-3
- Mass rebuild 2013-12-27

* Thu Dec 12 2013 Avesh Agarwal <avagarwa@redhat.com> - 0.9.8.0-2
- Fixed rhbz#921061
- Fixed rhbz#999353
- Fixed rhbz#1035786
- Fixed rhbz#1014830
- Fixes 1035786 (and its duplicate 1040924)
- Fixed 926225
- Fixed dependency to libreswan.
- Created a new sub package NetworkManager-openswan-gnome
- Various other spec file fixes.
- Additional code changes are as follows:
- Fixed an issue where proper network stack is not loaded unless
  _stackmanager is run before starting pluto daemon service.
- Fixed the termination operation of pluto daemon to comply with
  libreswan changes.
- Fixed various debug messages.
- Fixed initiation of pluto daemon by this plugin to reflect the
  changes in libreaswan.
- Fixed defaults values for more parameters to help the VPN
  connection stay more reliable.
- Rewrote pluto watch API which watches the pluto process for its status.
  Fixed memory leak issues as not all child processes were reaped correctly.
  Also g_spwan_close_pid was not being called after children were reaped.
  Also modified debugs and added more to help with debugging in the future.
- Fixed an issue where nm-openswan service is searching for ipsec binary in
  both /sbin and /usr/sbin leading to same operation twice, as /sbin is just
  symlink to /usr/sbin, so removed /sbin from the search paths.
- Fixed some libreswan related macro changes.
- Fixed netmask issue when sending IP information to the nm openswan
  plugin service.
- Fixed the current code as it does not set the default route field
  NM_VPN_PLUGIN_IP4_CONFIG_NEVER_DEFAULT when sending VPN information
  to nm-openswan plugin. This fix sets the field to TRUE.
- Fixed some issues found by coverity scan.
- Fixed an issue where writing configuration on stdin should not end with
  \n as it gives error. It used to work previously, but not with latest
  NetworkManager versions.
- libreswan related fixes, as some macros have been modified after forking
  to libreswan from openswan.
- openswan/libreswan does not provide tun0 interface, so fixed the code
  where it sends tun0 interface.
- Fix prcoessing of nm-openswan-dialog.ui file and added more error notifications.
- Fixed dead code based on coverity scan.
- Fixed gnomekeyring lib dependencies.
- Fixed Networkmanager and related lib dependencies.
- Fixed gtk label max width issue by setting it to 35.
- NM-openswan was missing support for nm-openswan-auth-dialog.desktop.in.in.
  So added a new nm-openswan-auth-dialog.desktop.in.in, and modified related
  Makefile and configure.ac files.

* Mon Aug 5 2013 Avesh Agarwal <avagarwa@redhat.com> - 0.9.8.0-1
- Rebase to latest upstream version 0.9.8.0
- Fixed several issues with the packaging

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3.995-5.git20120302
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 13 2012 Avesh Agarwal <avagarwa@redhat.com> - 0.9.3.995-4
- Fixed #845599, #865883

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3.995-3.git20120302
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 Avesh Agarwal <avagarwa@redhat.com> - 0.9.3.995-2
- Ported changes from rhel to fedora

* Fri Mar  2 2012 Dan Williams <dcbw@redhat.com> - 0.9.3.995-1
- Update to 0.9.3.995 (0.9.4-beta1)
- ui: add support for external UI mode, eg GNOME Shell

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.9.0-2
- Rebuild for new libpng

* Fri Aug 26 2011 Dan Williams <dcbw@redhat.com> - 0.9.0-1
- Update to 0.9.0
- ui: translation fixes

* Thu Jul 21 2011 Dan Williams <dcbw@redhat.com> - 0.8.999-2.git20110721
- Update to git snapshot
- Fixes for secrets handling and saving

* Tue May 03 2011 Dan Williams <dcbw@redhat.com> - 0.8.999-1
- Update to 0.8.999 (0.9-rc2)
- Port to GTK 3.0 and GtkBuilder
- Fix some issues with secrets storage

* Sun Mar 27 2011 Christopher Aillon <caillon@redhat.com> - 0.8.0-9.20100411git
- Rebuild against NetworkManager 0.9

* Wed Feb 16 2011 Avesh Agarwal <avagarwa@redhat.com> - 0.8.0-8.20100411git
- fixes for compile time errors

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-7.20100411git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 7 2010 Avesh Agarwal <avagarwa@redhat.com> - 0.8.0-6.20100411git
- Modified import and export interfaces to import_from_file and export_to_file, respectively,
  due to changes in NMVpnPluginUiInterface struct in NM (bz 631159). 

* Mon Jul 26 2010 Avesh Agarwal <avagarwa@redhat.com> - 0.8.0-5.20100411git
- Fixed #616910
- Support for reading phase1 and phase2 algorithms through GUI

* Tue Jul 13 2010 Avesh Agarwal <avagarwa@redhat.com> - 0.8.0-4.20100411git
- Modified fix for the bz 607352
- Fix to read connection configuration from stdin
- Fix to read Xauth user password from stdin
- Fix to delete the secret file as soon as read by Openswan

* Thu Jul 8 2010 Avesh Agarwal <avagarwa@redhat.com> - 0.8.0-3.20100411git
- Modified the patch so that it does not pass user password to 
  "ipsec whack" command.   

* Thu Jul 8 2010 Avesh Agarwal <avagarwa@redhat.com> - 0.8.0-2.20100411git
- Modified to initiate VPN connections with openswan whack interface
- Fixed the issue of world readable conf and secret files 
- Cleaned conf and secret files after VPN connection is stopped
- Fixed the issue of storing sensitive information like user 
  password in a file (rhbz# 607352)
- Changed PLUTO_SERVERBANNER to PLUTO_PEER_BANNER due
  to the same change in Openswan
- Modifed GUI to remove unused configuration boxes

* Tue Jun 15 2010 Avesh Agarwal <avagarwa@redhat.com> - 0.8.0-1.20100411git
- Initial build
