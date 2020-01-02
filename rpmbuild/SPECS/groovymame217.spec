#The debug build is disabled by default, please use # --with debug to override
%bcond_with debug

%global baseversion 217
%global name2 mame

Name:           groovymame
Version:        0.%{baseversion}
Release:        1%{?dist}
Summary:        Multiple Arcade Machine Emulator

#LGPLv2+:
#src/mame/audio/snes_snd.cpp: LGPL (v2 or later)
#src/devices/sound/tiasound.cpp: LGPL (v2) (with incorrect FSF address)
#src/devices/sound/tiasound.h: LGPL (v2) (with incorrect FSF address)
#
#ASL 2.0
#3rdparty/bgfx 

License:        GPLv2+ and LGPLv2+ and ASL 2.0
URL:            http://mamedev.org/
Source0:        https://github.com/mamedev/%{name}/releases/download/%{name}0%{baseversion}/%{name2}0%{baseversion}s.exe
Source1:        http://mamedev.org/releases/whatsnew_0%{baseversion}.txt
Patch0:         %{name2}-fortify.patch
Patch1:         %{name2}-genie-systemlua.patch
Patch2:         0217_groovymame_017p.diff
# %%{arm}:
# https://bugzilla.redhat.com/show_bug.cgi?id=1627625
# %%{power64}:
# https://github.com/mamedev/mame/issues/3157
# https://bugzilla.redhat.com/show_bug.cgi?id=1541613
ExcludeArch:    %{arm} %{power64}

#asio in Fedora repositories is too old (1.11.x is needed)
#BuildRequires:  asio-devel
BuildRequires:  expat-devel
BuildRequires:  flac-devel
BuildRequires:  fontconfig-devel
BuildRequires:  gcc-c++
BuildRequires:  glm-devel
BuildRequires:  jack-audio-connection-kit
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libXi-devel
BuildRequires:  libXinerama-devel
BuildRequires:  lua-devel >= 5.3.0
BuildRequires:  p7zip
BuildRequires:  portaudio-devel
BuildRequires:  portmidi-devel
BuildRequires:  pugixml-devel
#BuildRequires:  python3-sphinx_rtd_theme
#BuildRequires:  python3-sphinxcontrib-rsvgconverter
BuildRequires:  qt5-qtbase-devel
BuildRequires:  rapidjson-devel
BuildRequires:  SDL2_ttf-devel
BuildRequires:  sqlite-devel
BuildRequires:  utf8proc-devel
BuildRequires:  zlib-devel
Requires:       %{name2}-data = %{version}-%{release}

#bx and bgfx are not made to be linked to dynamically as per http://forums.bannister.org/ubbthreads.php?ubb=showflat&Number=104437
Provides:       bundled(bgfx)
Provides:       bundled(bimg)
Provides:       bundled(bx)
#fedora contains linenoise package but it is not compatible
Provides:       bundled(linenoise)
#Below have no fedora packages ATM and are very tiny
Provides:       bundled(lsqlite3)
Provides:       bundled(luafilesystem)
Provides:       bundled(lua-linenoise)
Provides:       bundled(lua-zlib)
#lzma is not made to be linked dynamically
Provides:       bundled(lzma-sdk) = 16.04
#minimp3 is just two header files
Provides:       bundled(minimp3)
#softfloat is not made to be linked dynamically
Provides:       bundled(softfloat)
#ldplayer has been turned into a regular mame driver in 0.180 cycle
Provides:       %{name}-ldplayer = %{version}-%{release}
Obsoletes:      %{name}-ldplayer < 0.179-4


%description
MAME stands for Multiple Arcade Machine Emulator.  When used in conjunction
with an arcade game's data files (ROMs), MAME will more or less faithfully
reproduce that game on a PC.

The ROM images that MAME utilizes are "dumped" from arcade games' original
circuit-board ROM chips.  MAME becomes the "hardware" for the games, taking
the place of their original CPUs and support chips.  Therefore, these games
are NOT simulations, but the actual, original games that appeared in arcades.

MAME's purpose is to preserve these decades of video-game history.  As gaming
technology continues to rush forward, MAME prevents these important "vintage"
games from being lost and forgotten.  This is achieved by documenting the
hardware and how it functions, thanks to the talent of programmers from the
MAME team and from other contributors.  Being able to play the games is just
a nice side-effect, which doesn't happen all the time.  MAME strives for
emulating the games faithfully.

