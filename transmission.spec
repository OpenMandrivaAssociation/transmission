%bcond_without gtk

Summary:	Simple Bittorrent client
Name:		transmission
Version:	4.0.0
Release:	0.beta2.1
License:	MIT and GPLv2
Group:		Networking/File transfer
Url:		http://www.transmissionbt.com/
Source0:	https://github.com/transmission/transmission-releases/raw/master/transmission-%{version}-beta.2.tar.gz
#Source1:	https://src.fedoraproject.org/rpms/transmission/raw/master/f/transmission-symbolic.svg
Source1:	https://github.com/transmission/libutp/archive/libutp-bf695bdfb047cdca9710ea9cffc4018669cf9548.tar.gz
Source2:	https://github.com/transmission/libb64/archive/libb64-91a38519cb18d3869b4f1c99b0a80726547054af.tar.gz
#Patch0:		transmission-3.00-no-Llib.patch

BuildRequires:	bzip2
BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	intltool
#BuildRequires:	gtest-source
BuildRequires:	miniupnpc-devel
BuildRequires:	libnatpmp-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libdeflate)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	systemd-rpm-macros

# Qt
BuildRequires:	qt6-qttools-linguist
BuildRequires:	cmake(Qt6Linguist)
BuildRequires:	qt6-cmake
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:	cmake(Qt6OpenGL)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Network)
BuildRequires:  cmake(Qt6Xml)
BuildRequires:	qmake5
BuildRequires:	qt5-macros

# GTK
BuildRequires:	pkgconfig(gtk4)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(libcanberra-gtk)
BuildRequires:	pkgconfig(appindicator3-0.1)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(gtkmm-4.0)
BuildRequires:	pkgconfig(glibmm-2.68)

%description
Transmission is a free, lightweight BitTorrent client. It features a 
simple, intuitive interface on top of an efficient back-end.

%package common
Summary:	Common files for Transmission Bittorrent client
Group:		Networking/File transfer
Conflicts:	transmission < 1.74

%description common
Transmission is a free, lightweight BitTorrent client. This package
contains the common files used by the different front-ends.

%package cli
Summary:	Command line interface for Transmission BitTorrent client
Group:		Networking/File transfer
Requires:	%{name}-common = %{version}
Conflicts:	transmission < 1.74

%description cli
Transmission is a free, lightweight BitTorrent client. This package
contains the command line interface front-end.

%if %with gtk
%package gtk
Summary:	GTK Interface for Transmission BitTorrent client
Group:		Networking/File transfer

Requires:	%{name}-common = %{version}
Provides:	%{name} = %{version}-%{release}
Provides:	%{name}-gui = %{version}-%{release}
Obsoletes:	transmission < 1.74-1
# Old, unmaintained clients that used old wx: transmission is as good
# an upgrade path as any - AdamW 2008/12
Obsoletes:	BitTornado <= 0:0.3.18-4
Obsoletes:	bittorrent-gui <= 5.2.2-3

%description gtk
Transmission is a free, lightweight BitTorrent client. It features a
simple, intuitive interface on top of an efficient back-end.

This package provides the GTK Interface.
%endif

%package qt
Summary:	Qt Interface for Transmission BitTorrent client
Group:		Networking/File transfer
Provides:	%{name}-gui = %{version}-%{release}
Requires:	%{name}-common = %{version}
%rename %{name}-qt4

%description qt
Transmission is a simple BitTorrent client. It features a very simple,
intuitive interface (gui and command-line) on top on an efficient,
cross-platform back-end.

This package contains QTransmission, a QT4 based GUI for Transmission
loosely based on the GTK+ client.

%package daemon
Summary:	Qt Interface for Transmission BitTorrent client
Group:		Networking/File transfer
Requires:	%{name}-common = %{version}
BuildRequires:	rpm-helper
Requires(post,preun):	rpm-helper

%description daemon
Transmission is a simple BitTorrent client. It features a very simple,
intuitive interface (gui and command-line) on top on an efficient,
cross-platform back-end.

