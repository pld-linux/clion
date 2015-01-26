%define		bid	140.1740.3
%define		rel	0.4
%define		product	clion
%include	/usr/lib/rpm/macros.java
Summary:	C/C++ IDE
Name:		clion
# About says "Version 1", but lets see first what first version will be
Version:	0
Release:	0.%{bid}.%{rel}
# TODO: figure out what's the licensing and redistribution
License:	?
Group:		Development/Tools
Source0:	http://download.jetbrains.com/cpp/clion-%{bid}.tar.gz
# NoSource0-md5:	af28ecedc672920503013ff457ed38df
NoSource:	0
Source1:	%{product}.desktop
Patch0:		pld.patch
URL:		http://www.jetbrains.com/clion/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	unzip
Requires:	jre >= 1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# don't strip fsnotifier, it's size is checked for "outdated binary"
# https://bugs.archlinux.org/task/34703
# http://git.jetbrains.org/?p=idea/community.git;a=blob;f=platform/platform-impl/src/com/intellij/openapi/vfs/impl/local/FileWatcher.java;h=004311b96a35df1ffc2c87baba78a8b2a8809f7d;hb=376b939fd6d6ec4c12191a5f90503d9d62c501da#l173
%define		_noautostrip	.*/fsnotifier.*

# use /usr/lib, 64bit files do not conflict with 32bit files (64 suffix)
# this allows to install both arch files and to use 32bit jdk on 64bit os
%define		_appdir		%{_prefix}/lib/%{product}

%description
Smart Editor. Code better, refactor easily

Knowing your code through and through, CLion can take care of the
routine while you focus on the important things. Boost your
productivity with the keyboard-centric approach (Vim-emulation plugin
is also available in plugin repository), full coding assistance, smart
and relevant code completion, fast project navigation, intelligent
intention actions, and reliable refactorings.

%prep
%setup -qn clion-%{bid}

# keep only single arch files (don't want to pull 32bit deps by default),
# if you want to mix, install rpm from both arch
%ifarch %{ix86}
rm bin/fsnotifier64
rm bin/libyjpagent-linux64.so
rm bin/libbreakgen64.so
rm bin/%{product}64.vmoptions
rm -r lib/libpty/linux/x86_64
%endif
%ifarch %{x8664}
rm bin/fsnotifier
rm bin/libyjpagent-linux.so
rm bin/libbreakgen.so
#rm bin/%{product}.vmoptions
rm -r lib/libpty/linux/x86
%endif
rm -r lib/libpty/{macosx,win}
chmod a+rx bin/*.so bin/fsnotifier*
mv bin/%{product}.svg .

%patch0 -p1

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_pixmapsdir},%{_desktopdir}}
cp -l build.txt $RPM_BUILD_ROOT/cp-test && l=l && rm -f $RPM_BUILD_ROOT/cp-test
cp -a$l bin help lib license plugins $RPM_BUILD_ROOT%{_appdir}
ln -s %{_pixmapsdir}/%{product}.svg $RPM_BUILD_ROOT%{_appdir}/bin
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{product}.svg $RPM_BUILD_ROOT%{_pixmapsdir}
ln -s %{_appdir}/bin/%{product}.sh $RPM_BUILD_ROOT%{_bindir}/%{product}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{product}
%dir %{_appdir}
%{_appdir}/help
%{_appdir}/license
%{_appdir}/plugins
%dir %{_appdir}/bin
%{_appdir}/bin/%{product}*.vmoptions
%{_appdir}/bin/%{product}.svg
%{_appdir}/bin/idea.properties
%{_appdir}/bin/log.xml
%attr(755,root,root) %{_appdir}/bin/%{product}.sh
%attr(755,root,root) %{_appdir}/bin/inspect.sh
%attr(755,root,root) %{_appdir}/bin/fsnotifier*
%attr(755,root,root) %{_appdir}/bin/libbreakgen*.so
%attr(755,root,root) %{_appdir}/bin/libyjpagent-linux*.so
%dir %{_appdir}/lib
%{_appdir}/lib/*.jar
%dir %{_appdir}/lib/libpty
%dir %{_appdir}/lib/libpty/linux
%dir %{_appdir}/lib/libpty/linux/x86*
%attr(755,root,root) %{_appdir}/lib/libpty/linux/x86*/libpty.so
%{_desktopdir}/%{product}.desktop
%{_pixmapsdir}/%{product}.svg

# TODO: system packages
%defattr(-,root,root,-)
%{_appdir}/bin/cmake
%{_appdir}/bin/gdb
