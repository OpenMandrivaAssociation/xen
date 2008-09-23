%define name            xen
%define xen_version             3.3.0
%define rel                     2
%define xen_release             %mkrel %rel
%define kernel_version          2.6.18.8
%define kernel_tarball_version  2.6.18
%define kernel_extraversion     -xen-%{xen_version}-%{rel}mdv
%define kernel_source_dir       %{kernel_tarball_version}-xen-3.3.0
# ensures file uniqueness
%define kernel_file_string      %{kernel_version}%{kernel_extraversion}
# ensures package uniqueness
%define kernel_package_string   %{kernel_version}%{kernel_extraversion}
%define major           3.0
%define libname         %mklibname %{name} %{major}
%define develname	    %mklibname %{name} -d

Name:       %{name}
Version:    %{xen_version}
Release:    %{xen_release}
Summary:    The basic tools for managing XEN virtual machines
Group:      System/Kernel and hardware
License:    GPL
Source0:    %{name}-%{version}.tar.gz
Source1:    bash-completion
Source2:    linux-2.6.18-xen-3.3.0.tar.gz
Source3:    xend.init
Source4:    xendomains.init
Patch1:     xen-3.2.0-bnx2-1.4.51b.patch
Patch3:     xen-3.2.0-squashfs.patch
Patch4:     xen-3.2.0-use-same-arch-default-config.patch
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
Release:    %mkrel 2
Summary:    XEN kernel
Group:      System/Kernel and hardware
Provides:   kernel = %{kernel_version}
Provides:   kernel-xen = %{kernel_version}
Obsoletes:  kernel-xen-uptodate

%description -n kernel-xen-%{kernel_package_string}
XEN kernel.

%package -n kernel-xen-devel-%{kernel_package_string}
Version:    1
Release:    %mkrel 2
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
%setup -q -T -D -a 2 -n %{name}-%{xen_version}

cd linux-%{kernel_source_dir}
%patch1 -p 1
%patch3 -p 1
%patch4 -p 1

# configure kernel
%ifarch x86_64
    %define kernel_config_file linux-defconfig_xen_x86_64
%else
    %define kernel_config_file linux-defconfig_xen_x86_32
%endif
perl -pi -e 's/^CONFIG_BLK_DEV_LOOP=.*/CONFIG_BLK_DEV_LOOP=m/' \
    buildconfigs/%{kernel_config_file}

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
make linux-2.6-xen-build < /dev/null
%make -C tools
%make -C xen
%make -C docs


%install
rm -rf %{buildroot}
export DONT_GPRINTIFY=1
export DESTDIR=%{buildroot}
#export XEN_LINUX_SOURCE=tarball
export KETCHUP=/bin/true
export LINUX_VER=%{kernel_version}
export EXTRAVERSION=%{kernel_extraversion}
export LINUX_SRCDIR=linux-%{kernel_source_dir}
export pae=y
make linux-2.6-xen-install
make -C tools install
make -C xen install

# remove additional kernel symlink
rm -f %{buildroot}/boot/vmlinuz-2.6-xen-%{kernel_extra_version}

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

# install kernel sources
install -d -m 755 %{buildroot}%{_prefix}/src
cp -r -L linux-%{kernel_source_dir} \
    %{buildroot}%{_prefix}/src/linux-%{kernel_file_string}

# clean sources from useless source files
pushd %{buildroot}%{_prefix}/src/linux-%{kernel_file_string}
for i in alpha arm arm26 avr32 blackfin cris frv h8300 ia64 mips m32r m68k m68knommu parisc powerpc ppc s390 sh sh64 v850 xtensa; do
	rm -rf arch/$i
	rm -rf include/asm-$i
done

%ifnarch %{ix86} x86_64
	rm -rf arch/i386
	rm -rf arch/x86_64
	rm -rf include/asm-i386
	rm -rf include/asm-x86_64
%endif
%ifnarch sparc sparc64
	rm -rf arch/sparc
	rm -rf arch/sparc64
	rm -rf include/asm-sparc
	rm -rf include/asm-sparc64
%endif
popd

# fix man pages
install -d -m 755 %{buildroot}%{_mandir}/man{1,5}
install -m 644 docs/man1/* %{buildroot}%{_mandir}/man1
install -m 644 docs/man5/* %{buildroot}%{_mandir}/man5

# bash completion
install -m 755 -d %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/bash_completion.d/xen

# install doc manually
rm -rf %{buildroot}%{_docdir}/qemu
install -d -m 755 %{buildroot}%{_docdir}/%{name}
install -m 644 README %{buildroot}%{_docdir}/%{name}
install -m 644 docs/ps/* %{buildroot}%{_docdir}/%{name}
install -m 644 docs/pdf/* %{buildroot}%{_docdir}/%{name}

# install state directory
install -d -m 755 %{buildroot}%{_localstatedir}/lib/xend/{domains,state,storage}

# install our own init scripts
install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{SOURCE3} %{buildroot}%{_initrddir}/xend
install -m 755 %{SOURCE4} %{buildroot}%{_initrddir}/xendomains

# delete original ones
rm -rf %{buildroot}%{_sysconfdir}/init.d

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
%config(noreplace) %{_sysconfdir}/hotplug/xen-backend.agent
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
%{_libdir}/python/xen
%{_libdir}/python/grub/*
%{_libdir}/python/fsimage.so
%if %{mdkversion} > 200700
%{_libdir}/python/pygrub-0.3-py2.5.egg-info
%{_libdir}/python/xen-3.0-py2.5.egg-info
%endif
%{_datadir}/xen
%{_localstatedir}/lib/xend
%{_localstatedir}/lib/xenstored
 /var/run/xenstored
/boot/xen*
%{_initrddir}/xend
%{_initrddir}/xendomains
%{_sbindir}/fs-backend
%{_sbindir}/xenstored
%{_sbindir}/netfix
%{_sbindir}/xm
%{_sbindir}/xend
%{_sbindir}/xenperf
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
%{_bindir}/xenperf
%{_bindir}/xencons
%{_bindir}/xentrace
%{_bindir}/xentrace_format
%{_bindir}/xentrace_setsize
%{_bindir}/xenstore-*
%{_bindir}/pygrub
%{_bindir}/xen-detect
%{_bindir}/qemu-img-xen
%{_bindir}/xenstore
%{_sysconfdir}/bash_completion.d/xen

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
