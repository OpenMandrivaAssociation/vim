# (tpg) do not enable it, as it is useless here
%bcond_with selinux
%bcond_without netbeans
%bcond_with vimspell
%bcond_without ruby
%bcond_without lua

%define baseversion %(echo %{version} |cut -d. -f1-2)
%define vimdir vim%(echo %{baseversion}|sed -e 's,\\.,,')

%global __requires_exclude perl\\(getopts.pl\\)
%global __requires_exclude_from %{_datadir}/vim

# Workaround for perl 5.38 API changes (they only change const-ness, so ABI-wise this is ok)
%global optflags %{optflags} -Wno-incompatible-function-pointer-types

# Should we build X11 gui
%bcond_without gui
%bcond_without python3

Summary: The VIM editor
URL: https://www.vim.org/
Name: vim
Version:	9.1.1291
Release:	1
License: Vim and MIT
Source0: https://github.com/vim/vim/archive/v%{version}.tar.gz
Source5: vimrc
Source7: gvim16.png
Source8: gvim32.png
Source9: gvim48.png
Source10: gvim64.png
Source11: vim.svg
%if %{with vimspell}
Source13: vim-spell-files.tar.bz2
%endif
# C++11/C++14/C++17 syntax highlighting, Version 0.931 from
# https://www.vim.org/scripts/script.php?script_id=4293
Source20: https://raw.githubusercontent.com/Mizuchi/STL-Syntax/master/after/syntax/cpp/stl.vim
# Assorted extra syntax highlighting files
Source21: http://trific.ath.cx/Ftp/vim/syntax/dhcpd.vim
Source22: apparmor.vim
Source23: cfengine.vim
Source24: nagios.vim

# Special syntax highlighting and indentation for
# Qt keywords (Q_OBJECT and friends)
Patch1000: vim-8.2-qt-highlighting.patch
# Don't replace "good" characters with .
Patch1001: xxd-locale.patch
# Don't detect paths for HOST perl
Patch1002: vim-crosscompile-find-perl.patch

#Patch2002: vim-7.0-fixkeys.patch
Patch2003: vim-7.4-specsyntax.patch

Patch3002: vim-7.4-nowarnings.patch
Patch3004: vim-7.0-rclocation.patch
Patch3008: vim-7.4-syncolor.patch
Patch3010: vim-7.3-manpage-typo-668894-675480.patch
Patch3016: vim-8.0-copy-paste.patch
# fips warning
Patch3018: vim-crypto-warning.patch

%if %{with python3}
BuildRequires: pkgconfig(python3)
%endif
BuildRequires: perl-devel
BuildRequires: pkgconfig(ncursesw)
BuildRequires:  perl(ExtUtils::Embed) perl(ExtUtils::ParseXS)
BuildRequires:  gpm-devel autoconf file
BuildRequires: pkgconfig(libacl)
BuildRequires: locales-extra-charsets
%if %{with selinux}
BuildRequires: selinux-devel
%endif
%if %{with ruby}
BuildRequires: ruby-devel ruby
%endif
%if %{with lua}
BuildRequires: lua-devel
%endif
Epoch: 2
# for /usr/bin/desktop-file-install
BuildRequires: desktop-file-utils
Conflicts: filesystem < 3

# vim bundles libvterm, which is used during build - so we need to provide
# bundled libvterm for catching possible libvterm CVEs
Provides: bundled(libvterm)

Provides: vi
Requires: vim-common = %{EVRD}
Provides: %{_bindir}/mergetool
Provides: %{_bindir}/vi
Provides: %{_bindir}/vim

Provides: texteditor

%rename %{name}-common
%rename %{name}-minimal
%rename %{name}-enhanced

%description
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.

%package spell
Summary: The dictionaries for spell checking. This package is optional
Requires: vim-common = %{EVRD}

%description spell
This subpackage contains dictionaries for vim spell checking in
many different languages.

%if %{with gui}
%package X11
Summary: The VIM version of the vi editor for the X Window System - GVim
# needed in configure script to have correct macros enabled for GUI (#1603272)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(xt)
BuildRequires: pkgconfig(xpm)
BuildRequires: pkgconfig(ice)
BuildRequires: pkgconfig(sm)
BuildRequires: appstream-util

Requires: %{name} = %{EVRD}
Requires: %{_lib}gtk3_0
Provides: gvim
Provides: %{_bindir}/mergetool
Provides: %{_bindir}/gvim
Requires: hicolor-icon-theme
# suggest python3, python2, lua, ruby and perl packages because of their
# embedded functionality in Vim/GVim
Suggests: python3
Suggests: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version)) perl-devel
%if %{with ruby}
Suggests: ruby-libs ruby
%endif
%if %{with lua}
Suggests: lua
%endif

