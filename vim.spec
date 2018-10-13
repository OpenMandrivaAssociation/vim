# Notes / Warning :
# - this package is not prefixable
# - to update official patches, aka SOURCE4, see README.upstream_patches in SOURCE4

%define rversion %(echo %version |cut -d. -f1-2)
%define official_ptchlvl %(echo %version |cut -d. -f3)
%define __noautoreq '.*/bin/awk|.*/bin/gawk'
%global	ldflags	%{ldflags} -Wl,--error-unresolved-symbols

# Should we build X11 gui
%bcond_without gui
%bcond_without python3

%define	title		VI editor
%define longtitle	All-purpose text editor

Name:		vim
Version:	8.1.0471
Release:	1
Summary:	VIsual editor iMproved
Url:		http://www.vim.org/
License:	Charityware
Group:		Editors
Source0:	https://github.com/vim/vim/archive/v%{version}.tar.gz
# read README.omv prior updating official patches:
Source3:	README.omv
# http://vim.sourceforge.net/scripts/script.php?script_id=98
Source5:	vim-spec-3.0.bz2
Source6:	http://trific.ath.cx/Ftp/vim/syntax/dhcpd.vim
# from apparmor-utils package
Source7:	apparmor.vim
Source8:	cfengine.vim
Source9:	nagios.vim
# http://www.vim.org/scripts/script.php?script_id=4293 (0.92)
# C++11/C++14 STL syntax highlighting
Source10:	stl.vim
# https://raw.githubusercontent.com/hynek/vim-python-pep8-indent/master/indent/python.vim
# python PEP8 indent replacing upstream non-PEP8 indent
Source11:	python-pep8-indent.vim
# perfect theme
# https://github.com/tomasr/molokai.git
Source12:	molokai.vim
Source13:	virc
Source100:	vim.rpmlintrc
# MDK patches
Patch1:		vim-8.0-nomouse.patch
Patch2:		vim-5.6a-paths.patch
Patch3:		vim-7.4.005-rpm-spec-syntax.patch
Patch4:		vim-8.1-perl-includes.patch
Patch8:		vim-6.0af-man-path.patch
Patch10:	xxd-locale.patch
Patch20:	vimrc_hebrew.patch
Patch22:	vim-6.1-fix-xterms-comments.patch
Patch24:	vim-6.1-outline-mode.patch
Patch25:	vim-6.1-xterm-s-insert.patch
Patch28:	vim-7.4-po-mode.patch
Patch30:	vim-7.3.478-add-dhcpd-syntax.patch
Patch33:	vim-7.4.005-CVE-2009-0316-debian.patch
# (proyvind): fix path to locale files
Patch35:	vim-7.4.005-use-proper-localedir.patch
Patch36:	vim-7.4-qt-highlighting.patch
Patch37:	vim-7.3.381-always-install-icons.patch
Patch38:	vim-7.3.478-dont-check-for-xsetlocale.patch

# Fedora patches
Patch101:	vim-7.4-fstabsyntax.patch

BuildRequires:	perl(ExtUtils::Embed)
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(python)
%if %{with python3}
BuildRequires:	pkgconfig(python3)
%endif
BuildRequires:	perl-devel
BuildRequires:	acl-devel
%if %{with gui}
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(xt)
BuildRequires:	tcl
BuildRequires:	tcl-devel
%endif

%description
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor. Vi was the first real screen-based editor for UNIX, and is still
very popular. VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more. The vim-common package
contains files which every VIM binary will need in order to run.

%package	common
Summary:	The common files needed by any version of the VIM editor
Group:		Editors
Conflicts:	man-pages-fr < 1.68.0-2mdk
Conflicts:	man-pages-it < 0.3.4-2mdk
Conflicts:	man-pages-pl <= 0.4-10mdk
Conflicts:	git-core < 1:1.6.0.1-2mdv

%description	common
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor. Vi was the first real screen-based editor for UNIX, and is still
very popular. VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more. The vim-common package
contains files which every VIM binary will need in order to run.

%package	minimal
Summary:	A minimal version of the VIM editor
Group:		Editors
Provides:	vim
Requires(post,postun):	chkconfig
Requires(post,postun):	rpm-helper
Requires(post,postun):	bash

