%define	major	0
%define	maj10	1.0
%define	maj30	3.0
%define maj43	4.3
%define	maj45	4.5
%define	libblktapctl	%mklibname blktapctl %{maj10}
%define	libbfsimage	%mklibname bfsimage %{maj10}
%define	libvhd		%mklibname vhd %{maj10}
%define	libxenctrl	%mklibname xenctrl %{maj45}
%define	libxenguest	%mklibname xenguest %{maj45}
%define	libxenlight	%mklibname xenlight %{maj45}
%define	libxenstat	%mklibname xenstat %{major}
%define	libxenstore	%mklibname xenstore %{maj30}
%define	libxenvchan	%mklibname xenvchan %{maj10}
%define	libxlutil	%mklibname xlutil %{maj43}
%define	devname		%mklibname %{name} -d

%define	_disable_ld_no_undefined 1

Summary:	The basic tools for managing XEN virtual machines
Name:		xen
Version:	4.5.0
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://xen.org/
Source0:	http://bits.xensource.com/oss-xen/release/%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}.modules
Source3:	http://xenbits.xen.org/xen-extfiles/libconfig-1.3.2.tar.gz
# stubdoms
Source10:	http://xenbits.xen.org/xen-extfiles/zlib-1.2.3.tar.gz
Source11:	http://xenbits.xen.org/xen-extfiles/newlib-1.16.0.tar.gz
Source12:	http://xenbits.xen.org/xen-extfiles/grub-0.97.tar.gz
Source13:	http://xenbits.xen.org/xen-extfiles/lwip-1.3.0.tar.gz
Source14:	http://xenbits.xen.org/xen-extfiles/pciutils-2.2.9.tar.bz2
Source15:	http://xenbits.xen.org/xen-extfiles/polarssl-1.1.4-gpl.tgz
Source16:	http://xenbits.xen.org/xen-extfiles/ipxe-git-9a93db3f0947484e30e753bbd61a10b17336e20e.tar.gz
Source17:	http://xenbits.xen.org/xen-extfiles/tpm_emulator-0.7.4.tar.gz
Source18:	http://xenbits.xen.org/xen-extfiles/gmp-4.3.2.tar.bz2

# initscripts
Source30:	sysconfig.xenstored
Source31:	sysconfig.xenconsoled
Source33:	%{name}-tmpfiles.conf
Source34:	xen.rpmlintrc
# systemd bits
Source40:	proc-xen.mount
Source41:	var-lib-xenstored.mount
Source42:	xenstored.service
Source45:	xenconsoled.service
Source46:	xen-watchdog.service
Source47:	xendomains.service
Source48:	libexec.xendomains
Source50:	oxenstored.service

# Mageia patches:
Patch0:		xen-4.1.2-fix-stubdom-Makefile.patch
Patch2:		xen-4.1.3-fix-doc-build.patch
Patch3:		xen-4.2.1-fix-glibc-build.patch
Patch4:		xencommons-fix-service.patch
Patch5:		xen-4.2-ocaml-build.patch
# Openmandriva patches
Patch6:		xen-4.4.1-gold.patch
%if %mdvver >= 201500
# we need to allow the module to be built with clang
Patch7:		xen-4.4.1-pybuild.patch
%endif
Patch8:		xen.ocaml.uint.fix.patch
# fedora patches

# documentation
BuildRequires:	ghostscript
BuildRequires:	transfig
BuildRequires:	texinfo
BuildRequires:	texlive-latex
BuildRequires:	texlive-dvips
BuildRequires:	ocaml
BuildRequires:	ocaml-findlib-devel
BuildRequires:	iasl
BuildRequires:	gettext
BuildRequires:	git
BuildRequires:	brlapi-devel
BuildRequires:	bzip2-devel
BuildRequires:	dev86-devel
BuildRequires:	libaio-devel
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(libconfig)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libidn)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(python) >= 2.4
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(yajl)
BuildRequires:	pkgconfig(zlib)
Requires:	bridge-utils
#Requires:	glibc-xen
Requires:	grub
Requires:	iptables
#Requires:	kernel-xen-pvops
Requires:	kmod
Requires:	python
Requires:	python-twisted-core
Requires:	python-lxml
Requires:	xen-hypervisor = %{EVRD}

