%bcond_without gtk

Summary:	Simple Bittorrent client
Name:		transmission
Version:	4.0.0.beta.2
Release:	1
License:	MIT and GPLv2
Group:		Networking/File transfer
Url:		http://www.transmissionbt.com/
Source0:	https://github.com/transmission/transmission/archive/refs/tags/4.0.0-beta.2/%{name}-4.0.0-beta.2.tar.gz
# Submodules, needed because source code tag was release without it. 
Source1:	https://github.com/transmission/libutp/archive/libutp-bf695bdfb047cdca9710ea9cffc4018669cf9548.tar.gz
Source2:	https://github.com/transmission/libb64/archive/libb64-91a38519cb18d3869b4f1c99b0a80726547054af.tar.gz
Source3:	https://github.com/transmission/wide-integer/archive/wide-integer-4de0b52ea939bada26fae7aef55a4d98eb1d8abb.tar.gz
Source4:	https://github.com/transmission/fast_float/archive/fast_float-662497742fea7055f0e0ee27e5a7ddc382c2c38e.tar.gz

BuildRequires:	dht
BuildRequires:	bzip2
BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	intltool
#BuildRequires:	gtest-source
BuildRequires:	miniupnpc-devel
BuildRequires:	libnatpmp-devel
BuildRequires:	cmake(utf8cpp)
BuildRequires:	pkgconfig(fmt)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libdeflate)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(libpsl)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(openssl)
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
Requires:	%{name}-daemon = %{version}-%{release}
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
Requires:	%{name}-daemon = %{version}-%{release}
%rename %{name}-qt6

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
%setup -a1 -a2 -a3 -a4 -q -n %{name}-4.0.0-beta.2

mv libutp-bf695bdfb047cdca9710ea9cffc4018669cf9548/* third-party/libutp/
mv libb64-91a38519cb18d3869b4f1c99b0a80726547054af/* third-party/libb64/
mv wide-integer-4de0b52ea939bada26fae7aef55a4d98eb1d8abb/* third-party/wide-integer/
mv fast_float-662497742fea7055f0e0ee27e5a7ddc382c2c38e/* third-party/fast_float/


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
%endif

%files common
%doc %{_datadir}/doc/transmission/
%{_datadir}/%{name}
%if %{with gtk}
%{_iconsdir}/hicolor/*/apps/*
%{_datadir}/metainfo/transmission-gtk.metainfo.xml
%endif

%files cli
%{_bindir}/%{name}-cli
%{_bindir}/%{name}-create
%{_bindir}/%{name}-edit
%{_bindir}/%{name}-remote
%{_bindir}/%{name}-show
%{_mandir}/man1/%{name}-cli.1*
%{_mandir}/man1/%{name}-create.1*
%{_mandir}/man1/%{name}-edit.1*
%{_mandir}/man1/%{name}-remote.1*
%{_mandir}/man1/%{name}-show.1*

%files daemon
%{_unitdir}/*.service
%{_bindir}/%{name}-daemon
%{_mandir}/man1/%{name}-daemon.1*

%if %with gtk
%files gtk -f %{name}-gtk.lang
%{_bindir}/%{name}-gtk
%{_datadir}/applications/%{name}-gtk.desktop
%{_mandir}/man1/%{name}-gtk.1*
%endif

%files qt
%{_bindir}/%{name}-qt
%{_datadir}/applications/%{name}-qt.desktop
%{_mandir}/man1/%{name}-qt.1*