%package tools
Summary:        Additional tools for MAME
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
%{summary}.

%package data
Summary:        Data files used by MAME

BuildArch:      noarch

%description data
%{summary}.

%package data-software-lists
Summary:        Software lists used by MAME
Requires:       %{name}-data = %{version}-%{release}

BuildArch:      noarch

%description data-software-lists
%{summary}. These are split from the main -data
subpackage due to relatively large size.

%package doc
Summary:        Documentation for MAME

BuildArch:      noarch

%description doc
HTML documentation for MAME.


%prep
%setup -qcT

#do not extract system libs or document themes to ensure system ones are used
#do not extract 3rdparty code not needed on Linux
7za x \
    -xr!3rdparty/compat \
    -xr!3rdparty/dxsdk \
    -xr!3rdparty/expat \
    -xr!3rdparty/genie/src/host/lua-5.3.0 \
    -xr!3rdparty/glm \
    -xr!3rdparty/libflac \
    -xr!3rdparty/libjpeg \
    -xr!3rdparty/lua \
    -xr!3rdparty/portaudio \
    -xr!3rdparty/portmidi \
    -xr!3rdparty/pugixml \
    -xr!3rdparty/rapidjson \
    -xr!3rdparty/SDL2 \
    -xr!3rdparty/SDL2-override \
    -xr!3rdparty/sqlite3 \
    -xr!3rdparty/tap-windows6 \
    -xr!3rdparty/utf8proc \
    -xr!3rdparty/winpcap \
    -xr!3rdparty/zlib \
    -xr!docs/themes \
    %{SOURCE0}

install -pm 644 %{SOURCE1} whatsnew_0%{baseversion}.txt

find \( -regex '.*\.\(c\|cpp\|fsh\|fx\|h\|hpp\|lua\|make\|map\|md\|txt\|vsh\|xml\)$' \
    -o -wholename ./makefile \) -exec sed -i 's@\r$@@' {} \;

%patch0 -p1 -b .fortify
%patch1 -p1 -b .systemlua
%patch2 -p1 -b .groovymame

# Create ini files
cat > %{name}.ini << EOF
# Define multi-user paths
artpath            %{_datadir}/%{name}/artwork;%{_datadir}/%{name}/effects
bgfx_path          %{_datadir}/%{name}/bgfx
cheatpath          %{_datadir}/%{name}/cheat
crosshairpath      %{_datadir}/%{name}/crosshair
ctrlrpath          %{_datadir}/%{name}/ctrlr
fontpath           %{_datadir}/%{name}/fonts
hashpath           %{_datadir}/%{name}/hash
languagepath       %{_datadir}/%{name}/language
pluginspath        %{_datadir}/%{name}/plugins
rompath            %{_datadir}/%{name}/roms;%{_datadir}/%{name}/chds
samplepath         %{_datadir}/%{name}/samples

# Allow user to override ini settings
inipath            \$HOME/.%{name}/ini;%{_sysconfdir}/%{name}

# Set paths for local storage
cfg_directory      \$HOME/.%{name}/cfg
comment_directory  \$HOME/.%{name}/comments
diff_directory     \$HOME/.%{name}/diff
input_directory    \$HOME/.%{name}/inp
nvram_directory    \$HOME/.%{name}/nvram
snapshot_directory \$HOME/.%{name}/snap
state_directory    \$HOME/.%{name}/sta

# Fedora custom defaults
video              opengl
autosave           1
EOF

#ensure genie uses $RPM_OPT_FLAGS and $RPM_LD_FLAGS
sed -i "s@-Wall -Wextra -Os \$(MPARAM)@$RPM_OPT_FLAGS@" 3rdparty/genie/build/gmake.linux/genie.make
sed -i "s@-s -rdynamic@$RPM_LD_FLAGS -rdynamic@" 3rdparty/genie/build/gmake.linux/genie.make

#rename various license files so that they can be installed with %%license
mv artwork/LICENSE LICENSE.CC0
mv bgfx/LICENSE LICENSE.BSD3
mv plugins/json/LICENSE LICENSE.MIT

