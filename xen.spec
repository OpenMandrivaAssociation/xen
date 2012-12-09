%define major       3.0
%define libname     %mklibname %{name} %{major}
%define develname   %mklibname %{name} -d
%define pyver       %(rpm -q --qf '%%{VERSION}' python |cut -d. -f1-2)

Name:       xen
Version:    4.1.2
Release:    3
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
# Make sure we pass rpmlint checks
Source100:  xen.rpmlintrc
Patch0:     xen-4.0.1-fix-stubdom-Makefile.patch
# fedora patches
Patch3:    xen-xenstore-cli.patch
Patch5:    xen-net-disable-iptables-on-bridge.patch
Patch10:   xen-no-werror.patch
Patch11:   xen-4.0.1-gcc45.patch
Patch12:   xen-4.0.1-gcc451.patch
Patch13:   xen-4.0.1-py2.7.patch
Patch14:   xen-4.1.0-gcc46.patch
Patch15:   xen-4.1.2-fedora-gcc47.patch
Requires:   python
Requires:   python-twisted-core
Requires:   python-pyxml
Requires:   module-init-tools
Requires:   iptables
Requires:   bridge-utils
Requires:   glibc-xen
Requires:   grub
Requires:   kernel-xen-pvops
Requires:   %{libname} = %{version}-%{release}
BuildRequires:  SDL-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  gtk2-devel
BuildRequires:  curl-devel
Buildrequires:  dev86-devel
BuildRequires:  pkgconfig(ext2fs)
BuildRequires:  ncurses-devel
BuildRequires:  pkgconfig(python) >= 2.4
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  lzma-devel
BuildRequires:  pkgconfig(libpci)
BuildRequires:  pkgconfig(libidn)
BuildRequires:  pkgconfig(libssl)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  brlapi-devel
BuildRequires:  pkgconfig(uuid)
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib-devel
BuildRequires:  iasl
BuildRequires:  gettext
BuildRequires:  pkgconfig(libconfig)
# documentation
BuildRequires:  ghostscript
BuildRequires:  transfig
BuildRequires:  texinfo
BuildRequires:  texlive-latex texlive-dvips
Obsoletes:      xen-uptodate
Requires:       xen-hypervisor = %{version}

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
#patch0 -p 1
#patch3 -p 1
#patch5 -p 1
#patch10 -p 1
#patch11 -p 1
#patch12 -p1
#patch13 -p1
%patch14 -p1
%patch15 -p1


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

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/xen
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a


%changelog
* Tue Mar 27 2012 Bernhard Rosenkraenzer <bero@bero.eu> 4.1.2-2
+ Revision: 787490
- Fix build in current environment
- Build with gnutls 3.x

* Wed Oct 26 2011 Sergey Zhemoitel <serg@mandriva.org> 4.1.2-1
+ Revision: 707335
- SILET: correct build > 2010.1
- new release 4.1.2

* Wed Apr 06 2011 Guillaume Rousse <guillomovitch@mandriva.org> 4.1.0-2
+ Revision: 650878
- add yet another external source
- new version

* Sat Nov 27 2010 Funda Wang <fwang@mandriva.org> 4.0.1-3mdv2011.0
+ Revision: 601642
- rebuild for liblzma

* Sat Nov 06 2010 Funda Wang <fwang@mandriva.org> 4.0.1-2mdv2011.0
+ Revision: 593862
- fix build with gcc 4.5.1 and py27

  + Michael Scherer <misc@mandriva.org>
    - rebuild for python 2.7

* Sun Aug 29 2010 Funda Wang <fwang@mandriva.org> 4.0.1-1mdv2011.0
+ Revision: 574082
- New version 4.0.1

* Thu Apr 08 2010 Guillaume Rousse <guillomovitch@mandriva.org> 4.0.0-1mdv2010.1
+ Revision: 532878
- oops
- new version

* Sun Apr 04 2010 Guillaume Rousse <guillomovitch@mandriva.org> 4.0-0.rc9.1mdv2010.1
+ Revision: 531043
- new version

* Sun Mar 28 2010 Guillaume Rousse <guillomovitch@mandriva.org> 4.0-0.rc8.1mdv2010.1
+ Revision: 528624
- new pre-release
- fix initscript

* Sun Mar 14 2010 Guillaume Rousse <guillomovitch@mandriva.org> 4.0-0.rc6.1mdv2010.1
+ Revision: 519088
- new prerelease version