%description	minimal
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor. Vi was the first real screen-based editor for UNIX, and is still
very popular. VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more. The vim-minimal package
includes a minimal version of VIM, which is installed into /bin/vi for use
when only the root partition is present.

%package	enhanced
Summary:	A version of the VIM editor which includes recent enhancements
Group:		Editors
Requires(post,postun):	chkconfig
Requires(post,postun):	rpm-helper
Requires(post,postun):	bash
Requires:	vim-common >= %{EVRD}
Obsoletes:	vim-color < 8.0.1523-1
Provides:	vim
Provides:	vim-color

%description	enhanced
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor. Vi was the first real screen-based editor for UNIX, and is still
very popular. VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more. The vim-enhanced package
contains a version of VIM with extra, recently introduced features like
Python and Perl interpreters.

Install the vim-enhanced package if you'd like to use a version of the VIM
editor which includes recently added enhancements like interpreters for the
Python and Perl scripting languages. You'll also need to install the
vim-common package.

%if %{with gui}
%package	X11
Summary:	The VIM version of the vi editor for the X Window System
Group:		Editors
Provides:	vim
Requires(post,postun):	update-alternatives
Requires(post,postun):	rpm-helper
Requires(post,postun):	bash
Requires:	vim-common >= %{EVRD}
Recommends: 	config(adwaita-gtk3-theme)

%description	X11
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor. Vi was the first real screen-based editor for UNIX, and is still
very popular. VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more. VIM-X11 is a version of the
VIM editor which will run within the X Window System. If you install this
package, you can run VIM as an X application with a full GUI interface and
mouse support.

Install the vim-X11 package if you'd like to try out a version of vi with
graphics and mouse capabilities. You'll also need to install the
vim-common package.
%endif

%prep
%setup -q -n vim-%{version}
# spec plugin
rm -f runtime/doc/pi_spec.txt
rm -f runtime/ftpplugin/spec.vim
tar xfj %{SOURCE5} -C runtime
cp -a %{SOURCE6} runtime/syntax/
cp -a %{SOURCE7} runtime/syntax/
cp -a %{SOURCE8} runtime/syntax/
cp -a %{SOURCE9} runtime/syntax/
install -m644 %{SOURCE10} runtime/syntax/cpp
cp -a %{SOURCE11} runtime/indent/python.vim
cp -a %{SOURCE12} runtime/colors

#mdk patches
%patch1 -p1 -b .nomouse~
%patch2 -p1 -b .p2~
%patch3 -p1 -b .spec~
%patch4 -p1 -b .perlinc~
%if "%{_libdir}" != "/usr/lib64"
sed -i -e 's,/usr/lib64/perl5/CORE,%{_libdir}/perl5/CORE,g' src/configure.ac
%endif
%patch8 -p1 -b .manpath~
%patch10 -p1 -b .xxdloc~
%patch20 -p1 -b .warly~
%patch22 -p0 -b .p22~
%patch24 -p1 -b .p24~
%patch25 -p1 -b .p25~
%patch28 -p1 -b .pomode~
%patch30 -p1 -b .dhcpd~
%patch33 -p1 -b .security~
#patch35 -p1 -b .localedir~
%patch36 -p1 -b .qthl~
#patch37 -p1 -b .icons_install~
#patch38 -p1 -b .xsetlocale~

# Fedora patches
%patch101 -p1 -b .fstab~

# Get rid of patch backup files - some stuff gets installed by
# copying the entire directory
find . -name "*.*~" |xargs rm -f

perl -pi -e 's|SYS_VIMRC_FILE "\$VIM/vimrc"|SYS_VIMRC_FILE "%{_sysconfdir}/vim/vimrc"|' src/os_unix.h
perl -pi -e 's|SYS_GVIMRC_FILE "\$VIM/gvimrc"|SYS_GVIMRC_FILE "%{_sysconfdir}/vim/gvimrc"|' src/os_unix.h
# disable command echo
for i in runtime/{gvimrc_example.vim,vimrc_example.vim}; do
	 perl -pi -e 's!^set showcmd!set noshowcmd!' $i
done
perl -pi -e 's|\Qsvn-commit.*.tmp\E|svn-commit*.tmp|' ./runtime/filetype.vim
pushd src
autoconf
popd

