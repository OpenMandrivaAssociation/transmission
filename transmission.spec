%define svn 0
%if %svn
%define release %mkrel 1
%else
%define release %mkrel 1
%endif

Summary:	Simple Bittorrent client
Name:		transmission
Version:	1.22
Release:	%{release}
%if %svn
Source0:	%{name}-%{svn}.tar.bz2
%else
Source0:	http://download.m0k.org/transmission/files/%{name}-%{version}.tar.bz2
%endif
License:	MIT and GPLv2
Group:		Networking/File transfer
URL:		http://www.transmissionbt.com/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gtk+2-devel
BuildRequires:	bzip2
BuildRequires:	openssl-devel
BuildRequires:	desktop-file-utils
BuildRequires:	ImageMagick
BuildRequires:	libevent-devel
BuildRequires:	libcurl-devel

%description
Transmission is a free, lightweight BitTorrent client. It features a 
simple, intuitive interface on top of an efficient back-end.

%prep
%if %svn
%setup -q -n %{name}
%else
%setup -q
%endif

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std
%find_lang %{name}

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
convert -scale 48 %{buildroot}/usr/share/pixmaps/transmission.png %buildroot%{_iconsdir}/hicolor/48x48/apps/%{name}.png 
convert -scale 32 %{buildroot}/usr/share/pixmaps/transmission.png %buildroot%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{buildroot}/usr/share/pixmaps/transmission.png %buildroot%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%if %mdkversion < 200900
%post
%{update_icon_cache hicolor}
%{update_menus}
%{update_desktop_database}
%endif
%if %mdkversion < 200900
%postun
%{clean_icon_cache hicolor}
%{clean_menus}
%{clean_desktop_database}
%endif

%clean
rm -rf %{buildroot}

%files -f %name.lang
%defattr(-,root,root)
%doc README NEWS LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}cli
%{_bindir}/%{name}-daemon
%{_bindir}/%{name}-proxy
%{_bindir}/%{name}-remote
%{_bindir}/benc2php
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/*/*