%description
The basic tools for managing XEN virtual machines.

%files
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/README
%{_sysconfdir}/bash_completion.d/xl.sh
%config(noreplace) %{_udevrulesdir}/*
%dir %{_sysconfdir}/xen
%{_sysconfdir}/xen/scripts
%{_sysconfdir}/xen/auto
%config(noreplace) %{_sysconfdir}/xen/xlexample*
%config(noreplace) %{_sysconfdir}/xen/cpupool
%config(noreplace) %{_sysconfdir}/xen/xl.conf
%config(noreplace) %{_sysconfdir}/xen/oxenstored.conf
%{_mandir}/man*/*
%{_libexecdir}/xen
%{_libdir}/fs
%if %mdvver >= 201500
%{py2_platsitedir}/xen
%{py2_platsitedir}/grub/*
%{py2_platsitedir}/fsimage.so
%{py2_platsitedir}/pygrub-0.3-py%{py2_ver}.egg-info
%{py2_platsitedir}/xen-3.0-py%{py2_ver}.egg-info
%else
%{py_platsitedir}/xen
%{py_platsitedir}/grub/*
%{py_platsitedir}/fsimage.so
%{py_platsitedir}/pygrub-0.3-py%{py_ver}.egg-info
%{py_platsitedir}/xen-3.0-py%{py_ver}.egg-info
%endif

%{_datadir}/xen
# general xen state
%{_localstatedir}/lib/xen
%{_localstatedir}/lib/xend
# xenstore state
%{_localstatedir}/lib/xenstored
# init scripts
%{_unitdir}/xendomains.service
%{_libexecdir}/xendomains
%{_unitdir}/proc-xen.mount
%{_unitdir}/var-lib-xenstored.mount
%{_unitdir}/xenstored.service
%{_unitdir}/oxenstored.service
%{_unitdir}/xenconsoled.service
%{_unitdir}/xen-watchdog.service
%{_unitdir}/xen-init-dom0.service
%{_unitdir}/xen-qemu-dom0-disk-backend.service
%{_unitdir}/xenstored.socket
%{_unitdir}/xenstored_ro.socket
/usr/lib/modules-load.d/xen.conf
%{_sysconfdir}/sysconfig/modules/xen.modules
%config(noreplace) %{_sysconfdir}/sysconfig/xendomains
%config(noreplace) %{_sysconfdir}/sysconfig/xenstored
%config(noreplace) %{_sysconfdir}/sysconfig/xenconsoled
%config(noreplace) %{_sysconfdir}/sysconfig/xencommons
%config(noreplace) %{_sysconfdir}/logrotate.d/xen
%{_tmpfilesdir}/%{name}.conf
%{_bindir}/pygrub
%{_bindir}/qemu-img-xen
%{_bindir}/qemu-nbd-xen
%{_bindir}/xencons
%{_bindir}/xentrace
%{_bindir}/xentrace_format
%{_bindir}/xentrace_setsize
%{_bindir}/xenstore-*
%{_bindir}/xen-detect
%{_bindir}/xenstore
%{_sbindir}/xenstored
%{_sbindir}/xenconsoled
%{_sbindir}/xentop
%{_sbindir}/xen-bugtool
%{_sbindir}/xenbaked
%{_sbindir}/xenmon.py
%{_sbindir}/img2qcow
%{_sbindir}/qcow-create
%{_sbindir}/qcow2raw
%{_sbindir}/xentrace_setmask
%{_sbindir}/xenperf
%{_sbindir}/xenpm
%{_sbindir}/xenpmd
%{_sbindir}/xen-mfndump
%{_bindir}/xencov_split
%{_sbindir}/xencov
%{_sbindir}/gdbsx
%{_sbindir}/gtracestat
%{_sbindir}/gtraceview
%{_sbindir}/kdd
%{_sbindir}/lock-util
%{_sbindir}/oxenstored
%{_sbindir}/tap-ctl
%{_sbindir}/tapdisk-client
%{_sbindir}/tapdisk-diff
%{_sbindir}/tapdisk-stream
%{_sbindir}/tapdisk2
%{_sbindir}/td-util
%{_sbindir}/vhd-update
%{_sbindir}/vhd-util
%{_sbindir}/xenlockprof
%{_sbindir}/xenwatchdogd
%{_sbindir}/xen-hvmctx
%{_sbindir}/xen-tmem-list-parse
%{_sbindir}/xen-lowmemd
%{_sbindir}/xen-ringwatch
%{_sbindir}/xen-hptool
%{_sbindir}/xen-hvmcrash
%{_sbindir}/xl

%post
%tmpfiles_create %{name}
%_post_service xencommons
%_post_service xendomains

%preun
%_preun_service xencommons
%_preun_service xendomains

#----------------------------------------------------------------------------

%package -n	ocaml-xen
Summary:	OCaml bindings for Xen
Group:		Development/Other

%description -n ocaml-xen
This package contains the Ocaml bindings for Xen.

%files -n ocaml-xen
%{_libdir}/ocaml/

#----------------------------------------------------------------------------

%package hypervisor
Summary:	Libraries for Xen tools
Group:		System/Kernel and hardware

%description hypervisor
This package contains the Xen hypervisor.

%files hypervisor
%ifarch %{ix86}
%doc README.4.3.0.upgrade.urpmi README.install.urpmi
%else
/boot/xen-syms-*
/boot/xen-*.gz
/boot/xen.gz
%endif

#----------------------------------------------------------------------------

%package doc
Summary:	XEN documentation
Group:		System/Kernel and hardware

%description doc
XEN documentation.

%files doc
%{_docdir}/%{name}/*
%exclude %{_docdir}/%{name}/README

#----------------------------------------------------------------------------

%package -n %{libblktapctl}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libblktapctl}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%files -n %{libblktapctl}
%{_libdir}/libblktapctl.so.%{maj10}*

#----------------------------------------------------------------------------

%package -n %{libbfsimage}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libbfsimage}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%files -n %{libbfsimage}
%{_libdir}/libfsimage.so.%{maj10}*

#----------------------------------------------------------------------------

%package -n %{libvhd}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libvhd}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%files -n %{libvhd}
%{_libdir}/libvhd.so.%{maj10}*

#----------------------------------------------------------------------------

%package -n %{libxenctrl}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libxenctrl}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%files -n %{libxenctrl}
%{_libdir}/libxenctrl.so.%{maj45}*

#----------------------------------------------------------------------------

%package -n %{libxenguest}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libxenguest}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%files -n %{libxenguest}
%{_libdir}/libxenguest.so.%{maj45}*

#----------------------------------------------------------------------------

%package -n %{libxenlight}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libxenlight}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%files -n %{libxenlight}
%{_libdir}/libxenlight.so.%{maj45}*

#----------------------------------------------------------------------------

%package -n %{libxenstat}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libxenstat}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%files -n %{libxenstat}
%{_libdir}/libxenstat.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libxenstore}
Summary:	Libraries for %{name}
Group:		System/Libraries
Obsoletes:	%{_lib}xen3.0 < 4.2.1-1
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libxenstore}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%files -n %{libxenstore}
%{_libdir}/libxenstore.so.%{maj30}*

#----------------------------------------------------------------------------

%package -n %{libxenvchan}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libxenvchan}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%files -n %{libxenvchan}
%{_libdir}/libxenvchan.so.%{maj10}*

#----------------------------------------------------------------------------

%package -n %{libxlutil}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libxlutil}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%files -n %{libxlutil}
%{_libdir}/libxlutil.so.%{maj43}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development libraries and header files for %{name}
Group:		Development/C
Requires:	%{libblktapctl} = %{EVRD}
Requires:	%{libbfsimage} = %{EVRD}
Requires:	%{libvhd} = %{EVRD}
Requires:	%{libxenctrl} = %{EVRD}
Requires:	%{libxenguest} = %{EVRD}
Requires:	%{libxenlight} = %{EVRD}
Requires:	%{libxenstat} = %{EVRD}
Requires:	%{libxenstore} = %{EVRD}
Requires:	%{libxenvchan} = %{EVRD}
Requires:	%{libxlutil} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This package contains the development libraries and headers needed
to compile applications linked with Xen libraries.

%files -n %{devname}
%{_includedir}/xen
%{_includedir}/xenstore-compat
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a

#----------------------------------------------------------------------------

%prep
%setup -q
%apply_patches

# stub domain
cp %{SOURCE10} stubdom
cp %{SOURCE11} stubdom
cp %{SOURCE12} stubdom
cp %{SOURCE13} stubdom
cp %{SOURCE14} stubdom
cp %{SOURCE15} stubdom
cp %{SOURCE17} stubdom
cp %{SOURCE18} stubdom

cp %{SOURCE16} tools/firmware/etherboot/ipxe.tar.gz

%build
mkdir -p bfd
ln -sf $(which ld.bfd) bfd/ld
export PATH="$PWD/bfd:$PATH"
export PYTHON=%{__python2}
export CFLAGS="%{optflags}"
# set to clang for the configure script
export CC=%__cc
export CXX=%__cxx
%ifnarch %{ix86}
%make prefix=/usr dist-xen
%endif
sed -E -i 's/(as_fn_error \$\? "cannot find wget or ftp" "\$LINENO" 5)/as_fn_status $?/' tools/configure
sed -E -i 's/(as_fn_error \$\? "cannot find wget or ftp" "\$LINENO" 5)/as_fn_status $?/' stubdom/configure

./configure --disable-seabios --build=%{_target_platform} \
        --prefix=%{_prefix} \
        --exec-prefix=%{_exec_prefix} \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir} \
        --sysconfdir=%{_sysconfdir} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libexecdir} \
        --localstatedir=%{_localstatedir} \
        --sharedstatedir=%{_sharedstatedir} \
        --mandir=%{_mandir} \
        --infodir=%{_infodir} \
	--with-system-qemu \
	--with-systemd=%{_unitdir}

%make prefix=/usr dist-tools
make  prefix=/usr dist-docs

unset CFLAGS
make dist-stubdom

%install
export PATH="$PWD/bfd:$PATH"

%ifarch %{ix86}
cat > README.install.urpmi <<_EOF
Since xen 4.3, the hypervisor is no longer supported on x86_32. But fear not,
you can actually use the x86_64 xen hypervisor, even when using a 32bit kernel
and system. This is because the hypervisor is loaded before the kernel and OS.
Keep in mind that a x86_64 capable processor is still required, but then if
you are installing a hypervisor, you really should be using 64bit anyway.
_EOF
ln README.install.urpmi README.4.3.0.upgrade.urpmi
%else
make DESTDIR=%{buildroot} prefix=/usr install-xen
%endif

make DESTDIR=%{buildroot} prefix=/usr install-tools
make DESTDIR=%{buildroot} prefix=/usr install-docs
make DESTDIR=%{buildroot} prefix=/usr install-stubdom

# stubdom: newlib
rm -rf %{buildroot}/usr/*-xen-elf

# remove additional kernel symlink
rm -f %{buildroot}/boot/xen-3.4.gz
rm -f %{buildroot}/boot/xen-3.gz

# remove unwanted firmware files
rm -rf %{buildroot}/lib/firmware

# remove pointless helper
rm -f %{buildroot}%{_sbindir}/xen-python-path

# remove  README's not intended for end users
rm -f %{buildroot}/%{_sysconfdir}/xen/README*

# fix man pages
install -d -m 755 %{buildroot}%{_mandir}/man{1,5}
install -m 644 docs/man/*.1 %{buildroot}%{_mandir}/man1
install -m 644 docs/man/*.5 %{buildroot}%{_mandir}/man5

# install doc manually
rm -rf %{buildroot}%{_docdir}/qemu
install -d -m 755 %{buildroot}%{_docdir}/%{name}
install -m 644 README %{buildroot}%{_docdir}/%{name}
install -d -m 755 %{buildroot}%{_docdir}/%{name}/txt
install -d -m 755 %{buildroot}%{_docdir}/%{name}/html
cp -R docs/txt/* %{buildroot}%{_docdir}/%{name}/txt/
cp -R docs/html/* %{buildroot}%{_docdir}/%{name}/html/

# install log directory
install -d -m 755 %{buildroot}%{_localstatedir}/log/xen

# install state directory
install -d -m 755 %{buildroot}%{_localstatedir}/lib/xend/{domains,state,storage}

# remove old init scripts
rm %{buildroot}%{_sysconfdir}/rc.d/init.d/xen-watchdog
rm %{buildroot}%{_sysconfdir}/rc.d/init.d/xencommons
rm %{buildroot}%{_sysconfdir}/rc.d/init.d/xendomains

# sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE30} %{buildroot}%{_sysconfdir}/sysconfig/xenstored
install -m 644 %{SOURCE31} %{buildroot}%{_sysconfdir}/sysconfig/xenconsoled

mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE40} %{buildroot}%{_unitdir}/proc-xen.mount
install -m 644 %{SOURCE41} %{buildroot}%{_unitdir}/var-lib-xenstored.mount
install -m 644 %{SOURCE42} %{buildroot}%{_unitdir}/xenstored.service
install -m 644 %{SOURCE45} %{buildroot}%{_unitdir}/xenconsoled.service
install -m 644 %{SOURCE46} %{buildroot}%{_unitdir}/xen-watchdog.service
install -m 644 %{SOURCE47} %{buildroot}%{_unitdir}/xendomains.service
mkdir -p %{buildroot}%{_libexecdir}
install -m 755 %{SOURCE48} %{buildroot}%{_libexecdir}/xendomains
mkdir -p %{buildroot}/usr/lib/tmpfiles.d
install -m 644 %{SOURCE50} %{buildroot}%{_unitdir}/oxenstored.service

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/modules
install -m 755 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/sysconfig/modules/%{name}.modules 

# tmpfiles
install -D -p -m 0644 %{SOURCE33} %{buildroot}%{_tmpfilesdir}/%{name}.conf

# udev
#rm -rf %{buildroot}/etc/udev/rules.d/xen*.rules
#mv %{buildroot}/etc/udev/rules.d/xen*.rules %{buildroot}/etc/udev/rules.d
mkdir -p %{buildroot}%{_udevrulesdir}
mv %{buildroot}%{_sysconfdir}/udev/rules.d/xen*.rules %{buildroot}%{_udevrulesdir}

# move ocaml stubs to correct dir
mkdir -p %{buildroot}%{_libdir}/ocaml/stublibs/
mv %{buildroot}%{_libdir}/ocaml/*/dll*_stubs.so %{buildroot}%{_libdir}/ocaml/stublibs/

# logrotate
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
cat > %{buildroot}%{_sysconfdir}/logrotate.d/xen <<EOF
/var/log/xen/xend-debug.log /var/log/xen/xen-hotplug.log
/var/log/xen/domain-builder-ng.log {
    notifempty
    missingok
    copytruncate
}
EOF

# standard gnu info files
rm -rf %{buildroot}/usr/info

# gprintify has a bug handling some constructs in xendomain
export DONT_GPRINTIFY=1

