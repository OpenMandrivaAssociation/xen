%define name                    xen
%define xen_version             3.4.0
%define rel                     1
%define xen_release             %mkrel %rel
%define kernel_version          2.6.27.23
%define kernel_tarball_version  2.6.27
%define kernel_extraversion     -xen-%{xen_version}-%{rel}mdv
%define kernel_source_dir       %{kernel_tarball_version}-xen.hg
# ensures file uniqueness
%define kernel_file_string      %{kernel_version}%{kernel_extraversion}
# ensures package uniqueness
%define kernel_package_string   %{kernel_version}%{kernel_extraversion}
%define major                   3.0
%define libname                 %mklibname %{name} %{major}
%define develname               %mklibname %{name} -d

Name:       %{name}
Version:    %{xen_version}
Release:    %{xen_release}
Summary:    The basic tools for managing XEN virtual machines
Group:      System/Kernel and hardware
License:    GPL
Source0:    http://bits.xensource.com/oss-xen/release/%{version}/%{name}-%{version}-xen.tar.gz
Source1:    linux-2.6.27-xen.hg.tar.bz2
Source2:    buildconfigs.tar.bz2
Source3:    xend.init
Source4:    xendomains.init
Source10:   zlib-1.2.3.tar.gz
Source11:   newlib-1.16.0.tar.gz
Source12:   grub-0.97.tar.gz
Source13:   lwip-1.3.0.tar.gz
Source14:   pciutils-2.2.9.tar.bz2
Patch0:     xen-3.3.1-fix-stubdom-Makefile.patch
# fedora patches
Patch11:    xen-initscript.patch
Patch12:    xen-fix-deprecated-warnings.patch
Patch13:    xen-xenstore-cli.patch
Patch14:    xen-dumpdir.patch
Patch15: xen-net-disable-iptables-on-bridge.patch

Patch100:   linux-2.6.27-xen.hg-suse-2.6.27.23.patch
Patch101:   linux-2.6.27-xen.hg-avoid-gcc-optmization.patch
Patch102:   linux-2.6.27-xen.hg-restore-default-mkcompile_h.patch
Patch103:   linux-2.6.27-xen.hg-gcc-4.4-elif-build-fix.patch
Patch104:   linux-2.6.27-xen.hg-gcc-4.4-percpu-build-fix.patch
Patch105:   linux-2.6.27-xen.hg-fix-mmconfig-detection-with-32bit-near-4g.patch
Requires:   python
Requires:   python-twisted-core
Requires:   python-pyxml
Requires:   module-init-tools
Requires:   iptables
Requires:   bridge-utils
Requires:   glibc-xen
Requires:   grub
Requires:   kernel-xen-%{kernel_package_string}
Requires(pre):   kernel-xen-%{kernel_package_string}
BuildRequires:	SDL-devel
BuildRequires:	curl-devel
Buildrequires:	dev86-devel
BuildRequires:  libext2fs-devel
BuildRequires:	ncurses-devel
BuildRequires:	libpython-devel >= 2.4
BuildRequires:	zlib-devel
BuildRequires:  tetex-latex
BuildRequires:  tetex-texi2html
BuildRequires:  pciutils-devel
BuildRequires:  texinfo
Obsoletes:      xen-uptodate
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description 
The basic tools for managing XEN virtual machines.

%package doc
Summary:    XEN documentation
Group:      System/Kernel and hardware
Obsoletes:  xen-uptodate-doc

%description doc
XEN documentation.

%package -n %{libname}
Summary:    Libraries for %{name}
Group:      System/Libraries
Conflicts:  %{name} < 3.1.0-5mdv2008.1

%description -n	%{libname}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%package -n %{develname}
Summary:    Static libraries and header files for %{name}
Group:      Development/C
Requires:	%{libname} = %{xen_version}-%{xen_release}
Provides:	%{name}-devel = %{xen_version}-%{xen_release}
Conflicts:  %name} < 3.1.0-5mdv2008.1

%description -n	%{develname}
This package contains the static development libraries and headers needed
to compile applications linked with Xen libraries.

%package -n kernel-xen-%{kernel_package_string}
Version:    1
Release:    %mkrel 1
Summary:    XEN kernel
Group:      System/Kernel and hardware
Provides:   kernel = %{kernel_version}
Provides:   kernel-xen = %{kernel_version}
Obsoletes:  kernel-xen-uptodate

%description -n kernel-xen-%{kernel_package_string}
XEN kernel.

%package -n kernel-xen-devel-%{kernel_package_string}
Version:    1
Release:    %mkrel 1
Summary:    XEN kernel sources
Group:      System/Kernel and hardware
Requires:   kernel-xen-%{kernel_package_string}
Provides:   kernel-devel = %{kernel_version}
Provides:   kernel-xen-devel = %{kernel_version}
Obsoletes:  kernel-xen-uptodate-devel

%description -n kernel-xen-devel-%{kernel_package_string}
XEN kernel sources.

%prep
%setup -q -n %{name}-%{xen_version}
%setup -q -T -D -a 1 -n %{name}-%{xen_version}
%patch0 -p 1