%build
#save some space
MAME_FLAGS="NOWERROR=1 OPTIMIZE=2 PYTHON_EXECUTABLE=python3 VERBOSE=1 \
    USE_SYSTEM_LIB_EXPAT=1 \
    USE_SYSTEM_LIB_FLAC=1 \
    USE_SYSTEM_LIB_GLM=1 \
    USE_SYSTEM_LIB_JPEG=1 \
    USE_SYSTEM_LIB_LUA=1 \
    USE_SYSTEM_LIB_PORTAUDIO=1 \
    USE_SYSTEM_LIB_PORTMIDI=1 \
    USE_SYSTEM_LIB_PUGIXML=1 \
    USE_SYSTEM_LIB_RAPIDJSON=1 \
    USE_SYSTEM_LIB_SQLITE3=1 \
    USE_SYSTEM_LIB_UTF8PROC=1 \
    USE_SYSTEM_LIB_ZLIB=1 \
    SDL_INI_PATH=%{_sysconfdir}/%{name};"

#standard -g caused problems with OOM or relocation overflows
RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | sed "s@-g@-g1@")
#32-bit architectures need even more measures
%ifarch %{ix86}
RPM_LD_FLAGS="$RPM_LD_FLAGS -Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif
%ifarch %{arm}
RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | sed "s@-O2@-Os@")
RPM_LD_FLAGS="$RPM_LD_FLAGS -Wl,--no-keep-memory -fuse-ld=gold"
MAME_FLAGS=$(echo $MAME_FLAGS | sed "s@OPTIMIZE=2@OPTIMIZE=s@")
%endif

%if %{with debug}
%make_build $MAME_FLAGS DEBUG=1 TOOLS=1 OPT_FLAGS="$RPM_OPT_FLAGS" \
    LDOPTS="$RPM_LD_FLAGS"
%else
%make_build $MAME_FLAGS TOOLS=1 OPT_FLAGS="$RPM_OPT_FLAGS" \
    LDOPTS="$RPM_LD_FLAGS"
%endif

pushd docs
    %make_build html
popd


%install
rm -rf $RPM_BUILD_ROOT

# create directories
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
for folder in cfg comments diff ini inp memcard nvram snap sta
do
    install -d $RPM_BUILD_ROOT%{_sysconfdir}/skel/.%{name}/$folder
done
install -d $RPM_BUILD_ROOT%{_bindir}
for folder in artwork bgfx chds cheats ctrlr effects fonts hash language \
    plugins keymaps roms samples shader
do
    install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/$folder
done
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -d $RPM_BUILD_ROOT%{_mandir}/man6

# install files
install -pm 644 %{name}.ini $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
%if %{with debug}
install -pm 755 %{name2}d $RPM_BUILD_ROOT%{_bindir}/%{name}d || \
install -pm 755 %{name2}64d $RPM_BUILD_ROOT%{_bindir}/%{name}d
%else
install -pm 755 %{name2} $RPM_BUILD_ROOT%{_bindir}/%{name} || \
install -pm 755 %{name2}64 $RPM_BUILD_ROOT%{_bindir}/%{name}
%endif
install -pm 755 castool chdman floptool imgtool jedutil ldresample ldverify \
    nltool nlwav pngcmp romcmp unidasm $RPM_BUILD_ROOT%{_bindir}
for tool in regrep split src2html srcclean
do
    install -pm 755 $tool $RPM_BUILD_ROOT%{_bindir}/%{name}-$tool
done
pushd artwork
    find -type d -exec install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/artwork/{} \;
    find -type f -exec install -pm 644 {} $RPM_BUILD_ROOT%{_datadir}/%{name}/artwork/{} \;
popd
pushd bgfx
    find -type d -a ! -wholename \*dx\* -a ! -wholename \*metal\* -exec install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/bgfx/{} \;
    find -type f -a ! -wholename \*dx\* -a ! -wholename \*metal\* -exec install -pm 644 {} $RPM_BUILD_ROOT%{_datadir}/%{name}/bgfx/{} \;
