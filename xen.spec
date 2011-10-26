%define name        xen
%define version     4.1.2
%define release     %mkrel 1
%define major       3.0
%define libname     %mklibname %{name} %{major}
%define develname   %mklibname %{name} -d

Name:       %{name}
Version:    %{version}
Release:    %{release}
Summary:    The basic tools for managing XEN virtual machines
Group:      System/Kernel and hardware
License:    GPL
Source0:    http://bits.xensource.com/oss-xen/release/%{version}/%{name}-%{version}.tar.gz
Source1:    %{name}.modules
Source2:    qemu-xen-4.0.0-rc4.tar.gz
Source3:    http://www.hyperrealm.com/libconfig/libconfig-1.3.2.tar.gz
# stubdoms
Source10:   zlib-1.2.3.tar.gz
Source11:   newlib-1.16.0.tar.gz
Source12:   grub-0.97.tar.gz
Source13:   lwip-1.3.0.tar.gz
Source14:   pciutils-2.2.9.tar.bz2
Source15:   ocaml-3.11.0.tar.gz
Source16:   ipxe-git-v1.0.0.tar.gz
# initscripts
Source20:   init.xenstored 
Source21:   init.xenconsoled
Source22:   init.blktapctrl
Source23:   init.xend
Source30:   sysconfig.xenstored
Source31:   sysconfig.xenconsoled
Source32:   sysconfig.blktapctrl
#Patch0:     xen-4.0.1-fix-stubdom-Makefile.patch
# fedora patches
#Patch3:    xen-xenstore-cli.patch
#Patch5:    xen-net-disable-iptables-on-bridge.patch
#Patch10:   xen-no-werror.patch
#Patch11:   xen-4.0.1-gcc45.patch
#Patch12:   xen-4.0.1-gcc451.patch
#Patch13:   xen-4.0.1-py2.7.patch
Requires:   python
Requires:   python-twisted-core
Requires:   python-pyxml
Requires:   module-init-tools
Requires:   iptables
Requires:   bridge-utils
Requires:   glibc-xen
Requires:   grub
Requires:   kernel-xen
Requires:   %{libname} = %{version}-%{release}
BuildRequires:  SDL-devel
BuildRequires:  libx11-devel
BuildRequires:  gtk2-devel
BuildRequires:  curl-devel
Buildrequires:  dev86-devel
BuildRequires:  libext2fs-devel
BuildRequires:  ncurses-devel
BuildRequires:  libpython-devel >= 2.4
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  lzma-devel
BuildRequires:  pciutils-devel
BuildRequires:  libidn-devel
BuildRequires:  openssl-devel
BuildRequires:  gnutls-devel
BuildRequires:  brlapi-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  libuuid-devel
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib-devel
BuildRequires:  iasl
%if %{mdkversion} >= 201000
BuildRequires:  vde-devel
BuildRequires:  libaio-devel
%endif
BuildRequires:  gettext
BuildRequires:  libconfig-devel
# documentation
BuildRequires:  ghostscript
BuildRequires:  transfig
BuildRequires:  texinfo
BuildRequires:  tetex-latex
%if %{mdkversion} <= 201010
BuildRequires:  tetex-texi2html
%endif
Obsoletes:      xen-uptodate
Requires:       xen-hypervisor = %{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description 
The basic tools for managing XEN virtual machines.

%package ocaml
Summary: OCaml bindings for Xen
Group: Development/Other

%description ocaml
This package contains the Ocaml bindings for Xen

%package hypervisor
Summary: Libraries for Xen tools
Group: System/Kernel and hardware

%description hypervisor
This package contains the Xen hypervisor

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

%description -n %{libname}
This package contains the libraries needed to run programs dynamically
linked with Xen libraries.

%package -n %{develname}
Summary:    Static libraries and header files for %{name}
Group:      Development/C
Requires:   %{libname} = %{version}-%{release}
Provides:   %{name}-devel = %{version}-%{release}
Conflicts:  %{name} < 3.1.0-5mdv2008.1

%description -n %{develname}
This package contains the static development libraries and headers needed
to compile applications linked with Xen libraries.

%prep
%setup -q
%patch0 -p 1
#patch3 -p 1
#patch5 -p 1
%patch10 -p 1
#patch11 -p 1
%patch12 -p1
#patch13 -p1

# stub domain
cp %{SOURCE10} stubdom
cp %{SOURCE11} stubdom
cp %{SOURCE12} stubdom
cp %{SOURCE13} stubdom
cp %{SOURCE14} stubdom
cp %{SOURCE15} stubdom

cp %{SOURCE16} tools/firmware/etherboot/ipxe.tar.gz

# qemu
tar xf %{SOURCE2} -C tools

%build
# clean all stuff
export CFLAGS="%{optflags}"
%make prefix=/usr dist-xen
%make prefix=/usr dist-tools
make  prefix=/usr dist-docs
unset CFLAGS
make dist-stubdom

%install
rm -rf %{buildroot}
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

# udev
#rm -rf %{buildroot}/etc/udev/rules.d/xen*.rules
#mv %{buildroot}/etc/udev/xen*.rules %{buildroot}/etc/udev/rules.d

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

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/README
%{_sysconfdir}/bash_completion.d/xl.sh
%config(noreplace) %{_sysconfdir}/udev/rules.d/*
%dir %{_sysconfdir}/xen
%{_sysconfdir}/xen/scripts
%{_sysconfdir}/xen/auto
%config(noreplace) %{_sysconfdir}/xen/*.sxp
%config(noreplace) %{_sysconfdir}/xen/*.xml
%config(noreplace) %{_sysconfdir}/xen/xmexample*
%config(noreplace) %{_sysconfdir}/xen/cpupool
%config(noreplace) %{_sysconfdir}/xen/xl.conf
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
%{_localstatedir}/run/xend/boot
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
%{_sbindir}/flask-loadpolicy
%{_sbindir}/xsview
%{_sbindir}/xenperf
%{_sbindir}/xenpm
%{_sbindir}/xenpmd
%{_sbindir}/flask-getenforce
%{_sbindir}/flask-setenforce
%{_sbindir}/gtracestat
%{_sbindir}/gtraceview
%{_sbindir}/lock-util
%{_sbindir}/tapdisk-client
%{_sbindir}/tapdisk-diff
%{_sbindir}/tapdisk-stream
%{_sbindir}/tapdisk2
%{_sbindir}/td-util
%{_sbindir}/vhd-update
%{_sbindir}/vhd-util
%{_sbindir}/xen-hvmctx
%{_sbindir}/xen-tmem-list-parse
%{_sbindir}/xenlockprof
%{_sbindir}/xenpaging
%{_sbindir}/xl
%{_sbindir}/gdbsx
%{_sbindir}/kdd
%{_sbindir}/oxenstored
%{_sbindir}/tap-ctl
%{_sbindir}/xen-hptool
%{_sbindir}/xen-hvmcrash
%{_sbindir}/xenwatchdogd
%{_bindir}/xencons
%{_bindir}/xentrace
%{_bindir}/xentrace_format
%{_bindir}/xentrace_setsize
%{_bindir}/xenstore-*
%{_bindir}/pygrub
%{_bindir}/remus
%{_bindir}/xen-detect
%{_bindir}/qemu-img-xen
%{_bindir}/qemu-nbd-xen
%{_bindir}/xenstore


%files ocaml
%defattr(-,root,root)
%{_libdir}/ocaml/eventchn
%{_libdir}/ocaml/mmap
%{_libdir}/ocaml/log
%{_libdir}/ocaml/uuid
%{_libdir}/ocaml/xb
%{_libdir}/ocaml/xc
%{_libdir}/ocaml/xl
%{_libdir}/ocaml/xs

%files hypervisor
%defattr(-,root,root)
/boot/xen-syms-*
/boot/xen-*.gz
/boot/xen.gz

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
