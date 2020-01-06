# RetroArcade-CentOS
Refer to: https://github.com/TiBeN/15khz-arcade-pkg

-------------------------------------------------------------

## REBUILD GROOVYMAME 0.217 (GCC 8.x)

packages base
```
yum install flac-devel gcc-c++ glm-devel jack-audio-connection-kit libjpeg-turbo-devel libXi-devel libXinerama-devel lua-devel portaudio-devel portmidi-devel pugixml-devel qt5-qtbase-devel rapidjson-devel SDL2_ttf-devel sqlite-devel utf8proc-devel qt5-qtquickcontrols2-devel harfbuzz-devel harfbuzz-icu graphite2-devel libXrandr-devel
```

lua 5.x
```
yum install http://www.nosuchhost.net/~cheese/fedora/packages/epel-7/x86_64/cheese-release-7-1.noarch.rpm
yum install lua-devel
```

python 3.6 / gcc 8.x
```
yum install centos-release-scl
yum install devtoolset-8-gcc devtoolset-8-gcc-c++
yum install rh-python36
```

enable python 3.6/gcc 8.x
```
scl enable devtoolset-8 -- bash
scl enable rh-python36 bash
```

python libraries
```
pip install --upgrade pip
pip install sphinx_rtd_theme
pip install sphinxcontrib-svg2pdfconverter
```

do not parallelize
```
echo "%_smp_mflags -j1" >> ~/.rpmmacros
```

download mame source
```
wget wget -O ~/rpmbuild/SOURCES/mame0217s.exe https://github.com/mamedev/mame/releases/download/mame0217/mame0217s.exe
```

create package
```
rpmbuild -ba ~/rpmbuild/SPECS/groovymame217.spec
```

--------------------

## REBUILD EMULATIONSTATION (GCC 4.x)

packages base
```
yum groupinstall -y "Development Tools"
yum install -y alsa-lib alsa-lib-devel SDL2-devel boost-system boost-filesystem boost-date-time boost-locale freeimage-devel boost-devel freetype-devel eigen3-devel.noarch libcurl-devel mesa-libGL-devel cmake git
```

download source
```
wget -O ~/rpmbuild/SOURCES/EmulationStation.zip https://codeload.github.com/Aloshi/EmulationStation/zip/master
```

build package
```
rpmbuild -ba ~/rpmbuild/SPECS/EmulationStation.spec
```

--------------------------------------

## REBUILD NOUVEAU LOW-RES PATCH (GCC 4.x)

packages base
```
yum install systemd-devel xorg-x11-server-devel libtoo
```

build package
```
rpmbuild -ba ~/rpmbuild/SPECS/xorg-x11-drv-nouveau.spec
```
--------------------------------------

## REBUILD KERNEL WITH LOW RES PATCH (GCC 4.X) [https://github.com/Ansa89/linux-15khz-patch]

packages base
```
yum install perl-interpreter python2-rpm-macros hmaccalc python3-devel devtoolset-8-build devtoolset-8-make python3-rpm-macros bison flex elfutils-devel binutils-devel newt-devel audit-libs-devel java-devel numactl-devel pciutils-devel python-docutils libcap-devel libcap-ng-devel llvm-toolset-7.0 pesign xmlto asciidoc rpm
```

build package
```
rpmbuild -ba ~/rpmbuild/SPECS/kernel.spec
```