popd
install -pm 644 hash/* $RPM_BUILD_ROOT%{_datadir}/%{name}/hash
install -pm 644 keymaps/* $RPM_BUILD_ROOT%{_datadir}/%{name}/keymaps
pushd language
    find -type d -exec install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/language/{} \;
    find -type f -name \*.mo -exec install -pm 644 {} $RPM_BUILD_ROOT%{_datadir}/%{name}/language/{} \;
    # flag the translation files as %%lang
    grep -r --include=*.po Language: | sed -r 's@(.*)/strings\.po:"Language: ([[:alpha:]]{2}(_[[:alpha:]]{2})?)\\n"@%lang(\2) %{_datadir}/%{name}/language/\1@' > ../%{name}.lang
popd
pushd plugins
    find -type d -exec install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins/{} \;
    find -type f -exec install -pm 644 {} $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins/{} \;
popd
pushd src/osd/modules/opengl
    install -pm 644 shader/*.?sh $RPM_BUILD_ROOT%{_datadir}/%{name}/shader
popd
pushd docs/man
install -pm 644 castool.1 chdman.1 imgtool.1 floptool.1 jedutil.1 ldresample.1 \
    ldverify.1 romcmp.1 $RPM_BUILD_ROOT%{_mandir}/man1
install -pm 644 mame.6 mess.6 $RPM_BUILD_ROOT%{_mandir}/man6
popd

#make sure only html documentation is installed
rm -f docs/.buildinfo
rm -rf docs/build/html/_sources

find $RPM_BUILD_ROOT%{_datadir}/%{name} -name LICENSE -exec rm {} \;


%files
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.ini
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/skel/.%{name}
%if %{with debug}
%{_bindir}/%{name}d
%else
%{_bindir}/%{name}
%endif
%{_mandir}/man6/mame.6*
%{_mandir}/man6/mess.6*

%files tools
%{_bindir}/castool
%{_bindir}/chdman
%{_bindir}/floptool
%{_bindir}/imgtool
%{_bindir}/jedutil
%{_bindir}/ldresample
%{_bindir}/ldverify
%{_bindir}/nltool
%{_bindir}/nlwav
%{_bindir}/pngcmp
%{_bindir}/%{name}-regrep
%{_bindir}/romcmp
%{_bindir}/%{name}-split
%{_bindir}/%{name}-src2html
%{_bindir}/%{name}-srcclean
%{_bindir}/unidasm
%{_mandir}/man1/castool.1*
%{_mandir}/man1/chdman.1*
%{_mandir}/man1/floptool.1*
%{_mandir}/man1/imgtool.1*
%{_mandir}/man1/jedutil.1*
%{_mandir}/man1/ldresample.1*
%{_mandir}/man1/ldverify.1*
%{_mandir}/man1/romcmp.1*

%files data -f %{name}.lang
%doc README.md whatsnew*.txt
%license LICENSE.md LICENSE.BSD3 LICENSE.CC0 LICENSE.MIT
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/artwork
%{_datadir}/%{name}/bgfx
%{_datadir}/%{name}/chds
%{_datadir}/%{name}/cheats
%{_datadir}/%{name}/effects
%{_datadir}/%{name}/fonts
%{_datadir}/%{name}/keymaps
%dir %{_datadir}/%{name}/language
%{_datadir}/%{name}/plugins
%{_datadir}/%{name}/roms
%{_datadir}/%{name}/samples
%{_datadir}/%{name}/shader

%files data-software-lists
%{_datadir}/%{name}/hash

%files doc
%doc docs/build/html/*


%changelog
* Wed Nov 27 2019 Julian Sikorski <belegdol@fedoraproject.org> - 0.216-1
- Update to 0.216

* Wed Oct 30 2019 Julian Sikorski <belegdol@fedoraproject.org> - 0.215-1
- Update to 0.215
- Do not extract 3rdparty code not needed on Linux

* Sat Sep 28 2019 Julian Sikorski <belegdol@fedoraproject.org> - 0.214-1
- Update to 0.214

* Wed Sep 04 2019 Julian Sikorski <belegdol@fedoraproject.org> - 0.213-1
- Update to 0.213
- Drop upstreamed rapidjson patch

* Sat Aug 03 2019 Julian Sikorski <belegdol@fedoraproject.org> - 0.212-1
- Update to 0.212

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.211-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Julian Sikorski <belegdol@fedoraproject.org> - 0.211-1
- Update to 0.211

* Sun Jun 02 2019 Julian Sikorski <belegdol@fedoraproject.org> - 0.210-1
- Update to 0.210
- Add libXi-devel to BuildRequires
- Flag translation files as %%lang
- Clean up mame-doc subpackage
- Drop hlsl shaders as they only work on Windows
- Drop bgfx dx9, dx11 and metal shaders as they only work on Windows and macOS, respectively

* Wed Apr 24 2019 Julian Sikorski <belegdol@fedoraproject.org> - 0.209-1
- Update to 0.209

* Wed Mar 27 2019 Julian Sikorski <belegdol@fedoraproject.org> - 0.208-1
- Update to 0.208
- Add python3-sphinx_rtd_theme to BuildRequires

* Wed Feb 27 2019 Julian Sikorski <belegdol@fedoraproject.org> - 0.207-1
- Update to 0.207
- Add python3-sphinxcontrib-rsvgconverter to BuildRequires

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.206-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Julian Sikorski <belegdol@fedoraproject.org> - 0.206-1
- Update to 0.206

* Fri Dec 28 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.205-1
- Update to 0.205
- Add jack-audio-connection-kit to BuildRequires

* Wed Nov 28 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.204-1
- Update to 0.204

* Thu Nov 01 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.203-1
- Update to 0.203

* Wed Sep 26 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.202-1
- Updated to 0.202

* Thu Aug 30 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.201-1
- Update to 0.201
- Drop upstreamed imgtool patch
- Add ExcludeArch: %%{arm} due to issues with linker running out of memory
- Apply -g1 across the board to prevent relocation overflows

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.200-3
- Rebuild with fixed binutils

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.200-2
- Rebuild for new binutils

* Wed Jul 25 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.200-1
- Updated to 0.200
- Re-enabled %%{arm} build

* Mon Jul 23 2018 Bastien Nocera <bnocera@redhat.com> - 0.199-4
- Fix imgtool options parsing

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.199-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.199-2
- Added riscv64 to the list of architectures needing -g1
- Rebuilt to fix issues caused by gcc PR86094

* Wed Jun 27 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.199-1
- Updated to 0.199
- Dropped upstreamed riscv64 patches
- Ensured $RPM_OPT_FLAGS are used when building m68kmake
- Ensured memory-saving compiler/linker flags are only used when needed

* Wed May 30 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.198-1
- Updated to 0.198
- Ensured python3 is called explicitly as per https://fedoraproject.org/wiki/Changes/Avoid_usr_bin_python_in_RPM_Build
- Updated BuildRequires to python3-sphinx

* Wed Apr 25 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.197-1
- Updated to 0.197
- Dropped upstreamed pugixml patch

* Wed Mar 28 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.196-1
- Updated to 0.196
- Updated to use system pugixml
- Added gcc-c++ to BuildRequires as per https://fedoraproject.org/wiki/Packaging:C_and_C%2B%2B#BuildRequires_and_Requires

* Fri Mar 09 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.195-1
- Updated to 0.195
- Updated to use system glm and rapidjson (asio in Fedora repositories is too old)
- Made MAME_FLAGS definition more easy to follow
- Added *.hpp to files needing line endings conversion

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.194-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.194-1
- Updated to 0.194
- Added ExcludeArch for ppc64 and ppc64le due to issues with long double

* Sun Dec 31 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.193-1
- Updated to 0.193

* Fri Dec 01 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.192-1
- Updated to 0.192

* Wed Oct 25 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.191-1
- Updated to 0.191

* Wed Sep 27 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.190-1
- Updated to 0.190

* Wed Aug 30 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.189-1
- Updated to 0.189

* Tue Aug 08 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.188-1
- Updated to 0.188

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.187-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.187-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 28 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.187-1
- Updated to 0.187

* Tue Jun 06 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.186-1
- Updated to 0.186

* Wed Apr 26 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.185-1
- Updated to 0.185

* Wed Mar 29 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.184-1
- Updated to 0.184

* Wed Feb 22 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.183-1
- Updated to 0.183
- Dropped upstreamed portaudio and utf8proc patches
- Do not extract unwanted folders instead of deleting them
- Dropped %%if 0%%{?fedora} >= 24 conditional as F23 is EOL

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.182-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 25 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.182-1
- Updated to 0.182
- Ensured system utf8proc is used
- Fixed system portaudio

* Wed Dec 28 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.181-1
- Updated to 0.181

* Wed Nov 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.180-1
- Updated to 0.180
- Dropped upstreamed ppc64le and s390x patches
- Dropped libuv from BuildRequires
- Dropped ldplayer subpackage, ldplayer is now part of mame

* Mon Nov 07 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.179-3
- Fixed s390x build

* Mon Nov 07 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.179-2
- Fixed ppc64le build
- Dropped NOASM=1 call, it is included in upstream makefile where needed

* Wed Oct 26 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.179-1
- Updated to 0.179

* Wed Sep 28 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.178-1
- Updated to 0.178

* Thu Sep 01 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.177-1
- Updated to 0.177
- Re-enabled ldplayer
- Added -doc subpackage

* Wed Jul 27 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.176-1
- Updated to 0.176
- Updated the fortify patch

* Mon Jul 11 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.175-2
- Added libXinerama-devel to BuildRequires since it is no longer pulled by
  SDL2-devel

* Wed Jun 29 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.175-1
- Updated to 0.175
- Dropped upstreamed patches
- Removed bundled lua-sqlite and http-parser provides as they were removed
- Ensured licenses for artwork and plugins are installed appropriately
- Disabled ldplayer since it does not build currently (Github #1015)

* Tue Jun 28 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.174-5
- Updated the License tag
- Made ldplayer dependent on the main package
- Dropped leftover mess-data provides
- Moved documentation to -data subpackage
- Made -data and -ldplayer Required arched

* Wed Jun 15 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.174-4
- Ensured Fedora compiler and linker flags are applied to genie as well
- Added 3rdparty/ cleanup commands
- Dropped SIMD and low memory conditionals
- Separated LICENSE.md to %%license
- Ensured genie is built using system lua
- Downgraded debug flags to -g1

* Tue Jun 14 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.174-3
- Cleaned up compiler and linker flags

* Mon Jun 13 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.174-2
- Updated SourceURL
- Added comments about bundled libraries
- Dropped old mess Provides

* Tue May 31 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.174-1
- Updated to 0.174

* Wed Apr 27 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.173-1
- Updated to 0.173
- Updated the bundled lib versions
- Removed lua from bundled libs

* Thu Apr 07 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.172-1
- Updated to 0.172
- Dropped upstreamed patches
- Added new files to the %%install and %%files sections
- Updated the License

* Sat Mar 12 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.171-1
- Updated to 0.171
- Added ability to build using system libuv
- Cleaned up the list of bundled libs
- Fixed building with gcc-6

* Thu Jan 28 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.170-1
- Updated to 0.170
- Dropped the smpfix patch

* Thu Dec 31 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.169-1
- Updated to 0.169
- Updated the smpfix patch
- Updated BuildRequires for Qt5

* Thu Nov 26 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.168-1
- Updated to 0.168
- Updated the smpfix patch

* Thu Oct 29 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.167-1
- Update 0.167
- Updated the smpfix patch

* Thu Oct 01 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.166-1
- Updated to 0.166

* Thu Aug 27 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.165-1
- Updated to 0.165
- Updated the smpfix patch

* Thu Jul 30 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.164-1
- Updated to 0.164
- Dropped upstreamed patches

* Sat Jul 18 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.163-4
- Fixed debug conditional build (rfbz #3715)

* Tue Jul 14 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.163-3
- Fixed arm build
- Added crosshairpath to default .ini, removed memcard_directory
- Further spec cleanups

* Mon Jul 13 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.163-2
- Added ExcludeArch: %%{arm}

* Sun Jul 05 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.163-1
- Updated to 0.163
- Cleaned up the spec file further
- Dropped upstreamed patches
- Patched to use system PortAudio
- Added more workarouds for low memory on the builder
- Replaced wildcards with || approach
- Fixed parallel building

* Sun Jun 07 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.162-1
- Updated to 0.162
- Adapted to the new build system
- Cleaned up the .spec file considerably 

* Sun Mar 29 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.160-1
- Updated to 0.160

* Thu Feb 26 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.159-1
- Updated to 0.159
- Updated the verbosebuild patch

* Wed Jan 28 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.158-1
- Updated to 0.158
- Updated the verbosebuild patch
- Patched to make build using system zlib and flac work

* Sat Jan 03 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.157-1
- Updated to 0.157
- Updated the verbosebuild patch

* Thu Nov 27 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.156-1
- Updated to 0.156
- Switched to SDL2

* Tue Nov 04 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.155-2
- Fixed the ini path correctly

* Wed Oct 15 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.155-1
- Updated to 0.155
- Fixed the knock-on effect of changed build order on ini file names
- Use system sqlite3

* Thu Jul 24 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.154-1
- Updated to 0.154
- Changed to build mess before mame

* Mon Apr 14 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.153-1
- Updated to 0.153

* Wed Jan 01 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.152-1
- Updated to 0.152

* Sun Nov 10 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.151-1
- Updated to 0.151
- Updated the verbosebuild patch
- Use system-wide portmidi
- Fedora 17 is long EOL, always use system-wide libjpeg
- Added a conditional N64 SIMD
- Added new man pages
- Only use assembly on supported architectures

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.150-2
- Rebuilt

* Thu Sep 19 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.150-1
- Updated to 0.150
- Fixed the cheatpath

* Wed Jul 24 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.149u1-1
- Updated to 0.149u1

* Tue Jun 11 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.149-1
- Updated to 0.149

* Mon May 20 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.148u5-1
- Updated to 0.148u5

* Tue Apr 30 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.148u4-1
- Updated to 0.148u4

* Tue Apr 09 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.148u3-1
- Updated to 0.148u3

* Tue Mar 19 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.148u2-1
- Updated to 0.148u2
- Switched to the qt debugger and adjusted BR accordingly
- Made it easy to build an svn snapshot

* Mon Feb 11 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.148u1-1
- Updated to 0.148u1
- Use system libjpeg on Fedora 18 too (RH bug #854695)

* Sat Jan 12 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.148-1
- Updated to 0.148

* Mon Dec 17 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.147u4-1
- Updated to 0.147u4
- Updated the lowmem workaround - the linker is not the culprit, dwz is
- BR: libjpeg-devel → libjpeg-turbo-devel
- Updated the verbosebuild patch

* Mon Nov 19 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.147u3-1
- Updated to 0.147u3

* Tue Oct 30 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.147u2-1
- Updated to 0.147u2
- Conditionalised the low memory workaround
- Use system libjpeg-turbo on Fedora 19 and above
- Do not delete the entire obj/, leave the bits needed by the -debuginfo package

* Sat Oct 27 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.147u1-2
- Work around low memory on the RPM Fusion builder

* Mon Oct 08 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.147u1-1
- Updated to 0.147u1
- Dropped missing whatsnew.txt workaround
- Fixed incorrect paths in mess.ini
- Remove the object tree between mame and mess builds to prevent mess using /etc/mame

* Fri Sep 21 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.147-1
- Updated to 0.147
- Merged with mess
- Streamlined the directories installation
- Worked around missing whatsnew.txt
- Fixed mame.6 installation location
- Re-enabled ldplayer
- Cleaned-up ancient Obsoletes/Provides

* Mon Aug 20 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.146u5-1
- Updated to 0.146u5

* Mon Jul 30 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.146u4-1
- Updated to 0.146u4

* Sun Jul 15 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.146u3-1
- Updated to 0.146u3

* Mon Jul 02 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.146u2-1
- Updated to 0.146u2

* Mon Jun 11 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.146u1-1
- Updated to 0.146u1

* Tue May 22 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.146-1
- Updated to 0.146
- Added GLSL shaders to the installed files

* Mon May 07 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145u8-1
- Updated to 0.145u8

* Sun Apr 22 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145u7-1
- Updated to 0.145u7

* Sun Apr 08 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145u6-1
- Updated to 0.154u6
- Dropped the systemlibs patch (no longer necessary)

* Sun Mar 25 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145u5-1
- Updated to 0.145u5
- mame.1 → mame.6

* Sun Mar 11 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145u4-1
- Updated to 0.145u4
- Updated the systemlibs patch (FLAC++ was removed)

* Mon Feb 27 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145u3-1
- Updated to 0.145u3

* Sun Feb 26 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145u2-1
- Updated to 0.145u2
- Re-enabled ldresample and ldverify

* Sun Feb 19 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145u1-1
- Updated to 0.145u1
- Added artwork/* and hlsl/* to the installed files
- Fixed the line ending fix to spare all the *.png files
- Added bundled(libjpeg) and bundled(lzma-sdk) Provides
- Temporarily disabled ldresample and ldverify

* Mon Feb 06 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.145-1
- Updated to 0.145
- Updated the systemlibs patch

* Mon Jan 30 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.144u7-1
- Updated to 0.144u7
- Dropped upstreamed gcc-4.7 patch
- Patched to use system libflac, libjpeg needs more work

* Mon Jan 16 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.144u6-1
- Updated to 0.144u6

* Tue Jan 10 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.144u5-1
- Updated to 0.144u5
- Fixed building with gcc-4.7

* Sun Dec 25 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.144u4-1
- Updated to 0.144u4

* Wed Dec 14 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.144u3-1
- Updated to 0.144u3
- Dropped obsolete Group, Buildroot, %%clean and %%defattr

* Sun Dec 04 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.144u2-1
- Updated to 0.144u2

* Sun Nov 27 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.144u1-1
- Updated to 0.144u1

* Tue Nov 15 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.144-1
- Updated to 0.144
- Fixed whatsnew.txt encoding (cp1252 → utf-8)
- Updated Source0 URL

* Thu Oct 27 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u9-1
- Updated to 0.143u9

* Sun Oct 23 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u8-1
- Updated to 0.143u8

* Tue Oct 11 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u7-1
- Updated to 0.143u7

* Thu Sep 22 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u6-1
- Updated to 0.143u6
- Dropped upstreamed stacksmash patch

* Tue Sep 06 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u5-1
- Updated to 0.143u5
- Fixed stack smash in m68kmake.c

* Thu Aug 25 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u4-1
- Updated to 0.143u4

* Mon Aug 15 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u3-1
- Updated to 0.143u3

* Wed Jul 27 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u2-1
- Updated to 0.143u2

* Fri Jul 15 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143u1-1
- Updated to 0.143u1

* Wed Jun 29 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.143-1
- Updated to 0.143

* Sun Jun 19 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.142u6-1
- Updated to 0.142u6

* Mon Jun 06 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.142u5-1
- Updated to 0.142u5

* Tue May 24 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.142u4-1
- Updated to 0.142u4

* Sun May 08 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.142u3-1
- Updated to 0.142u3
- Disabled ldplayer

* Mon Apr 25 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.142u2-1
- Updated to 0.142u2

* Tue Apr 19 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.142u1-1
- Updated to 0.142u1
- Updated the verbosebuild patch

* Sun Apr 03 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.142-1
- Updated to 0.142

* Fri Mar 25 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.141u4-1
- Updated to 0.141u4
- Re-enabled ldplayer
- Added support for hash files
- Sorted the %%install section alphabetically

* Mon Feb 28 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.141u3-1
- Updated to 0.141u3
- Filtered out redundant $RPM_OPT_FLAGS
- No longer enable joystick by default
- Provided an easy way to disable ldplayer
- Dropped upstreamed gcc-4.6 patch

* Wed Feb 09 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.141u2-1
- Updated to 0.141u2

* Mon Jan 24 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.141u1-1
- Updated to 0.141u1
- Re-enabled the fortify patch
- Fixed building with gcc-4.6

* Thu Jan 13 2011 Julian Sikorski <belegdol@fedoraproject.org> - 0.141-1
- Updated to 0.141
- Temporarily dropped the fortify patch

* Thu Dec 09 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.140u2-1
- Updated to 0.140u2
- Added SDL_ttf-devel to BuildRequires, removed explicit SDL-devel

* Mon Nov 08 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.140u1-1
- Updated to 0.140u1

* Thu Oct 21 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.140-1
- Updated to 0.140
- Re-enabled ldplayer

* Sat Oct 16 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.139u4-1
- Updated to 0.139u4

* Thu Oct 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.139u3-2
- Rebuilt for gcc bug

* Sun Sep 19 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.139u3-1
- Updated to 0.139u3
- Updated the verbosebuild patch

* Tue Aug 31 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.139u2-1
- Updated to 0.139u2

* Fri Aug 13 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.139u1-1
- Updated to 0.139u1

* Thu Jul 29 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.139
- Updated to 0.139

* Thu Jul 22 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.138u4-1
- Updated to 0.138u4
- Install the new manpages

* Thu Jul 08 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.138u3-1
- Updated to 0.138u3
- Updated the verbosebuild patch
- Disabled ldplayer since it does not build ATM (mametesters #3930)

* Thu Jun 17 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.138u2-1
- Updated to 0.138u2
- Adjusted the license tag - it concerns the binary, not the source

* Fri May 28 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.138u1-1
- Updated to 0.138u1

* Sun May 16 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.138-1
- Updated to 0.138

* Wed May 05 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.137u4-1
- Updated to 0137u4

* Thu Apr 22 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.137u3-1
- Updated to 0137u3
- Dropped upstreamed ppc64 patch
- Moved rpm patches application after upstream ones

* Fri Apr 09 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.137u2-1
- Updated to 0137u2

* Sun Mar 21 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.137-4
- Stripped @ from the commands to make the build more verbose

* Sun Mar 21 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.137-3
- Dropped suffix64
- Added ppc64 autodetection support
- Re-diffed the fortify patch

* Sat Mar 20 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0.137-2
- Changed the versioning scheme to include the dot
- Changed the source URL to point to aarongiles.com mirror directly
- Added missing application of the fortify patch
- Added sparc64 and s390 to architectures getting suffix64
- Removed duplicate license.txt

* Thu Mar 11 2010 Julian Sikorski <belegdol@fedoraproject.org> - 0137-1
- Initial package based on sdlmame
