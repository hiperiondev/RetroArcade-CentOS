# RetroArcade-CentOS

PRECOMPILED PACKAGES: https://mega.nz/#F!tyYRFQpR!3zIwc-7gRe3li1hJJU0suw

Refer to: https://github.com/TiBeN/15khz-arcade-pkg

-------------------------------------------------------------

## REBUILD GROOVYMAME 0.219 (GCC 8.x)

packages base
```
yum install flac-devel gcc-c++ glm-devel jack-audio-connection-kit libjpeg-turbo-devel libXi-devel libXinerama-devel lua-devel portaudio-devel portmidi-devel pugixml-devel qt5-qtbase-devel rapidjson-devel SDL2_ttf-devel sqlite-devel utf8proc-devel qt5-qtquickcontrols2-devel harfbuzz-devel harfbuzz-icu graphite2-devel libXrandr-devel expat-devel fontconfig-devel zlib-devel
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
wget -O ~/rpmbuild/SOURCES/mame0219s.exe https://github.com/mamedev/mame/releases/download/mame0219/mame0219s.exe
```

create package
```
rpmbuild -ba ~/rpmbuild/SPECS/groovymame219.spec
```

--------------------

## REBUILD EMULATIONSTATION (GCC 8.x) [from RetroPie]

packages base
```
yum groupinstall -y "Development Tools"
yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum install https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm

yum install -y alsa-lib alsa-lib-devel SDL2-devel boost-system boost-filesystem boost-date-time boost-locale freeimage-devel boost-devel freetype-devel eigen3-devel.noarch libcurl-devel mesa-libGL-devel cmake git vlc-devel rapidjson-devel

yum install centos-release-scl
yum install devtoolset-8-gcc devtoolset-8-gcc-c++
scl enable devtoolset-8 -- bash
```

download source
```
cd ~/rpmbuild/SOURCES/
git clone --recursive https://github.com/RetroPie/EmulationStation.git

cat EmulationStation/CMake/Packages/FindRapidJSON.cmake | iconv -f utf-8 -t ascii//TRANSLIT > EmulationStation/CMake/Packages/FindRapidJSON.cmake

mv EmulationStation EmulationStation-master
zip -r EmulationStation EmulationStation-master
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
--------------------------------------

## PROBLEMS/ERRORS

### Gamepad not detected:

Create a file /etc/udev/rules.d/99-gamepad.rules with the content
```
SUBSYSTEM=="input", ATTRS{name}=="NAME OF DEVICE", MODE="0666", ENV{ID_INPUT_JOYSTICK}="1"
```
Replacing NAME OF DEVICE with the fullname - that will show in dmesg eg:
```
hid-generic 0003:0583:2060.0006: input,hidraw2: USB HID v1.10 Joystick [USB,2-axis 8-button gamepad] on usb-3f980000.usb-1.5/
```
In this case it would be ATTRS{name}=="USB,2-axis 8-button gamepad"