%description X11
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and
more. VIM-X11 is a version of the VIM editor which will run within the
X Window System.  If you install this package, you can run VIM as an X
application with a full GUI interface and mouse support by command gvim.

Install the vim-X11 package if you'd like to try out a version of vi
with graphics and mouse capabilities.  You'll also need to install the
vim-common package.

%package X11-tutor
Summary:	Tutor teaching the use of the gVIM editor
Requires:	%{name}-X11 = %{EVRD}
Requires:	%{name}-tutor = %{EVRD}

%description X11-tutor
Tutor teaching the use of the gVIM editor
%endif

%package -n xxd
Summary:	Command line hexdump tool

%description -n xxd
Command line hexdump tool

%package tutor
Summary:	Tutor teaching the use of the VIM editor
Requires:	%{name} = %{EVRD}

%description tutor
Tutor teaching the use of the VIM editor

%prep
%autosetup -p1

# Additional syntax highlighting support
mkdir runtime/syntax/cpp
cp %{S:20} runtime/syntax/cpp/
cp %{S:21} %{S:22} %{S:23} %{S:24} runtime/syntax/

# fix rogue dependencies from sample code
chmod -x runtime/tools/mve.awk
sed -i -e "s,bin/nawk,bin/awk,g" runtime/tools/mve.awk

# install spell files
%if %{with vimspell}
%{__tar} xjf %{SOURCE13}
%endif

cd src
autoconf

%build
export CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64"

%if %{cross_compiling}
export vim_cv_toupper_broken=no
export vim_cv_terminfo=yes
export vim_cv_tgetent=zero
export vim_cv_getcwd_broken=no
export vim_cv_timer_create=yes
export vim_cv_stat_ignores_slash=yes
export vim_cv_memmove_handles_overlap=yes
%endif

%define common_options \\\
	--with-features=huge \\\
	--enable-python3interp=dynamic \\\
	--enable-perlinterp=dynamic \\\
	--disable-tclinterp \\\
	--enable-multibyte \\\
	--with-tlib=ncursesw \\\
	--enable-fips-warning \\\
	--with-compiledby="<bugzilla@openmandriva.org>" \\\
	--with-modified-by="<bugzilla@openmandriva.org>" \\\
	--enable-cscope \\\
	--%{?with_selinux:en}%{!?with_selinux:dis}able-selinux \\\
	--%{?with_netbeans:en}%{!?with_netbeans:dis}able-netbeans \\\
	--%{?with_ruby:en}%{!?with_ruby:dis}able-ruby%{?with_ruby:=dynamic} \\\
	--%{?with_lua:en}%{!?with_lua:dis}able-lua%{?with_lua:=dynamic} \\\
	--enable-fail-if-missing

%if %{with gui}
%configure \
	%common_options \
%if %{cross_compiling}
	--with-python3-config-dir=$(ls -1d /usr/%{_target_platform}%{_libdir}/python*/config-*/ |head -n1) \\\
%endif
	--with-x=yes \
	--enable-gtk3-check --enable-gui=gtk3 \
	--enable-xim

%make_build VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} EXTRA_LIBS=-lpython3.11
# Unfortunately, out-of-tree builds aren't supported, so we have to do
# install to an alternate DESTDIR instead of doing %%make_install twice
# in the %%install section
make install DESTDIR="`pwd`/binaries-gui" VIMRCLOC=/etc STRIP=/bin/true
%make_build clean
# Tweak symlinks so we don't conflict with the text-only version
cd binaries-gui%{_bindir}
rm gvim
mv vim gvim
for i in *; do
	if [ -h $i ]; then
		rm $i
		ln -s gvim $i
	fi
done
cd -
%endif

%configure \
	%common_options \
%if %{cross_compiling}
	--with-python3-config-dir=$(ls -1d /usr/%{_target_platform}%{_libdir}/python*/config-*/ |head -n1) \\\
%endif
	--with-x=no --enable-gui=no

%make_build VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} EXTRA_LIBS=-lpython3.11

%install
%make_install BINDIR=%{_bindir} VIMRCLOC=/etc VIMRUNTIMEDIR=/usr/share/vim/%{vimdir} STRIP=/bin/true
find binaries-gui |while read r; do
	[ -e %{buildroot}${r:12} ] || cp -a $r %{buildroot}${r:12}
done

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64,scalable}/apps
install -p -m644 %{SOURCE7} \
	%{buildroot}%{_datadir}/icons/hicolor/16x16/apps/gvim.png
install -p -m644 %{SOURCE8} \
	%{buildroot}%{_datadir}/icons/hicolor/32x32/apps/gvim.png
install -p -m644 %{SOURCE9} \
	%{buildroot}%{_datadir}/icons/hicolor/48x48/apps/gvim.png