%if %{with gui}
mkdir .gui
cp -a * .gui
%endif

mkdir .enhanced
cp -a * .enhanced

mkdir .minimal
cp -a * .minimal
# https://issues.openmandriva.org/show_bug.cgi?id=1627
sed -i "s/vimrc/virc/" .minimal/src/os_unix.h

%build
%if %{with gui}
# First build: gvim
pushd .gui
%configure \
	--localedir=%{_localedir} \
	--disable-darwin \
	--disable-selinux \
	--disable-xsmp \
	--disable-xsmp-interact \
	--enable-luainterp=dynamic \
	--enable-mzschemeinterp=no \
	--enable-perlinterp=dynamic \
	--enable-pythoninterp=dynamic \
	--enable-python3interp=dynamic \
	--enable-tclinterp=dynamic \
	--enable-rubyinterp=dynamic \
	--disable-cscope \
	--disable-workshop \
	--enable-netbeans \
	--disable-sniff \
	--enable-multibyte \
	--disable-hangulinput \
	--enable-xim \
	--enable-fontset \
	--with-features=huge \
	--enable-gui=gtk3 \
	--with-tlib=ncurses \
	--enable-gtk3-check \
	--enable-acl \
	--enable-gpm \
	--disable-sysmouse \
	--enable-nls \
	--with-x=yes \
	--with-compiledby="%{vendor} %{bugurl}" \
	--with-modified-by="the OpenMandriva team <om-cooker@lists.openmandriva.org>"

%make
popd
%endif

# Second build: vim-enhanced
pushd .enhanced
# We use --disable-gpm here because gpm in vim running in konsole
# "breaks" cut&paste -- cut&paste is far more useful than vim
# mouse control.
%configure \
	--localedir=%{_localedir} \
	--disable-selinux \
	--enable-acl \
	--enable-luainterp=dynamic \
	--enable-perlinterp=dynamic \
	--enable-pythoninterp=dynamic \
	--enable-python3interp=dynamic \
	--enable-tclinterp=dynamic \
	--enable-rubyinterp=dynamic \
	--with-features=huge \
	--with-x=no \
	--enable-gui=no \
	--with-tlib=ncurses \
	--disable-gpm \
	--with-compiledby="%{vendor} %{bugurl}" \
	--with-modified-by="the OpenMandriva team <om-cooker@lists.openmandriva.org>"

%make
popd

# Third build: vim-minimal
pushd .minimal
%configure \
	--localedir=%{_localedir} \
	--disable-selinux \
	--with-features=tiny \
	--disable-tclinterp \
	--disable-cscope \
	--enable-multibyte \
	--disable-hangulinput \
	--disable-xim \
	--disable-fontset \
	--disable-gui \
	--disable-acl \
	--disable-pythoninterp \
	--disable-python3interp \
	--disable-perlinterp \
	--with-x=no \
	--enable-gui=no \
	--with-tlib=ncurses \
	--disable-gpm \
	--with-compiledby="%{vendor} %{bugurl}" \
	--with-modified-by="the OpenMandriva team <om-cooker@lists.openmandriva.org>"

%make
popd

cp -al runtime/doc doc
# apply os_doc.diff
pushd doc
rm -f *.1
rm -f os_{390,dos,msdos,risc,win32,amiga,mac,os2,beos,mint,qnx,vms}.txt
rm -f gui_{w16,w32}.txt
rm -f vim2html.pl Makefile *awk
popd

# britton support
ln -s tutor.fr runtime/tutor/tutor.br
ln -s menu_fr_fr.iso_8859-15.vim runtime/lang/menu_br

%install
%makeinstall_std -C .enhanced VIMRTDIR=""


make -C .enhanced/src installmacros prefix=%{buildroot}%{_prefix} VIMRTDIR=""