* Wed Mar 03 2010 Guillaume Rousse <guillomovitch@mandriva.org> 4.0-0.rc5.1mdv2010.1
+ Revision: 514016
- new pre-release

* Tue Feb 23 2010 Guillaume Rousse <guillomovitch@mandriva.org> 4.0-0.rc4.1mdv2010.1
+ Revision: 510276
- new version
- files in %%{_sysconfdir}/sysconfig/modules should be executable

* Fri Dec 11 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.4.2-2mdv2010.1
+ Revision: 476337
- add missing sysconfig modules script
- don't gprintify initscripts, it breaks xenddomains

* Tue Nov 10 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.4.2-1mdv2010.1
+ Revision: 464372
- new version
- drop patches merged upstream

* Mon Oct 19 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.4.1-7mdv2010.0
+ Revision: 458266
- hard dependency on xenstored in xend service
- add logrotate configuration
- versionned dependency for libraries

  + Pascal Terjan <pterjan@mandriva.org>
    - Fix previous commit
    - Drop Requires(pre): kernel-xen as there is no scriptlet needing it

  + Thomas Backlund <tmb@mandriva.org>
    - fix typo in initscript

* Sun Sep 27 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.4.1-6mdv2010.0
+ Revision: 450188
- deal with kernel installation in kernel package, not in hypervisor one

* Sat Sep 26 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.4.1-5mdv2010.0
+ Revision: 449400
- add libfsimage support
- more fedora patches
- fix kernel-xen dependency
- drop selinux stuff from initscripts

* Mon Aug 24 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.4.1-3mdv2010.0
+ Revision: 420590
- yet more conditional build dependencies

* Mon Aug 24 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.4.1-2mdv2010.0
+ Revision: 420390
- make vde-devel build dependency conditional, for backporting

* Fri Aug 21 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.4.1-1mdv2010.0
+ Revision: 419016
- sync with fedora build process
- new version
- yet more build dependencies
- remove additional uneeded files
- allow initscripts translation
- drop kernel-xen, as it comes from distinct sources
- drop useless check, squashfs has been merged into the kernel now
- do not symlink %%{_localstatedir}/lib/xend to %%{_localstatedir}/lib/xen, so as to make things a little more clear
- sync build dependencies with fedora
- call installkernel only for hypervisor package
- split hypervisor in its own subpackage
- sync init scripts with fedora
- clean udev rules location
- sync patches with fedora

* Mon Jun 29 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.4.0-1mdv2010.0
+ Revision: 390560
- new version
- drop patch1, merged

* Tue Jun 09 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 3.3.1-5mdv2010.0
+ Revision: 384515
- Sync xensource 2.6.27.5 suse based kernel with latest suse 2.6.27.23
  kernel version. This brings security fix for CVE-2009-1758 and another
  bug fixes.
- Apply fix for http://bugzilla.kernel.org/show_bug.cgi?id=13470

* Thu May 21 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 3.3.1-4mdv2010.0
+ Revision: 378230
- Sync xensource 2.6.27.5 suse based kernel with latest suse 2.6.27.21
  kernel version. This brings bug fixes and what looks like missing
  hunks on 2.6.27.5 version. It fixes also #51085
- Include needed build fixes when using gcc 4.4.0
- On mandriva versions previous to 2009.1, make sure to enable
  compatibility kernel options: CONFIG_SYSFS_DEPRECATED=y,
  CONFIG_SYSFS_DEPRECATED_V2=y, CONFIG_USB_DEVICE_CLASS=y
- Use make macro for kernel build (allow parallel build).

* Sun May 17 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 3.3.1-3mdv2010.0
+ Revision: 376614
- Updated kernel-xen to Novell's 2.6.27.5 version found at
  http://xenbits.xensource.com/ext/linux-2.6.27-xen.hg
  * tarball created stripping mercurial repository info and .orig files
  * default x86_64 and i386 configs were created/updated
  * old buildconfigs structure kept from previous kernel-xen,
    maintainted at buildconfigs.tar.bz2
  * spec updates for new kernel
  * dropped uneeded/merged patches:
    xen-3.2.0-squashfs.patch (squashfs already present in new kernel)
    xen-3.2.0-use-same-arch-default-config.patch (obsolete)
    xen-3.2.0-bnx2-1.4.51b.patch (merged)
  * Fix build with newer gcc, optimization issue
    (linux-2.6.27-xen.hg-avoid-gcc-optmization.patch)
  * Restore default scripts/mkcompile_h from stock kernel (uneeded
    changes)

