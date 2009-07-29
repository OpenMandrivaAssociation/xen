%define name                    xen
%define xen_version             3.4.0
%define rel                     2
%define xen_release             %mkrel %rel
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
Source20:   init.xenstored 
Source21:   init.xenconsoled
Source22:   init.blktapctrl
Source23:   init.xend
Source30:   sysconfig.xenstored
Source31:   sysconfig.xenconsoled
Source32:   sysconfig.blktapctrl
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
Patch15:    xen-net-disable-iptables-on-bridge.patch
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
BuildRequires:  SDL-devel
BuildRequires:  libx11-devel
BuildRequires:  gtk2-devel
BuildRequires:  curl-devel
Buildrequires:  dev86-devel
BuildRequires:  libext2fs-devel
BuildRequires:  ncurses-devel
BuildRequires:  libpython-devel >= 2.4
BuildRequires:  zlib-devel
BuildRequires:  pciutils-devel
BuildRequires:  libidn-devel
BuildRequires:  libaio-devel
BuildRequires:  openssl-devel
BuildRequires:  gettext
# documentation
BuildRequires:  ghostscript
BuildRequires:  transfig
BuildRequires:  texinfo
BuildRequires:  tetex-latex
BuildRequires:  tetex-texi2html
Obsoletes:      xen-uptodate
Requires:       xen-hypervisor = %{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description 
The basic tools for managing XEN virtual machines.

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
Requires:   %{libname} = %{xen_version}-%{xen_release}
Provides:   %{name}-devel = %{xen_version}-%{xen_release}
Conflicts:  %name} < 3.1.0-5mdv2008.1

%description -n %{develname}
This package contains the static development libraries and headers needed
to compile applications linked with Xen libraries.

%prep
%setup -q -n %{name}-%{xen_version}
%patch0 -p 1

%patch11 -p 1
%patch12 -p 1
%patch13 -p 1
%patch14 -p 1
%patch15 -p 1

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
export pae=y 
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
export pae=y
make -C tools install HOTPLUGS=install-udev
make -C xen install
make -C stubdom install
%ifarch x86_64
make -C stubdom install-grub XEN_TARGET_ARCH=x86_32
%endif

# remove additional kernel symlink
rm -f %{buildroot}/boot/xen-3.4.gz
rm -f %{buildroot}/boot/xen-3.gz

# remove unwanted firmware files
rm -rf %{buildroot}/lib/firmware

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

# delete original ones
rm -rf %{buildroot}%{_sysconfdir}/init.d

# udev
rm -rf %{buildroot}/etc/udev/rules.d/xen*.rules
mv %{buildroot}/etc/udev/xen*.rules %{buildroot}/etc/udev/rules.d

# init scripts
install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{SOURCE20} %{buildroot}%{_initrddir}/xenstored
install -m 755 %{SOURCE21} %{buildroot}%{_initrddir}/xenconsoled
install -m 755 %{SOURCE22} %{buildroot}%{_initrddir}/blktapctrl
install -m 755 %{SOURCE23} %{buildroot}%{_initrddir}/xend

# sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE30} %{buildroot}%{_sysconfdir}/sysconfig/xenstored
install -m 644 %{SOURCE31} %{buildroot}%{_sysconfdir}/sysconfig/xenconsoled
install -m 644 %{SOURCE32} %{buildroot}%{_sysconfdir}/sysconfig/blktapctrl

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post hypervisor
/sbin/installkernel %{kernel_file_string}

%preun hypervisor
/sbin/installkernel -R %{kernel_file_string}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/README
%config(noreplace) %{_sysconfdir}/udev/rules.d/*
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
%config(noreplace) %{_sysconfdir}/sysconfig/xendomains
%config(noreplace) %{_sysconfdir}/sysconfig/blktapctrl
%config(noreplace) %{_sysconfdir}/sysconfig/xenstored
%config(noreplace) %{_sysconfdir}/sysconfig/xenconsoled

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
