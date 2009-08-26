%define svn	0
%define rel	3
%if %svn
%define release		%mkrel 0.%svn.%rel
%define distname	%{name}-%{svn}.tar.lzma
%define dirname		%{name}
%else
%define release		%mkrel %rel
%define distname	%{name}-%{version}.tar.lzma
%define dirname		%{name}-%{version}
%endif

Summary:	Simple Bittorrent client
Name:		transmission
Version:	1.74
Release:	%{release}
Source0:	http://download.m0k.org/transmission/files/%{distname}
License:	MIT and GPLv2
Group:		Networking/File transfer
URL:		http://www.transmissionbt.com/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gtk+2-devel
BuildRequires:	qt4-devel
BuildRequires:	bzip2
BuildRequires:	openssl-devel
BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	libcurl-devel
BuildRequires:	libnotify-devel
BuildRequires:	libevent-devel
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
%setup -q -n %{dirname}

%build
%configure2_5x
%make

#QT Gui
pushd qt
%qmake_qt4 qtr.pro
%make
popd

%install
rm -rf %{buildroot}
%makeinstall_std
%find_lang %{name}

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
convert -scale 48 %{buildroot}/usr/share/pixmaps/transmission.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png 
convert -scale 32 %{buildroot}/usr/share/pixmaps/transmission.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{buildroot}/usr/share/pixmaps/transmission.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

#Qt Gui Installation
pushd qt
INSTALL_ROOT=%{buildroot}%{_prefix} make install
popd

# Creating the desktop file for qt4 gui based on the GTK one
sed -e 's,Exec=transmission,Exec=qtr,g' -e 's,GTK,QT,g' < %{buildroot}/%{_datadir}/applications/%{name}.desktop > %{buildroot}/%{_datadir}/applications/mandriva-%{name}-qtr.desktop

%clean
rm -rf %{buildroot}

%files common
%defattr(-,root,root)
%doc README NEWS AUTHORS
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_iconsdir}/hicolor/*/apps/*

%files cli
%defattr(-,root,root)
%{_bindir}/%{name}cli
%{_bindir}/%{name}-remote
%{_mandir}/man1/transmission-remote.1*
%{_mandir}/man1/transmissioncli.1*

%files daemon
%defattr(-,root,root)
%{_bindir}/transmission-daemon
%{_mandir}/man1/transmission-daemon.1*

%files gtk -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/transmission.1*

%files qt4
%defattr(-,root,root)
%{_bindir}/qtr
%{_datadir}/applications/mandriva-%{name}-qtr.desktop
