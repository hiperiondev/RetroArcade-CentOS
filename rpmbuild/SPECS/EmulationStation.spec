#
# spec file for package EmulationStation
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


# See also http://en.opensuse.org/openSUSE:Specfile_guidelines
Name:           EmulationStation
Version:        master
Release:        lastest.git
Summary:        A cross-platform graphical front-end for emulators
License:        MIT
Group:          System/Emulators/Other
URL:            http://www.emulationstation.org/
Source0:        %{name}.zip
Source1:        es_icon.png
Source2:        es_systems.cfg
#Source3:        README.openSUSE
Source4:        themes.tar.gz
#Patch0:         stringcompare.patch
#Patch1:         date_time.patch
BuildRequires:  alsa-lib-devel
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  eigen3-devel
BuildRequires:  freeimage-devel
BuildRequires:  freetype-devel
BuildRequires:  gcc-c++
BuildRequires:  SDL2-devel
BuildRequires:  boost-date-time
BuildRequires:  boost-filesystem
BuildRequires:  boost-locale
BuildRequires:  boost-system
BuildRequires:  libcurl-devel

%description
A graphical and themeable emulator front-end that allows you to access all your favorite games in one place, even without a keyboard!

%prep
%setup -q
%setup -q -T -D -a 4
#%patch0
#%patch1

%build
%cmake
make

%install
#cd build
%make_install
#cd ..

install -D -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/es_icon.png
install -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/emulationstation/es_systems.cfg
mkdir -p %{buildroot}%{_sysconfdir}/emulationstation/themes/simple
cp -r themes %{buildroot}%{_sysconfdir}/emulationstation/

#Doc files
mkdir -p %{buildroot}%{_docdir}/EmulationStation/
install -D -m 0644 *.md %{buildroot}%{_docdir}/EmulationStation/

#Resources
cp -r resources/ %{buildroot}/%{_bindir} 

#missed desktop file, writing one
mkdir -p %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=EmulationStation
GenericName=EmulationStation
Comment= A cross-platform graphical front-end for emulators
Comment[it]= Un front-end grafico per emulatori cross-platform
Exec=%{_bindir}/emulationstation
Icon=es_icon
StartupNotify=true
Terminal=false
Type=Application
Categories=Game;Simulation;
EOF

%files
%{_bindir}/emulationstation
%{_bindir}/resources/
%{_datadir}/pixmaps/es_icon.png
%{_datadir}/applications/%{name}.desktop
%{_libdir}/* 
%{_includedir}/*
%dir %{_sysconfdir}/emulationstation/
%dir %{_sysconfdir}/emulationstation/themes/
%config %{_sysconfdir}/emulationstation/themes/simple/
%config %{_sysconfdir}/emulationstation/themes/crt/
%config %{_sysconfdir}/emulationstation/themes/crt-centered/
%config %{_sysconfdir}/emulationstation/es_systems.cfg
%docdir %{_docdir}/EmulationStation/
%{_docdir}/EmulationStation/

%changelog
* Fri May 10 2019 Christian Galeffi <chri@gallochri.com>
- Update to git version 9cc42ad
  * Merge pull request #594 from codinghipster/master
  * Fix linux (fedora) compilation issues
  * No changelog was made available.
* Thu Oct  4 2018 Christian Galeffi <chri@gallochri.com>
- declaration_conflict.patch removed
* Fri Mar 23 2018 chri@gallochri.com
- Libboost package splitted in Leap_15.0 Build
* Fri Mar 23 2018 chri@gallochri.com
- Service switched to obs_tar
- Libboost package splitted in TW/Factory Build
* Fri Nov 25 2016 aloisio@gmx.com
- Added EmulationStation-declaration_conflict.patch
  to fix TW/Factory build
* Wed Jan  6 2016 chri@gallochri.com
-Fixed libfreeimage require 3.15.4
* Wed Jan  6 2016 chri@gallochri.com
-Update readme.opensuse
* Tue Jan  5 2016 chri@gallochri.com
-Fixed Freeimage version to 3.15.4
* Tue Jan  5 2016 chri@gallochri.com
-Added themes, systems configurations file and openSUSE README
* Mon Jan  4 2016 chri@gallochri.com
-PNG icon file added
* Sun Jan  3 2016 chri@gallochri.com
-Doc and desktopfile added
* Sun Jan  3 2016 chri@gallochri.com
-Split patches
* Sun Jan  3 2016 chri@gallochri.com
-Compare string errors fixed
* Sat Jan  2 2016 chri@gallochri.com
-Use of cmake macros added
* Fri Jan  1 2016 chri@gallochri.com
-First build
* Fri Jan  1 2016 chri@gallochri.com
-Initial version
