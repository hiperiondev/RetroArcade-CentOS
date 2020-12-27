#The debug build is disabled by default, please use # --with debug to override
%bcond_with debug

%global baseversion 226
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
Patch2:         0226_groovymame_017s.diff
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
Requires:       %{name}-data = %{version}-%{release}

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