This package contains the transmission-daemon.

%pre daemon
%_pre_useradd transmission /var/lib/transmission /sbin/nologin

%postun daemon
%_postun_userdel transmission
%_postun_groupdel transmission

%prep
%setup -a1 -a2 -q -n %{name}-%{version}-beta.2

mv libutp-bf695bdfb047cdca9710ea9cffc4018669cf9548/* third-party/
mv libb64-91a38519cb18d3869b4f1c99b0a80726547054af/* third-party/

%build
%cmake	\
	-DENABLE_GTK=ON \
	-DENABLE_QT=ON \
	-DUSE_QT_VERSION=6 \
	-DENABLE_CLI=ON \
	-DENABLE_TESTS=OFF
%make_build


%install
%make_install -C build

mkdir -p %{buildroot}%{_unitdir}
install -m0644 daemon/transmission-daemon.service %{buildroot}%{_unitdir}/

%if %{with gtk}
%find_lang %{name}-gtk

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
convert -scale 48 %{buildroot}/usr/share/pixmaps/transmission.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png 
convert -scale 32 %{buildroot}/usr/share/pixmaps/transmission.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{buildroot}/usr/share/pixmaps/transmission.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%endif

#Qt Gui Installation
pushd qt
INSTALL_ROOT=%{buildroot}%{_prefix} make install
popd

# Install transmission-qt.desktop manually as make install doesn't install it:
install -m644 qt/transmission-qt.desktop -D %{buildroot}%{_datadir}/applications/transmission-qt.desktop

# Configure transmission-daemon
sed -i -e 's,--log-error,--log-error --config-dir %{_sysconfdir}/transmission-daemon,' %{buildroot}%{_unitdir}/transmission-daemon.service
mkdir -p \
	%{buildroot}/var/lib/transmission/download \
	%{buildroot}/var/lib/transmission/incoming \
	%{buildroot}/var/lib/transmission/torrents \
	%{buildroot}%{_sysconfdir}/transmission-daemon

cat >%{buildroot}%{_sysconfdir}/transmission-daemon/settings.json <<EOF
{
	"rpc-enabled": true,
	"rpc-whitelist": "127.0.0.1,10.*.*.*,192.168.*.*",
	"download-dir": "/var/lib/transmission/download",
	"incomplete-dir-enabled": true,
	"incomplete-dir": "/var/lib/transmission/incoming",
	"watch-dir": "/var/lib/transmission/torrents"
}
EOF


%files common
%doc AUTHORS
%{_datadir}/%{name}
%if %{with gtk}
%{_datadir}/pixmaps/%{name}.png
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/appdata/transmission-gtk.appdata.xml
%endif

%files cli
%{_bindir}/%{name}-cli
%{_bindir}/%{name}-create
%{_bindir}/%{name}-edit
%{_bindir}/%{name}-remote
%{_bindir}/%{name}-show
%doc %{_mandir}/man1/%{name}-cli.1*
%doc %{_mandir}/man1/%{name}-create.1*
%doc %{_mandir}/man1/%{name}-edit.1*
%doc %{_mandir}/man1/%{name}-remote.1*
%doc %{_mandir}/man1/%{name}-show.1*

%files daemon
%{_unitdir}/*.service
%{_bindir}/%{name}-daemon
%doc %{_mandir}/man1/%{name}-daemon.1*
%{_sysconfdir}/transmission-daemon
%attr(0775,transmission,transmission) /var/lib/transmission

%if %with gtk
%files gtk -f %{name}-gtk.lang
%{_bindir}/%{name}-gtk
%{_datadir}/applications/%{name}-gtk.desktop
%doc %{_mandir}/man1/%{name}-gtk.1*
%endif

%files qt
%{_bindir}/%{name}-qt
%{_datadir}/applications/%{name}-qt.desktop
%doc %{_mandir}/man1/%{name}-qt.1*