install -d %{buildroot}%{_localedir}
mv %{buildroot}%{_datadir}/vim/lang/*/ %{buildroot}%{_localedir}

%if %{with gui}
install -m755 .gui/src/vim -D %{buildroot}%{_bindir}/gvim
%endif

install -m755 .enhanced/src/vim -D %{buildroot}%{_bindir}/vim-enhanced
install -m755 .minimal/src/vim -D %{buildroot}/bin/vim-minimal

rm -f %{buildroot}%{_bindir}/{rview,rvim,view}
for i in ex vimdiff; do
  ln -sf vim-enhanced %{buildroot}%{_bindir}/$i
done
rm -f %{buildroot}%{_mandir}/man1/evim.*
%if %{with gui}
ln -sf gvim %{buildroot}%{_bindir}/gvimdiff
ln -sf gvim %{buildroot}%{_bindir}/vimx
%endif
rm -f %{buildroot}%{_datadir}/vim/*/cmake.vim

# installing man pages
for i in %{buildroot}%{_mandir}/man1/{vi,rvi}; do
  ln -s vim.1%{_extension} $i.1%{_extension}
done

%if %{with gui}
ln -s vim.1%{_extension} %{buildroot}%{_mandir}/man1/gvim.1%{_extension}
%endif

ln -sf vimrc_example.vim %{buildroot}%{_datadir}/vim/vimrc

# Be short-circuit aware :
ln -f runtime/macros/README.txt README_macros.txt
ln -f runtime/tools/README.txt README_tools.txt

# installing the menu icons & entry
%if %{with gui}
# gvim and fontset (from Pablo) 2001/03/19
echo 'set guifontset=-*-fixed-medium-r-normal--14-*-*-*-c-*-*-*,-*-*-medium-r-normal--14-*-*-*-c-*-*-*,-*-*-medium-r-normal--14-*-*-*-m-*-*-*,*' > %{buildroot}%{_datadir}/vim/gvimrc
%else
rm -rf %{buildroot}%{_iconsdir}
%endif

# prevent including twice the doc
rm -rf %{buildroot}%{_datadir}/vim/doc
ln -s %{_defaultdocdir}/%{name}-common/doc %{buildroot}%{_datadir}/vim/doc

%{find_lang} %{name} --with-man --all-name

find %{buildroot}%{_datadir}/vim/tutor -name "tutor.*" | grep -v -E 'tutor(|\.vim)$' |
 sed -e "s^%{buildroot}^^" -e 's!^\(.*tutor.\)\(..\)!%lang(\2) \1\2!g' >> %{name}.lang

find %{buildroot}%{_datadir}/vim/lang -name "menu*" |
 sed -e "s^%{buildroot}^^" \
  -e 's!^\(/.*menu_\)\(..\)\(_\)!%lang(\2) \1\2\3!g' \
  -e 's!^\(/.*menu_\)\(..\)\(_\)!%lang(\2) \1\2\3!g' \
  -e 's!^\(/.*menu\)\(_chinese\)!%lang(zh) \1\2!g' \
  -e 's!^\(/.*menu\)\(_czech_\)!%lang(cs) \1\2!g' \
  -e 's!^\(/.*menu\)\(_french\)!%lang(fr) \1\2!g' \
  -e 's!^\(/.*menu\)\(_german\)!%lang(de) \1\2!g' \
  -e 's!^\(/.*menu\)\(_japanes\)!%lang(ja) \1\2!g' \
  -e 's!^\(/.*menu\)\(_polish\)!%lang(pl) \1\2!g' \
  -e 's!^\(/.*menu\)\(_slovak\)!%lang(sk) \1\2!g' \
  -e 's!^\(/.*menu\)\(_spanis\)!%lang(es) \1\2!g' \
  -e 's!^\(/.*menu_\)\(..\)!%lang(\2) \1\2!g' \
  >> %{name}.lang
rm -f %{buildroot}%{_bindir}/vim
# Desktop file for the text mode version? Probably not very useful
rm -f %{buildroot}%{_datadir}/applications/vim.desktop

mkdir -p %{buildroot}%{_sysconfdir}/vim/
MESSAGE='"Place your systemwide modification here.\n"%{_datadir}/vim/ files will be overwritten on update\n'
echo -e "$MESSAGE\nsource %{_datadir}/vim/vimrc" > %{buildroot}%{_sysconfdir}/vim/vimrc
%if %{with gui}
echo -e "$MESSAGE\nsource %{_datadir}/vim/gvimrc" > %{buildroot}%{_sysconfdir}/vim/gvimrc
%endif
install -m644 %{SOURCE13} %{buildroot}%{_sysconfdir}/vim/virc

