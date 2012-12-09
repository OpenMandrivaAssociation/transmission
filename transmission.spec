%bcond_without gtk

Summary:	Simple Bittorrent client
Name:		transmission
Version:	2.72
Release:	1
Source0:	http://download.transmissionbt.com/files/%{name}-%{version}.tar.xz
License:	MIT and GPLv2
Group:		Networking/File transfer
URL:		http://www.transmissionbt.com/
Patch0:		transmission-2.51-mdv-desktop.patch
BuildRequires:	qt4-devel >= 4:4.6.0
BuildRequires:	bzip2
BuildRequires:	pkgconfig(openssl)
BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	intltool

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
BuildRequires:	gtk+2-devel
BuildRequires:	libGConf2-devel
BuildRequires:	pkgconfig(libcanberra-gtk)
BuildRequires:	pkgconfig(ndesk-dbus-glib-1.0)
BuildRequires:	pkgconfig(libnotify)
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


%package qt4
Summary:	Qt4 Interface for Transmission BitTorrent client
Group:		Networking/File transfer
Provides:	%{name}-gui = %{version}-%{release}
Requires:	%{name}-common = %{version}

%description qt4
Transmission is a simple BitTorrent client. It features a very simple,
intuitive interface (gui and command-line) on top on an efficient,
cross-platform back-end.

This package contains QTransmission, a QT4 based GUI for Transmission
loosely based on the GTK+ client.


%package daemon
Summary:	Qt4 Interface for Transmission BitTorrent client
Group:		Networking/File transfer
Requires:	%{name}-common = %{version}

%description daemon
Transmission is a simple BitTorrent client. It features a very simple,
intuitive interface (gui and command-line) on top on an efficient,
cross-platform back-end.

This package contains the transmission-daemon.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
%configure
%make

#QT Gui
pushd qt
%qmake_qt4 qtr.pro
%make
popd

%install
%makeinstall_std
%if %with gtk
%find_lang %{name}-gtk
%endif

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
convert -scale 48 %{buildroot}/usr/share/pixmaps/transmission.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png 
convert -scale 32 %{buildroot}/usr/share/pixmaps/transmission.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{buildroot}/usr/share/pixmaps/transmission.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

#Qt Gui Installation
pushd qt
INSTALL_ROOT=%{buildroot}%{_prefix} make install
popd

# Install transmission-qt.desktop manually as make install doesn't install it:
cp -a qt/transmission-qt.desktop %{buildroot}/%{_datadir}/applications/

%files common
%doc README NEWS AUTHORS
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_iconsdir}/hicolor/*/apps/*

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
%{_bindir}/%{name}-daemon
%{_mandir}/man1/%{name}-daemon.1*

%if %with gtk
%files gtk -f %{name}-gtk.lang
%{_bindir}/%{name}-gtk
%{_datadir}/applications/%{name}-gtk.desktop
%{_mandir}/man1/%{name}-gtk.1*
%endif

%files qt4
%{_bindir}/%{name}-qt
%{_datadir}/applications/%{name}-qt.desktop
%{_mandir}/man1/%{name}-qt.1*
