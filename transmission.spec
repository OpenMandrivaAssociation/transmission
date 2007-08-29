%define name transmission
%define origname Transmission
%define version 0.81
%define svn 0
%if %svn
%define release %mkrel 0.%svn.1
%else
%define release %mkrel 1
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
Source0: %{origname}-%{version}.tar.gz
%endif
Patch0: transmission-0.7.0-fix-man-dir.patch
License: MIT and GPLv2
Group: Networking/File transfer
Url: http://transmission.m0k.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libgtk+2-devel
BuildRequires: bzip2
BuildRequires: libopenssl-devel
BuildRequires: desktop-file-utils
BuildRequires: ImageMagick
BuildRequires: libevent-devel

%description
Transmission is a free, lightweight BitTorrent client. It features a 
simple, intuitive interface on top of an efficient back-end.

%prep
%if %svn
%setup -q -n %{name}
%else
%setup -q -c
%endif
%patch0 -p0 -b .fixmandir

%build
%configure
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
%find_lang %{name}

mkdir -p %buildroot%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
convert -scale 48 $RPM_BUILD_ROOT/usr/share/pixmaps/transmission.png %buildroot%_iconsdir/hicolor/48x48/apps/%{name}.png 
convert -scale 32 $RPM_BUILD_ROOT/usr/share/pixmaps/transmission.png %buildroot%_iconsdir/hicolor/32x32/apps/%{name}.png
convert -scale 16 $RPM_BUILD_ROOT/usr/share/pixmaps/transmission.png %buildroot%_iconsdir/hicolor/16x16/apps/%{name}.png

perl -pi -e 's,transmission.png,%{name},g' %buildroot%_datadir/applications/transmission-gtk.desktop

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
%doc README NEWS LICENSE
%_bindir/%{name}-gtk
%_bindir/%{name}cli
%_bindir/%{name}-daemon
%_bindir/%{name}-proxy
%_bindir/%{name}-remote
%_mandir/man1/%{name}-gtk.1*
%_mandir/man1/%{name}cli.1*
%_mandir/man1/%{name}-daemon.1*
%_mandir/man1/%{name}-proxy.1*
%_mandir/man1/%{name}-remote.1*
%lang(fr) %_datadir/locale/fr/LC_MESSAGES/transmission-gtk.mo
%lang(it) %_datadir/locale/it/LC_MESSAGES/transmission-gtk.mo
%lang(bg) %_datadir/locale/bg/LC_MESSAGES/transmission-gtk.mo
%lang(es) %_datadir/locale/es/LC_MESSAGES/transmission-gtk.mo
%lang(fi) %_datadir/locale/fi/LC_MESSAGES/transmission-gtk.mo
%lang(nl) %_datadir/locale/nl/LC_MESSAGES/transmission-gtk.mo
%lang(pl) %_datadir/locale/pl/LC_MESSAGES/transmission-gtk.mo
%lang(pt) %_datadir/locale/pt/LC_MESSAGES/transmission-gtk.mo
%lang(pt_BR) %_datadir/locale/pt_BR/LC_MESSAGES/transmission-gtk.mo
%lang(ro) %_datadir/locale/ro/LC_MESSAGES/transmission-gtk.mo
%lang(ru) %_datadir/locale/ru/LC_MESSAGES/transmission-gtk.mo
%lang(sk) %_datadir/locale/sk/LC_MESSAGES/transmission-gtk.mo
%lang(sv) %_datadir/locale/sv/LC_MESSAGES/transmission-gtk.mo
%_datadir/applications/transmission-gtk.desktop
%_datadir/pixmaps/%{name}.png
%_datadir/zsh/site-functions/_transmissioncli
%_iconsdir/hicolor/*/apps/%{name}.png