* Tue Feb 03 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.3.1-2mdv2009.1
+ Revision: 337184
- keep bash completion in its own package

* Tue Jan 13 2009 Guillaume Rousse <guillomovitch@mandriva.org> 3.3.1-1mdv2009.1
+ Revision: 329051
- new version

* Mon Dec 29 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.3.0-7mdv2009.1
+ Revision: 321269
- build stub domain

* Mon Dec 22 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.3.0-6mdv2009.1
+ Revision: 317497
- fix xendomains init script, it needs bash, not just sh

* Thu Dec 18 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.3.0-5mdv2009.1
+ Revision: 315986
- remove additional symlinks in /boot
- add %%{_localstatedir}/lib/xen to fix live migration

* Fri Nov 14 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.3.0-4mdv2009.1
+ Revision: 303279
- ensure pci pass-through support is built
  ensure udev hotplug support, despite /usr/bin/udevinfo removal

* Tue Sep 23 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.3.0-2mdv2009.0
+ Revision: 287209
- compile loop driver as a module (bug #36838)
- drop patch 5, useless now than we have our own init scripts

* Wed Sep 03 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.3.0-1mdv2009.0
+ Revision: 279981
- new version

* Sat Aug 09 2008 Thierry Vignaud <tv@mandriva.org> 3.2.1-3mdv2009.0
+ Revision: 269768
- rebuild early 2009.0 package (before pixel changes)

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - add missing python-pyxml dependency (fix #41745)
    - update bash completion

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Fri May 23 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.2.1-2mdv2009.0
+ Revision: 210415
- update squashfs patch to 3.3

* Thu May 22 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.2.1-1mdv2009.0
+ Revision: 210001
- new version
  check squashfs support is built

* Wed May 21 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.2.0-4mdv2009.0
+ Revision: 209810
- patch 7: fix sumversion compilation
- really apply patch 5
- patch 6: fix compilation with gcc 4.3
- rediff squashfs patch to ensure support is built
- no more vnc-devel build dependency

* Sat May 17 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.2.0-3mdv2009.0
+ Revision: 208456
- add kernel-xen and kernel-xen-devel virtual packages

* Sat Mar 22 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.2.0-2mdv2008.1
+ Revision: 189471
- minor completion fixes
  silent initscripts errors

* Mon Mar 03 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.2.0-1mdv2008.1
+ Revision: 177959
- new version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Dec 07 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.1.2-3mdv2008.1
+ Revision: 116295
- really fix devel package dependencies

* Thu Dec 06 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.1.2-2mdv2008.1
+ Revision: 115963
- fix devel package dependencies

* Fri Nov 16 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.1.2-1mdv2008.1
+ Revision: 109146
- new version
- add kernel and xen versions in kernel package name, to ensure package uniqueness
- add xen version in kernel extra string to make the files really unique
- workaround curious ln -sf behaviour with directories in kernel-devel installation
- fix conflict

* Sun Nov 11 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.1.1-1mdv2008.1
+ Revision: 107975
- make kernel-xen virtual package use xen version, not kernel version
- new version

* Fri Nov 09 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.1.0-6mdv2008.1
+ Revision: 107033
- move the install kernel call to the hypervisor post-installation, so as to break circular dependencies between kernel and hypervisor (kernel alone is not bootable anyway), and make dependencies between hypervisor and kernel stricter
- fix ldconfig call to belong to lib package
- add a call to installkernel -R when uninstalling kernel
- add a conflict from lib packages to previous releases of the main one to help upgrade
- make the kernel package provides kernel-xen

* Thu Nov 08 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.1.0-5mdv2008.1
+ Revision: 106856
- build missing vnc binaries
- let installkernel manage unversioned symlink
- compress modules, and create modules.description file, as in other mdv kernels
- remove additional vmlinuz symlinks, as per other mdv kernels
- fix using extraversion on x86_64
- versioned kernel package and files
- split libs and devel files in their own package
- standard virtual packages for kernel and kernel-devel packages
- no need for the serial support patch, actually, xencons is OK
- better squashfs patch

  + Vincent Danen <vdanen@mandriva.com>
    -P403: security patch for CVE-2007-3919

* Fri Oct 12 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.1.0-4mdv2008.1
+ Revision: 97223
- build requires tetex-texi2html instead of texi2html
- fix serial support on x86_64
- patch3: squashfs support (fix bug#34275)

* Fri Oct 05 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.1.0-3mdv2008.1
+ Revision: 95545
- security patches for CVE-2007-1321 and CVE-2007-4993

* Mon Sep 17 2007 Olivier Blin <blino@mandriva.org> 3.1.0-2mdv2008.0
+ Revision: 89095
- make kernel-xen require xen in post script (bootloader-config only configures xen kernels if xen is installed)

* Sun Sep 02 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.1.0-1mdv2008.0
+ Revision: 78111
- obsoletes xen-uptodate
- merge from xen-uptodate package
- make xen-uptodate the new xen package
- really fix PAE mismatch on i586 (#32027)
- install missing %%{_localstatedir}/xend directory
- build PAE hypervisor (fix #32027)
- fix memcmp build issue
- add missing patch
- update bnx2 driver to 1.4.51b, to fix IPMI issues (see http://lists.us.dell.com/pipermail/linux-poweredge/2007-January/029054.html)
- don't mark scripts as configuration
- handle doc manually
- patch0: fix default interface guess
- installing kernel is part of kernel package post-installation, not of kernel-devel one
- updated completion
- fix file list for mdk version <= 2007
- add a bootloader entry (support is just one patch away)
- requires grub
- fix kernel source tree
- call installkernel in %%post to create initrd
- don't prepare kernel tree twice, and use sparse kernel tree as devel package content
- fix symlink handling in kernel %%post
- fix file list in kernel package
- drop init patch, merged upstream
- change dependencies: make it provide xen, so as to be usable for building other package requiring a recent xen version, hence dropping explicit conflict on regular xen package
- new version
- can't provide and conflict at once with xen
- build only one kernel
- split documentation into a subpackage
- build host and guest kernels too
- change group (fix #29868)
- LSB compliant init script

  + Thierry Vignaud <tv@mandriva.org>
    - replace %%{_datadir}/man by %%{_mandir}!


* Mon Mar 19 2007 Gwenole Beauchesne <gbeauchesne@mandriva.com> 3.0.3-0.20060703.5mdv2007.1
- forward port lib64 fix from 2006-branch

* Mon Dec 11 2006 Arnaud Patard <apatard@mandriva.com> 3.0.3-0.20060703.4mdv2007.1
- Rebuilt for python 2.5 
- Fix python version check and include egg-info files (G. Rousse)
- Add bash-completion support (G. Rousse)

* Wed Sep 20 2006 Arnaud Patard <apatard@mandriva.com> 3.0.3-0.20060703.3mdv2007.0
- Rebuild with ncurses 5.5-1.20051029.3mdv2007.0

* Wed Sep 13 2006 Arnaud Patard <apatard@mandriva.com> 3.0.3-0.20060703.2mdv2007.0
- Fix patch0

* Tue Jul 11 2006 Arnaud Patard <apatard@mandriva.com> 3.0.3-0.20060703.1mdv2007.0
- New snapshot

* Fri May 19 2006 Arnaud Patard <apatard@mandriva.com> 3.0-0.20060510.1mdk
- New snapshot
- Disable gprintify
- Allow to set bridge mac adress

* Tue Jan 17 2006 Arnaud Patard <apatard@mandriva.com> 3.0-0.20051213.1mdk
- New snapshot

* Mon Jan 16 2006 Stefan van der Eijk <stefan@eijk.nu> 3.0-0.20050823.7mdk
- BuildRequires

* Fri Sep 09 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 3.0-0.20050823.6mdk
- x86_64 fixes for binutils 2.16.9x
- requires glibc-xen for */nosegneg/ libs

* Fri Aug 12 2005 Fl\E1vio Bruno Leitner <fbl@mandriva.com> 3.0-0.20050823.5mdk
- updated to snapshot of 2005-08-23 (last know working)

* Fri Aug 12 2005 Fl\E1vio Bruno Leitner <fbl@mandriva.com> 3.0-0.20050829.4mdk
- updated to snapshot of 2005-08-29

* Fri Aug 12 2005 Fl\E1vio Bruno Leitner <fbl@mandriva.com> 3.0-0.20050811.3mdk
- updated to snapshot of 2005-08-19

* Fri Aug 12 2005 Fl\E1vio Bruno Leitner <fbl@mandriva.com> 3.0-0.20050811.2mdk
- updated to snapshot of 2005-08-11

* Sat Aug 06 2005 Fl\E1vio Bruno Leitner <fbl@mandriva.com> 3.0-0.20050801.1mdk
- created package.
