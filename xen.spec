%define name            xen
%define kernel_version  2.6.18

Name:       %{name}
Version:    3.1.0
Release:    %mkrel 4
Summary:    The basic tools for managing XEN virtual machines
Group:      System/Kernel and hardware
License:    GPL
Source0:    %{name}-%{version}-src.tgz
Source1:    bash-completion
Source2:    linux-%{kernel_version}.tar.bz2
Patch0:     xen-3.1-fix-default-interface.patch
Patch1:     xen-3.1.0-bnx2-1.4.51b.patch
Patch2:     xen-3.1.0-memcmp.patch
Patch3:     xen-3.1.0-squashfs.patch
# CVE-2007-1321
Patch401:   xen-qemu-ne2000-CVE-2007-1321.patch
# CVE-2007-4993
Patch402:   pygrub-dont-exec.patch
Requires:   python-twisted-core
Requires:   python
Requires:   module-init-tools
Requires:   iptables
Requires:   bridge-utils
Requires:   glibc-xen
Requires:   grub
Requires:   kernel-xen = %{version}
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

%package -n kernel-xen
Summary:    XEN kernel
Group:      System/Kernel and hardware
Provides:   kernel = %{kernel_version}
Requires(post):	xen
Obsoletes:  kernel-xen-uptodate

%description -n kernel-xen
XEN kernel.

%package -n kernel-xen-devel
Summary:    XEN kernel sources
Group:      System/Kernel and hardware
Requires:   kernel-xen = %{version}
Provides:   kernel-devel = %{kernel_version}
Obsoletes:  kernel-xen-uptodate-devel

%description -n kernel-xen-devel
XEN kernel sources.

%package doc
Summary:    XEN documentation
Group:      System/Kernel and hardware
Obsoletes:  xen-uptodate-doc

%description doc
XEN documentation.

%prep
%setup -q -n %{name}-%{version}-src
%patch0 -p 1
%patch1 -p 1
%patch2 -p 0
%patch3 -p 1

%patch401 -p 1
%patch402 -p 1

%build

# clean all stuff
export CFLAGS="$CFLAGS -fno-strict-aliasing"
export HOSTCC="$HOSTCC -fno-strict-aliasing"
export LINUX_SRC_PATH=$RPM_SOURCE_DIR
export pae=y
%make kernels
%make -C tools
%make -C xen
%make -C docs


%install
rm -rf %{buildroot}
export DONT_GPRINTIFY=1
export pae=y
export DESTDIR=%{buildroot}
make linux-2.6-xen-install
make -C tools install
make -C xen install

# drop dangling symlinks
rm -f %{buildroot}/lib/modules/*/{build,source}

# install kernel sources
install -d -m 755 %{buildroot}%{_prefix}/src
cp -r -L linux-2.6.18-xen %{buildroot}%{_prefix}/src/linux-%{kernel_version}-xen

# clean sources from useless source files
pushd %{buildroot}%{_prefix}/src/linux-%{kernel_version}-xen
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
install -m 644 tools/ioemu/*.html %{buildroot}%{_docdir}/%{name}
install -m 644 docs/ps/* %{buildroot}%{_docdir}/%{name}
install -m 644 docs/pdf/* %{buildroot}%{_docdir}/%{name}

# install state directory
install -d -m 755 %{buildroot}%{_localstatedir}/xend/{domains,state,storage}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n kernel-xen
/sbin/installkernel -L %{kernel_version}-xen

%post -n kernel-xen-devel
if [ -d /lib/modules/%{kernel_version}-xen ]; then
    ln -sf /usr/src/linux-%{kernel_version}-xen /lib/modules/%{kernel_version}-xen/build
    ln -sf /usr/src/linux-%{kernel_version}-xen /lib/modules/%{kernel_version}-xen/source
fi

%postun -n kernel-xen-devel
if [ -L /lib/modules/%{kernel_version}-xen/build ]; then
    rm -f /lib/modules/%{kernel_version}-xen/build
fi
if [ -L /lib/modules/%{kernel_version}-xen/source ]; then
    rm -f /lib/modules/%{kernel_version}-xen/source
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/README
%config(noreplace) %{_sysconfdir}/sysconfig/xendomains
%config(noreplace) %{_sysconfdir}/udev/rules.d/xen-backend.rules
%config(noreplace) %{_sysconfdir}/udev/xen-backend.rules
%dir %{_sysconfdir}/xen
%{_sysconfdir}/xen/scripts
%{_sysconfdir}/xen/auto
%{_sysconfdir}/xen/qemu-ifup
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
%{_libdir}/libxenstore*
%{_libdir}/libxenctrl*
%{_libdir}/libxenguest*
%{_libdir}/libblktap*
%{_libdir}/libfsimage*
%{_datadir}/xen
%{_localstatedir}/xend
%{_localstatedir}/xenstored
 /var/run/xenstored
/boot/xen*
%{_includedir}/xen
%{_includedir}/*.h
%{_sysconfdir}/init.d/xend
%{_sysconfdir}/init.d/xendomains
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
%{_bindir}/xenperf
%{_bindir}/xencons
%{_bindir}/lomount
%{_bindir}/xentrace
%{_bindir}/xentrace_format
%{_bindir}/xentrace_setsize
%{_bindir}/xenstore-*
%{_bindir}/pygrub
%{_bindir}/xen-detect
%{_sysconfdir}/bash_completion.d/xen

%files -n kernel-xen
%defattr(-,root,root)
/boot/*-xen
/lib/modules/%{kernel_version}-xen

%files -n kernel-xen-devel
%defattr(-,root,root)
%{_prefix}/src/linux-%{kernel_version}-xen

%files doc
%defattr(-,root,root)
%{_docdir}/%{name}/*
%exclude %{_docdir}/%{name}/README
%doc docs/ps/* docs/pdf/* tools/ioemu/*.html