install -p -m644 %{SOURCE10} \
	%{buildroot}%{_datadir}/icons/hicolor/64x64/apps/gvim.png
install -p -m644 %{SOURCE11} \
	%{buildroot}%{_datadir}/icons/hicolor/scalable/apps/gvim.svg

%if %{with gui}
# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p %{buildroot}%{_datadir}/metainfo
cat > %{buildroot}%{_datadir}/metainfo/gvim.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
EmailAddress: Bram@moolenaar.net>
SentUpstream: 2014-05-22
-->
<application>
  <id type="desktop">gvim.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <project_license>Vim</project_license>
  <description>
    <p>
     Vim is an advanced text editor that seeks to provide the power of the
     de-facto Unix editor 'Vi', with a more complete feature set.
     It's useful whether you're already using vi or using a different editor.
    </p>
    <p>
     Vim is a highly configurable text editor built to enable efficient text
     editing.
     Vim is often called a "programmer's editor," and so useful for programming
     that many consider it an entire IDE. It is not just for programmers, though.
     Vim is perfect for all kinds of text editing, from composing email to
     editing configuration files.
    </p>
  </description>
  <screenshots>
    <screenshot type="default">
      <image>https://raw.githubusercontent.com/zdohnal/vim/zdohnal-screenshot/gvim16_9.png</image>
    </screenshot>
  </screenshots>
  <url type="homepage">http://www.vim.org/</url>
</application>
EOF

appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/metainfo/*.appdata.xml
%endif

mkdir -p %{buildroot}%{_sysconfdir}
install -p -m644 %{SOURCE5} %{buildroot}%{_sysconfdir}/vimrc

# Remove non-UTF-8 manpages
for i in pl.ISO8859-2 it.ISO8859-1 ru.KOI8-R fr.ISO8859-1 da.ISO8859-1 de.ISO8859-1 tr.ISO8859-9; do
	rm -rf %{buildroot}/%{_mandir}/$i
done

# use common man1/ru directory
mv %{buildroot}/%{_mandir}/ru.UTF-8 %{buildroot}/%{_mandir}/ru

# Remove duplicate man pages
for i in fr.UTF-8 it.UTF-8 pl.UTF-8 da.UTF-8 de.UTF-8 tr.UTF-8; do
	rm -rf %{buildroot}/%{_mandir}/$i
done

mkdir -p %{buildroot}/%{_mandir}/man5
echo ".so man1/vim.1" > %{buildroot}/%{_mandir}/man5/vimrc.5

BUILDDIR="$(pwd)"
cd %{buildroot}%{_mandir}
for i in man1/* man5/*; do
	basename $i |grep -q xxd && continue
	if basename $i |cut -d. -f1 |grep -qE '(g|ev)'; then
		echo "%{_mandir}/${i}*" >>$BUILDDIR/gvim.mans
	else
		echo "%{_mandir}/${i}*" >>$BUILDDIR/vim.mans
	fi
done
for l in *; do
	echo $l |grep -q man && continue
	for i in $l/*/*; do
		if basename $i |cut -d. -f1 |grep -qE '(g|ev)'; then
			echo "%lang($l) %{_mandir}/${i}*" >>$BUILDDIR/gvim.mans
		else
			echo "%lang($l) %{_mandir}/${i}*" >>$BUILDDIR/vim.mans
		fi
	done
done

%if %{without gui}
# Those are always built, but only needed for GUI
rm -f %{buildroot}%{_mandir}/*/evim.1* \
	%{buildroot}%{_mandir}/*/*/evim.1* \
	%{buildroot}%{_datadir}/applications/gvim.desktop
%endif

%files -f vim.mans
%config(noreplace) %{_sysconfdir}/vimrc
%{_bindir}/ex
%{_bindir}/rview
%{_bindir}/rvim
%{_bindir}/view
%{_bindir}/vim
%{_bindir}/vimdiff
%{_datadir}/applications/vim.desktop
%{_datadir}/icons/*/*/*/*
%{_datadir}/vim
%exclude %{_datadir}/vim/%{vimdir}/tutor

%files -n xxd
%{_bindir}/xxd
%{_mandir}/man1/xxd.1*

%files tutor
%{_bindir}/vimtutor
%{_datadir}/vim/%{vimdir}/tutor

%if %{with gui}
%files X11 -f gvim.mans
%{_bindir}/eview
%{_bindir}/evim
%{_bindir}/gview
%{_bindir}/gvim
%{_bindir}/gvimdiff
%{_bindir}/rgview
%{_bindir}/rgvim
%{_datadir}/applications/gvim.desktop
%{_datadir}/metainfo/gvim.appdata.xml

%files X11-tutor
%{_bindir}/gvimtutor
%endif