%patch11 -p 1
%patch12 -p 1
%patch13 -p 1
%patch14 -p 1
%patch15 -p 1

cd linux-%{kernel_source_dir}
tar -jxf %{_sourcedir}/buildconfigs.tar.bz2
extra_version=%{kernel_extraversion}
ln -s linux-defconfig_xen_x86_32 \
      buildconfigs/linux-defconfig_${extra_version#-}_x86_32
ln -s linux-defconfig_xen_x86_64 \
      buildconfigs/linux-defconfig_${extra_version#-}_x86_64
%if %{mdkversion} < 200910
cat << EOF | tee -a buildconfigs/linux-defconfig_xen_x86_32 \
                 >> buildconfigs/linux-defconfig_xen_x86_64
CONFIG_SYSFS_DEPRECATED=y
CONFIG_SYSFS_DEPRECATED_V2=y
CONFIG_USB_DEVICE_CLASS=y
EOF
%endif
%patch100 -p 1
%patch101 -p 1
%patch102 -p 1
%patch103 -p 1
%patch104 -p 1
%patch105 -p 1
cd ..


# install additional sources
cp %{SOURCE10} stubdom
cp %{SOURCE11} stubdom
cp %{SOURCE12} stubdom
cp %{SOURCE13} stubdom
cp %{SOURCE14} stubdom


%build

# clean all stuff
export CFLAGS="$CFLAGS -fno-strict-aliasing"
export HOSTCC="$HOSTCC -fno-strict-aliasing"
export XEN_LINUX_SOURCE=tarball
export KETCHUP=/bin/true
export LINUX_VER=%{kernel_version}
export EXTRAVERSION=%{kernel_extraversion}
export LINUX_SRCDIR=linux-%{kernel_source_dir}
export pae=y 
%make linux-2.6-xen-build < /dev/null
%make -C tools HOTPLUGS=install-udev 
%make -C xen 
%make -C docs 
%make -C stubdom
%ifarch x86_64
%make -C stubdom pv-grub XEN_TARGET_ARCH=x86_32
%endif

%install
rm -rf %{buildroot}
export CFLAGS="$CFLAGS -fno-strict-aliasing"
export DONT_GPRINTIFY=1
export DESTDIR=%{buildroot}
export KETCHUP=/bin/true
export LINUX_VER=%{kernel_version}
export EXTRAVERSION=%{kernel_extraversion}
export LINUX_SRCDIR=linux-%{kernel_source_dir}
export pae=y
make linux-2.6-xen-install
make -C tools install HOTPLUGS=install-udev
make -C xen install
make -C stubdom install
%ifarch x86_64
make -C stubdom install-grub XEN_TARGET_ARCH=x86_32
%endif

# remove additional kernel symlink
rm -f %{buildroot}/boot/vmlinuz-2.6-xen-%{kernel_extra_version}
rm -f %{buildroot}/boot/xen-3.4.gz
rm -f %{buildroot}/boot/xen-3.gz

# drop dangling symlinks
rm -f %{buildroot}/lib/modules/%{kernel_file_string}/{build,source}

# compress modules
find %{buildroot}/lib/modules/%{kernel_file_string} -name "*.ko" | xargs gzip -9
/sbin/depmod -u -ae -b %{buildroot} -r \
    -F %{buildroot}/boot/System.map-%{kernel_file_string} \
    %{kernel_file_string}

# create modules description
pushd %{buildroot}/lib/modules/%{kernel_file_string}
find . -name "*.ko.gz" | xargs /sbin/modinfo | \
    perl -lne 'print "$name\t$1" if $name && /^description:\s*(.*)/; $name = $1 if m!^filename:\s*(.*)\.k?o!; $name =~ s!.*/!!' \
    > modules.description
popd

# remove unwanted firmware files
rm -rf %{buildroot}/lib/firmware

# install kernel sources
install -d -m 755 %{buildroot}%{_prefix}/src
cp -r -L linux-%{kernel_source_dir} \
    %{buildroot}%{_prefix}/src/linux-%{kernel_file_string}

# clean sources from useless source files
pushd %{buildroot}%{_prefix}/src/linux-%{kernel_file_string}
for i in alpha arm arm26 avr32 blackfin cris frv h8300 ia64 m32r mips m68k \
         m68knommu mn10300 parisc powerpc s390 sh sh64 sparc sparc64 v850 xtensa
do
	rm -rf arch/$i
	rm -rf include/asm-$i
done
popd

# fix man pages
install -d -m 755 %{buildroot}%{_mandir}/man{1,5}
install -m 644 docs/man1/* %{buildroot}%{_mandir}/man1
install -m 644 docs/man5/* %{buildroot}%{_mandir}/man5

# install doc manually
rm -rf %{buildroot}%{_docdir}/qemu
install -d -m 755 %{buildroot}%{_docdir}/%{name}
install -m 644 README %{buildroot}%{_docdir}/%{name}
install -m 644 docs/ps/* %{buildroot}%{_docdir}/%{name}
install -m 644 docs/pdf/* %{buildroot}%{_docdir}/%{name}

# install state directory
install -d -m 755 %{buildroot}%{_localstatedir}/lib/xend/{domains,state,storage}
# symlink /var/lib/xend to allow live migration to work
# https://bugs.launchpad.net/ubuntu/+source/xen-3.2/+bug/277132
(cd %{buildroot}%{_localstatedir}/lib && rmdir xen && ln -sf xend xen)

# install our own init scripts
install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{SOURCE3} %{buildroot}%{_initrddir}/xend
install -m 755 %{SOURCE4} %{buildroot}%{_initrddir}/xendomains

# delete original ones
rm -rf %{buildroot}%{_sysconfdir}/init.d

# udev
rm -rf %{buildroot}/etc/udev/rules.d/xen*.rules
mv %{buildroot}/etc/udev/xen*.rules %{buildroot}/etc/udev/rules.d


%check
grep -q "^CONFIG_SQUASHFS=m" %{buildroot}/boot/config-%{kernel_file_string} \
    || exit 0

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post
/sbin/installkernel %{kernel_file_string}

%preun
/sbin/installkernel -R %{kernel_file_string}

%post -n kernel-xen-devel-%{kernel_package_string}
if [ -d /lib/modules/%{kernel_file_string} ]; then
    ln -sTf /usr/src/linux-%{kernel_file_string} /lib/modules/%{kernel_file_string}/build
    ln -sTf /usr/src/linux-%{kernel_file_string} /lib/modules/%{kernel_file_string}/source
fi

%postun -n kernel-xen-devel-%{kernel_package_string}
if [ -L /lib/modules/%{kernel_file_string}/build ]; then
    rm -f /lib/modules/%{kernel_file_string}/build
fi
if [ -L /lib/modules/%{kernel_file_string}/source ]; then
    rm -f /lib/modules/%{kernel_file_string}/source
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/README
%config(noreplace) %{_sysconfdir}/sysconfig/xendomains
%config(noreplace) %{_sysconfdir}/udev/rules.d/xen-backend.rules
%config(noreplace) %{_sysconfdir}/udev/rules.d/xend.rules
%dir %{_sysconfdir}/xen
%{_sysconfdir}/xen/scripts
%{_sysconfdir}/xen/auto
%{_sysconfdir}/xen/qemu-ifup
%{_sysconfdir}/xen/README
%{_sysconfdir}/xen/README.incompatibilities
%config(noreplace) %{_sysconfdir}/xen/*.sxp
%config(noreplace) %{_sysconfdir}/xen/*.xml
%config(noreplace) %{_sysconfdir}/xen/xmexample*
%{_mandir}/man*/*
%{_libdir}/xen
%if "%{_lib}" != "lib"
%{_prefix}/lib/xen
%endif
%{_libdir}/fs
%{py_platsitedir}/xen
%{py_platsitedir}/grub/*
%{py_platsitedir}/fsimage.so
%if %{mdkversion} > 200700
%{py_platsitedir}/pygrub-0.3-py%{pyver}.egg-info
%{py_platsitedir}/xen-3.0-py%{pyver}.egg-info
%endif
%{_datadir}/xen
%{_localstatedir}/lib/xen
%{_localstatedir}/lib/xend
%{_localstatedir}/lib/xenstored
 /var/run/xenstored
/boot/xen*
%{_initrddir}/xend
%{_initrddir}/xendomains
%{_sbindir}/fs-backend
%{_sbindir}/xenstored
%{_sbindir}/xm
%{_sbindir}/xend
%{_sbindir}/xenconsoled
%{_sbindir}/xentop
%{_sbindir}/xen-bugtool
%{_sbindir}/xenbaked
%{_sbindir}/xenmon.py
%{_sbindir}/blktapctrl
%{_sbindir}/img2qcow
%{_sbindir}/qcow-create
%{_sbindir}/qcow2raw
%{_sbindir}/tapdisk
%{_sbindir}/xentrace_setmask
%{_sbindir}/xen-python-path
%{_sbindir}/flask-loadpolicy
%{_sbindir}/xsview
%{_sbindir}/xenperf
%{_sbindir}/xenpm
%{_sbindir}/xenpmd
%{_bindir}/xencons
%{_bindir}/xentrace
%{_bindir}/xentrace_format
%{_bindir}/xentrace_setsize
%{_bindir}/xenstore-*
%{_bindir}/pygrub
%{_bindir}/xen-detect
%{_bindir}/qemu-img-xen
%{_bindir}/qemu-nbd-xen
%{_bindir}/xenstore

%files -n kernel-xen-%{kernel_package_string}
%defattr(-,root,root)
/lib/modules/%{kernel_file_string}
/boot/System.map-%{kernel_file_string}
/boot/config-%{kernel_file_string}
/boot/vmlinuz-%{kernel_file_string}

%files -n kernel-xen-devel-%{kernel_package_string}
%defattr(-,root,root)
%{_prefix}/src/linux-%{kernel_file_string}

%files doc
%defattr(-,root,root)
%{_docdir}/%{name}/*
%exclude %{_docdir}/%{name}/README
%doc docs/ps/* docs/pdf/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/xen
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a
