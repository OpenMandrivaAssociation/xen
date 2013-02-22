%define	major	0
%define	maj10	1.0
%define	maj20	2.0
%define	maj30	3.0
%define	maj42	4.2
%define	libblktap	%mklibname blktap %{maj30}
%define libblktapctl	%mklibname blktapctl %{maj10}
%define libbfsimage	%mklibname bfsimage %{maj10}
%define libvhd		%mklibname vhd %{maj10}
%define libxenctrl	%mklibname xenctrl %{maj42}
%define libxenguest	%mklibname xenguest %{maj42}
%define libxenlight	%mklibname xenlight %{maj20}
%define libxenstat	%mklibname xenstat %{major}
%define	libxenstore	%mklibname xenstore %{maj30}
%define libxenvchan	%mklibname xenvchan %{maj10}
%define libxlutil	%mklibname xlutil %{maj10}
%define devname		%mklibname %{name} -d
%define pyver	%(rpm -q --qf '%%{VERSION}' python |cut -d. -f1-2)

Summary:	The basic tools for managing XEN virtual machines
Name:		xen
Version:	4.2.1
Release:	1
Group:		System/Kernel and hardware
License:	GPLv2+
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
Source15:	http://caml.inria.fr/pub/distrib/ocaml-3.11/ocaml-3.11.0.tar.gz
Source16:	http://xenbits.xen.org/xen-extfiles/ipxe-git-9a93db3f0947484e30e753bbd61a10b17336e20e.tar.gz
# initscripts
Source20:	init.xenstored 
Source21:	init.xenconsoled
Source22:	init.blktapctrl
Source23:	init.xend
Source30:	sysconfig.xenstored
Source31:	sysconfig.xenconsoled
Source32:	sysconfig.blktapctrl
# Make sure we pass rpmlint checks
Source100:	xen.rpmlintrc
Patch0:		xen-4.1.2-fix-stubdom-Makefile.patch
Patch2:		xen-4.1.3-fix-doc-build.patch
Patch3:		xen-4.2.1-fix-glibc-build.patch
# fedora patches
Patch12:	xen-4.0.1-gcc451.patch
Patch13:	qemu-xen.tradonly.patch
Patch14:	xen-4.2.1-fix-xg-build.patch
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
Buildrequires:	dev86-devel
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
Requires:	glibc-xen
Requires:	grub
Requires:	iptables
Requires:	kernel-xen-pvops
Requires:	kmod
Requires:	python
Requires:	python-twisted-core
Requires:	python-pyxml
Requires:	xen-hypervisor = %{version}

%description 
The basic tools for managing XEN virtual machines.

%package ocaml
Summary:	OCaml bindings for Xen
Group:		Development/Other

%description ocaml
This package contains the Ocaml bindings for Xen

%package hypervisor
Summary:	Libraries for Xen tools
Group:		System/Kernel and hardware

%description hypervisor
This package contains the Xen hypervisor

%package doc
Summary:	XEN documentation
Group:		System/Kernel and hardware

%description doc
XEN documentation.

%package -n %{libblktapctl}
Summary:	Libraries for %{name}
Group:		System/Libraries
Obsoletes:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libblktapctl}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%package -n %{libblktap}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libblktap}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%package -n %{libbfsimage}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libbfsimage}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%package -n %{libvhd}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libvhd}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%package -n %{libxenctrl}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libxenctrl}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%package -n %{libxenguest}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libxenguest}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%package -n %{libxenlight}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libxenlight}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%package -n %{libxenstat}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libxenstat}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%package -n %{libxenstore}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libxenstore}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%package -n %{libxenvchan}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libxenvchan}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%package -n %{libxlutil}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}xen3.0 < 4.2.1-1

%description -n %{libxlutil}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%package -n %{devname}
Summary:	Development libraries and header files for %{name}
Group:		Development/C
Requires:	%{libblktap} = %{version}-%{release}
Requires:	%{libblktapctl} = %{version}-%{release}
Requires:	%{libbfsimage} = %{version}-%{release}
Requires:	%{libvhd} = %{version}-%{release}
Requires:	%{libxenctrl} = %{version}-%{release}
Requires:	%{libxenguest} = %{version}-%{release}
Requires:	%{libxenlight} = %{version}-%{release}
Requires:	%{libxenstat} = %{version}-%{release}
Requires:	%{libxenstore} = %{version}-%{release}
Requires:	%{libxenvchan} = %{version}-%{release}
Requires:	%{libxlutil} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the development libraries and headers needed
to compile applications linked with Xen libraries.

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

cp %{SOURCE16} tools/firmware/etherboot/ipxe.tar.gz

%build
# clean all stuff
export CFLAGS="%{optflags}"
%make prefix=/usr dist-xen
%configure	--disable-seabios\

%make prefix=/usr dist-tools
make  prefix=/usr dist-docs
unset CFLAGS
make dist-stubdom

%install
make DESTDIR=%{buildroot} prefix=/usr install-xen
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
#install -m 644 docs/man1/* %{buildroot}%{_mandir}/man1
#install -m 644 docs/man5/* %{buildroot}%{_mandir}/man5

