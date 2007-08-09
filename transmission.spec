%define name transmission
%define origname Transmission
%define version 0.72
%define svn 0
%if %svn
%define release %mkrel 0.%svn.1
%else
%define release %mkrel 2
%endif
%define major 0
%define libname %mklibname %name %major

Summary: Simple Bittorrent client
Name: %{name}
Version: %{version}
Release: %{release}
%if %svn
Source0: %{name}-%{svn}.tar.bz2
%else
Source0: %{origname}-%{version}.tar.bz2
%endif
Patch0: transmission-0.7.0-fix-man-dir.patch
Patch1: transmission-0.7.0-malformed-bencode.patch
License: MIT
Group: Networking/File transfer
Url: http://transmission.m0k.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libgtk+2-devel
BuildRequires: bzip2
BuildRequires: libopenssl-devel
BuildRequires: desktop-file-utils
BuildRequires: ImageMagick

%description
Transmission is a free, lightweight BitTorrent client. It features a 
simple, intuitive interface on top of an efficient back-end.

%prep
%if %svn
%setup -q -n %{origname}
%else
%setup -q -n %{origname}
%endif
%patch0 -p0 -b .fixmandir
%patch1 -p0 -b .malformed-bencode

%build
%configure
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
%find_lang %{name}

mkdir -p %buildroot{%_liconsdir,%_miconsdir}
mkdir -p %buildroot%{_iconsdir}/hicolor
mkdir -p %buildroot%{_iconsdir}/hicolor/{48x48,32x32,24x24,22x22,16x16}
mkdir -p %buildroot%{_iconsdir}/hicolor/{48x48,32x32,24x24,22x22,16x16}/apps
convert -scale 48 $RPM_BUILD_ROOT/usr/share/pixmaps/transmission.png %buildroot%_liconsdir/%{name}.png
convert -scale 48 $RPM_BUILD_ROOT/usr/share/pixmaps/transmission.png %buildroot%_iconsdir/hicolor/48x48/apps/%{name}.png 
convert -scale 32 $RPM_BUILD_ROOT/usr/share/pixmaps/transmission.png %buildroot%_iconsdir/%{name}.png
convert -scale 32 $RPM_BUILD_ROOT/usr/share/pixmaps/transmission.png %buildroot%_iconsdir/hicolor/32x32/apps/%{name}.png
convert -scale 24 $RPM_BUILD_ROOT/usr/share/pixmaps/transmission.png %buildroot%_iconsdir/hicolor/24x24/apps/%{name}.png
convert -scale 22 $RPM_BUILD_ROOT/usr/share/pixmaps/transmission.png %buildroot%_iconsdir/hicolor/22x22/apps/%{name}.png
convert -scale 16 $RPM_BUILD_ROOT/usr/share/pixmaps/transmission.png %buildroot%_miconsdir/%{name}.png
convert -scale 16 $RPM_BUILD_ROOT/usr/share/pixmaps/transmission.png %buildroot%_iconsdir/hicolor/16x16/apps/%{name}.png

%post
%update_icon_cache hicolor
%update_menus
%update_desktop_database
%postun
%clean_icon_cache hicolor
%clean_menus
%clean_desktop_database

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-,root,root)
%doc README NEWS
%_bindir/%{name}-gtk
%_bindir/%{name}cli
%_mandir/man1/%{name}-gtk.1*
%_mandir/man1/%{name}cli.1*
%lang(fr) %_datadir/locale/fr/LC_MESSAGES/transmission-gtk.mo
%lang(it) %_datadir/locale/it/LC_MESSAGES/transmission-gtk.mo
%lang(bg) %_datadir/locale/bg/LC_MESSAGES/transmission-gtk.mo
%lang(es) %_datadir/locale/es/LC_MESSAGES/transmission-gtk.mo
%lang(fi) %_datadir/locale/fi/LC_MESSAGES/transmission-gtk.mo
%lang(pl) %_datadir/locale/pl/LC_MESSAGES/transmission-gtk.mo
%lang(ro) %_datadir/locale/ro/LC_MESSAGES/transmission-gtk.mo
%lang(ru) %_datadir/locale/ru/LC_MESSAGES/transmission-gtk.mo
%lang(sv) %_datadir/locale/sv/LC_MESSAGES/transmission-gtk.mo
%_datadir/applications/transmission-gtk.desktop
%_datadir/pixmaps/%{name}.png
%_datadir/zsh/site-functions/_transmissioncli
%_iconsdir/hicolor/*/apps/%{name}.png
%_liconsdir/%{name}.png
%_iconsdir/%{name}.png
%_miconsdir/%{name}.png
