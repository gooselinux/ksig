# Review request:
# https://bugzilla.redhat.com/show_bug.cgi?id=432701

%define    svn_date 20080213

Name:           ksig
Version:        1.1
Release:        0.10.%{svn_date}%{?dist}
Summary:        A graphical application to manage multiple email signatures

Group:          Applications/Internet
License:        GPLv2+
URL:            http://extragear.kde.org

# Creation of tarball from svn
#
# Kevin Kofler enhanced the create_tarball.rb script from upstream to also support ksig
# This script also download the translations and docs
# To use it you will need the script itself and a config.ini in the same directory
#
# http://repo.calcforge.org/f9/kde4-tarballs/create_tarball.rb
# http://repo.calcforge.org/f9/kde4-tarballs/config.ini
#
# To create a new checkout use it with anonymous svn access
# ./create_tarball.rb -n
# At the prompt you have to enter "ksig" (without brackets)

Source0:        %{name}-%{version}-svn.tar.bz2
# fix CMakeLists.txt so this builds as a standalone directory (without all of extragear-pim)
Patch0:         ksig-1.1-svn-cmakelists.patch
# Install documentation into the correct subdir
Patch1:         ksig-1.1-svn-docsdir.patch
Patch2:         ksig-1.1-svn-desktopfile.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kdelibs4-devel
BuildRequires:  kde-filesystem >= 4
BuildRequires:  cmake
BuildRequires:  gettext
BuildRequires:  libutempter-devel

%{?_kde4_macros_api:Requires: kde4-macros(api) = %{_kde4_macros_api} }
Requires:       oxygen-icon-theme
Requires(post): xdg-utils
Requires(postun): xdg-utils
Requires:       %{name}-doc = %{version}-%{release}

%description
KSig is a graphical tool for keeping track of many different email signatures.
The signatures themselves can be edited through KSig's graphical user 
interface. A command-line interface is then available for generating random 
or daily signatures from a list. The command-line interface makes a suitable 
plugin for generating signatures in external mail clients such as KMail.

%package doc
Group:          System Environment/Libraries
Summary:        Documentation files for ksig
BuildArch:      noarch

%description doc
This package includes the documentation for ksig.

%prep
%setup -qn %{name}-%{version}-svn
%patch0 -p1 -b .cmakelists
%patch1 -p1 -b .docsdir
%patch2 -p1 -b .desktopfile

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} -C %{_target_platform}

# validate desktop file
desktop-file-install --vendor ""                          \
        --dir %{buildroot}%{_datadir}/applications/kde4   \
        %{buildroot}%{_datadir}/applications/kde4/%{name}.desktop


%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
xdg-icon-resource forceupdate --theme hicolor 2> /dev/null || :

%postun
xdg-icon-resource forceupdate --theme hicolor 2> /dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING COPYING.DOC
%{_kde4_bindir}/ksig
%{_kde4_appsdir}/ksig/
%{_kde4_iconsdir}/hicolor/*/apps/ksig.png
%{_datadir}/applications/kde4/ksig.desktop

%files doc
%defattr(-,root,root,-)
%{_docdir}/HTML/en/ksig/

%changelog
* Fri Jun 18 2010 Lukas Tinkl <ltinkl@redhat.com> - 1.1-0.10.20080213
- Resolves: #605070 - RPMdiff run failed for package ksig-1.1-0.8.20080213.1.el6
  (sanitize .desktop file)

* Thu Jun 17 2010 Lukas Tinkl <ltinkl@redhat.com> - 1.1-0.9.20080213
- Resolves: #605070 - RPMdiff run failed for package ksig-1.1-0.8.20080213.1.el6
  (create a noarch doc subpackage)

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.1-0.8.20080213.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.8.20080213
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.7.20080213
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Sebastian Vahl <fedora@deadbabylon.de> - 1.1-0.6.20080213
- re-create patches for rpmbuild's fuzz=0
- BR: libutempter-devel

* Thu Apr 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.1-0.5.20080213
- rebuild (again) for the fixed %%{_kde4_buildtype}

* Wed Apr 02 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.1-0.4.20080213
- omit hard dep on kdelibs
- add scriptlet deps

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.1-0.3.20080213
- rebuild for NDEBUG and _kde4_libexecdir

* Fri Feb 15 2008 Sebastian Vahl <fedora@deadbabylon.de> - 1.1-0.2.20080213
- change group to Applications/Internet

* Wed Feb 13 2008 Sebastian Vahl <fedora@deadbabylon.de> - 1.1-0.1.20080213
- initial version