# install doc manually
rm -rf %{buildroot}%{_docdir}/qemu
install -d -m 755 %{buildroot}%{_docdir}/%{name}
install -m 644 README %{buildroot}%{_docdir}/%{name}
install -m 644 docs/ps/* %{buildroot}%{_docdir}/%{name} || :
install -m 644 docs/pdf/* %{buildroot}%{_docdir}/%{name} || :

# install state directory
install -d -m 755 %{buildroot}%{_localstatedir}/lib/xend/{domains,state,storage}

# init scripts
#install -d -m 755 %{buildroot}%{_initrddir}
#mv %{buildroot}%{_sysconfdir}/init.d/* %{buildroot}%{_initrddir}
#rm -rf %{buildroot}%{_sysconfdir}/init.d

install -m 755 %{SOURCE20} %{buildroot}%{_initrddir}/xenstored
install -m 755 %{SOURCE21} %{buildroot}%{_initrddir}/xenconsoled
install -m 755 %{SOURCE22} %{buildroot}%{_initrddir}/blktapctrl
install -m 755 %{SOURCE23} %{buildroot}%{_initrddir}/xend

# sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE30} %{buildroot}%{_sysconfdir}/sysconfig/xenstored
install -m 644 %{SOURCE31} %{buildroot}%{_sysconfdir}/sysconfig/xenconsoled
install -m 644 %{SOURCE32} %{buildroot}%{_sysconfdir}/sysconfig/blktapctrl

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/modules
install -m 755 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/sysconfig/modules/%{name}.modules 

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

%post
%_post_service xencommons
%_post_service xend
%_post_service xendomains

%preun
%_preun_service xencommons
%_preun_service xend
%_preun_service xendomains

%files
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/README
%{_sysconfdir}/bash_completion.d/xl.sh
%config(noreplace) %{_sysconfdir}/udev/rules.d/*
%dir %{_sysconfdir}/xen
%{_sysconfdir}/xen/scripts
%{_sysconfdir}/xen/auto
%config(noreplace) %{_sysconfdir}/xen/*.sxp
%config(noreplace) %{_sysconfdir}/xen/*.xml
%config(noreplace) %{_sysconfdir}/xen/xlexample*
%config(noreplace) %{_sysconfdir}/xen/xmexample*
%config(noreplace) %{_sysconfdir}/xen/cpupool
%config(noreplace) %{_sysconfdir}/xen/xl.conf
%config(noreplace) %{_sysconfdir}/xen/oxenstored.conf
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
# general xen state
%{_localstatedir}/lib/xen
%{_localstatedir}/lib/xend
# xenstore state
%{_localstatedir}/lib/xenstored
%{_localstatedir}/run/xenstored
 # xend state
%{_localstatedir}/run/xend
# init scripts
%{_initrddir}/xend
%{_initrddir}/xendomains
%{_initrddir}/blktapctrl
%{_initrddir}/xenstored
%{_initrddir}/xenconsoled
%{_initrddir}/xen-watchdog
%{_initrddir}/xencommons
%{_sysconfdir}/sysconfig/modules/xen.modules
%config(noreplace) %{_sysconfdir}/sysconfig/xendomains
%config(noreplace) %{_sysconfdir}/sysconfig/blktapctrl
%config(noreplace) %{_sysconfdir}/sysconfig/xenstored
%config(noreplace) %{_sysconfdir}/sysconfig/xenconsoled
%config(noreplace) %{_sysconfdir}/sysconfig/xencommons
%config(noreplace) %{_sysconfdir}/logrotate.d/xen
%{_bindir}/pygrub
%{_bindir}/qemu-img-xen
%{_bindir}/qemu-nbd-xen
%{_bindir}/remus
%{_bindir}/xencons
%{_bindir}/xentrace
%{_bindir}/xentrace_format
%{_bindir}/xentrace_setsize
%{_bindir}/xenstore-*
%{_bindir}/xen-detect
%{_bindir}/xenstore
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
%{_sbindir}/xsview
%{_sbindir}/xenperf
%{_sbindir}/xenpm
%{_sbindir}/xenpmd
%{_sbindir}/flask-getenforce
%{_sbindir}/flask-get-bool
%{_sbindir}/flask-label-pci
%{_sbindir}/flask-loadpolicy
%{_sbindir}/flask-setenforce
%{_sbindir}/flask-set-bool
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

%files ocaml
%{_libdir}/ocaml/xeneventchn
%{_libdir}/ocaml/xenmmap
%{_libdir}/ocaml/xenbus
%{_libdir}/ocaml/xenctrl
%{_libdir}/ocaml/xenlight
%{_libdir}/ocaml/xenstore

%files hypervisor
/boot/xen-syms-*
/boot/xen-*.gz
/boot/xen.gz

%files doc
%{_docdir}/%{name}/*
%exclude %{_docdir}/%{name}/README

%files -n %{libblktap}
%{_libdir}/libblktap.so.%{maj30}*

%files -n %{libblktapctl}
%{_libdir}/libblktapctl.so.%{maj10}*

%files -n %{libbfsimage}
%{_libdir}/libfsimage.so.%{maj10}*

%files -n %{libvhd}
%{_libdir}/libvhd.so.%{maj10}*

%files -n %{libxenctrl}
%{_libdir}/libxenctrl.so.%{maj42}*

%files -n %{libxenguest}
%{_libdir}/libxenguest.so.%{maj42}*

%files -n %{libxenlight}
%{_libdir}/libxenlight.so.%{maj20}*

%files -n %{libxenstat}
%{_libdir}/libxenstat.so.%{major}*

%files -n %{libxenstore}
%{_libdir}/libxenstore.so.%{maj30}*

%files -n %{libxenvchan}
%{_libdir}/libxenvchan.so.%{maj10}*

%files -n %{libxlutil}
%{_libdir}/libxlutil.so.%{maj10}*

%files -n %{devname}
%{_includedir}/xen
%{_includedir}/xenstore-compat
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a