%post minimal
update-alternatives --install /bin/vi vi /bin/vim-minimal 10 \
    --slave /bin/view view /bin/vim-minimal \
    --slave /bin/ex ex /bin/vim-minimal \
    --slave /bin/rvi rvi /bin/vim-minimal \
    --slave /bin/rview rview /bin/vim-minimal
update-alternatives --install /bin/vim vim /bin/vim-minimal 10 \
    --slave /bin/rvim rvim /bin/vim-minimal

%postun minimal
[ $1 = 0 ] || exit 0
update-alternatives --remove vi /bin/vim-minimal
update-alternatives --remove vim /bin/vim-minimal

%triggerpostun minimal -- vim-minimal < 7.3
update-alternatives --remove uvi /bin/vim-minimal
for i in view ex rvi rview rvim; do
    update-alternatives --remove $i /bin/$i || :
done

%post enhanced
update-alternatives --install /bin/vi vi /usr/bin/vim-enhanced 20 \
    --slave /bin/view view /usr/bin/vim-enhanced \
    --slave /bin/ex ex /usr/bin/vim-enhanced \
    --slave /bin/rvi rvi /usr/bin/vim-enhanced \
    --slave /bin/rview rview /usr/bin/vim-enhanced
update-alternatives --install /bin/vim vim /usr/bin/vim-enhanced 20 \
    --slave /bin/rvim rvim /usr/bin/vim-enhanced

%postun enhanced
[ $1 = 0 ] || exit 0
update-alternatives --remove vi /usr/bin/vim-enhanced
update-alternatives --remove vim /usr/bin/vim-enhanced

%triggerpostun enhanced -- vim-enhanced < 7.3
update-alternatives --remove uvi /usr/bin/vim-enhanced

%files common -f vim.lang
%doc README*.txt runtime/termcap
#%doc --parents mandriva/README*
%doc doc

%dir %{_datadir}/vim/
%{_datadir}/vim/autoload
%{_datadir}/vim/colors
%{_datadir}/vim/compiler
%{_datadir}/vim/doc
%{_datadir}/vim/ftplugin
%{_datadir}/vim/indent
%{_datadir}/vim/keymap
%dir %{_datadir}/vim/lang
%{_datadir}/vim/lang/README.txt
%{_datadir}/vim/macros
%{_datadir}/vim/plugin
%{_datadir}/vim/pack
%{_datadir}/vim/print
%{_datadir}/vim/spell
%{_datadir}/vim/syntax
%{_datadir}/vim/tools
%dir %{_datadir}/vim/tutor
%{_datadir}/vim/tutor/*.txt
%{_datadir}/vim/tutor/tutor
%{_datadir}/vim/tutor/tutor.vim
%{_datadir}/vim/*.vim
%{_datadir}/vim/vimrc
%{_mandir}/man1/vim.1*
%{_mandir}/man1/ex.1*
%{_mandir}/man1/vi.1*
%{_mandir}/man1/view.1*
%{_mandir}/man1/rvi.1*
%{_mandir}/man1/rview.1*
%{_mandir}/man1/vimdiff.1*
%{_mandir}/man1/vimtutor.1*
%{_mandir}/man1/rvim.1*
%{_bindir}/vimtutor
%{_bindir}/xxd
%{_mandir}/man1/xxd.1*
%{_datadir}/vim/rgb.txt
%dir %{_sysconfdir}/vim/
%exclude %{_sysconfdir}/vim/virc
%config(noreplace) %{_sysconfdir}/vim/*

%files minimal
%doc README*.txt
/bin/vim-minimal
%config(noreplace) %{_sysconfdir}/vim/virc

%files enhanced
%doc README*.txt
%{_bindir}/ex
%{_bindir}/vimdiff
%{_bindir}/vim-enhanced

%if %{with gui}
%files X11
%doc README*.txt
%{_bindir}/gvim
%{_bindir}/gvimdiff
%{_bindir}/vimx
%{_mandir}/man1/gvim.1*
%{_iconsdir}/locolor/16x16/apps/gvim.png
%{_iconsdir}/locolor/32x32/apps/gvim.png
%{_iconsdir}/hicolor/48x48/apps/gvim.png
%{_datadir}/applications/gvim.desktop
%{_datadir}/vim/gvimrc
%endif
