
Summary: RDF Parser Toolkit for Redland
Name:    raptor2
Version: 2.0.15
Release: 16%{?dist}

License: GPLv2+ or LGPLv2+ or ASL 2.0
Source:  http://download.librdf.org/source/raptor2-%{version}.tar.gz
URL:     http://librdf.org/raptor/

## upstream patches
# https://github.com/dajobe/raptor/commit/590681e546cd9aa18d57dc2ea1858cb734a3863f
Patch1: 0001-Calcualte-max-nspace-declarations-correctly-for-XML-.patch
# https://bugs.librdf.org/mantis/view.php?id=650
Patch2: 0001-CVE-2020-25713-raptor2-malformed-input-file-can-lead.patch

BuildRequires: curl-devel
%if ! 0%{?flatpak}
BuildRequires: gtk-doc
%endif
BuildRequires: libicu-devel
BuildRequires: pkgconfig(libxslt)

# when /usr/bin/rappor moved here  -- rex
Conflicts: raptor < 1.4.21-10

%description
Raptor is the RDF Parser Toolkit for Redland that provides
a set of standalone RDF parsers, generating triples from RDF/XML
or N-Triples.

%package devel
Summary: Development files for %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.


%prep
%autosetup -p1

# hack to nuke rpaths
%if "%{_libdir}" != "/usr/lib"
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif


%build
%configure \
  --disable-static --enable-release \
  --with-icu-config=/usr/bin/icu-config \
%if 0%{?flatpak}
  --disable-gtk-doc \
%endif
  --with-yajl=no

make %{?_smp_mflags}


%install
rm -rf %{buildroot} 

make DESTDIR=%{buildroot} install

## unpackaged files
rm -fv %{buildroot}%{_libdir}/lib*.la


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion raptor2)" = "%{version}"
make check 


%clean
rm -rf %{buildroot} 


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog NEWS README
%doc COPYING* LICENSE.txt LICENSE-2.0.txt
%{_libdir}/libraptor2.so.0*
%{_bindir}/rapper
%{_mandir}/man1/rapper*

%files devel
%doc UPGRADING.html
%{_includedir}/raptor2/
%{_libdir}/libraptor2.so
%{_libdir}/pkgconfig/raptor2.pc
%{_mandir}/man3/libraptor2*
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html/
%{_datadir}/gtk-doc/html/raptor2/


%changelog
* Tue Nov 24 2020 Caolán McNamara <caolanm@redhat.com> - 2.0.15-16
- Resolves: rhbz#1900904 CVE-2020-25713 raptor2: malformed input file can lead to a segfault

* Tue Nov 17 2020 Caolán McNamara <caolanm@redhat.com> - 2.0.15-15
- Resolves: rhbz#1896534 CVE-2017-18926 raptor: heap-based buffer overflow

* Mon Nov 16 2020 Caolán McNamara <caolanm@redhat.com> - 2.0.15-14
- Resolves: rhbz#1896340 Suppress documentation in Flatpak builds

* Tue Aug 21 2018 Caolán McNamara <caolanm@redhat.com> - 2.0.15-13
- Resolves: rhbz#1560206 drop requirement on yajl

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 2.0.15-11
- Rebuild for ICU 60.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 2.0.15-7
- rebuild for ICU 57.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 2.0.15-5
- rebuild for ICU 56.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 18 2015 Rex Dieter <rdieter@fedoraproject.org> 2.0.15-3
- rebuild (gcc5)

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 2.0.15-2
- rebuild for ICU 54.1

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0.15-1
- 2.0.15 (#1159636)

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 2.0.14-4
- rebuild for ICU 53.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 06 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0.14-1
- 2.0.14 (#1094721)

* Tue Mar 04 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0.13-1
- 2.0.13

* Wed Feb 12 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0.9-3
- rebuild (libicu)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0.9-1
- 2.0.9
- BR: libicu-devel

* Tue Feb 19 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0.8-1
- 2.0.8

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 23 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.7-1
- 2.0.7

* Mon Mar 05 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.6-1
- 2.0.6

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.4-3
- rebuild (yajl)
- pkgconfig-style deps

* Sun Jul 31 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.4-2
- include rapper here

* Fri Jul 29 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.4-1
- 2.0.4

* Fri Jul 29 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.3-3
- upstream patch to fix build against newer libcurl

* Tue Jul 26 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.3-2
- -devel: drop Group: tag
- add lot's of %%doc's
- License: GPLv2+ or LGPLv2+ or ASL 2.0 (or newer)

* Sat Jul 23 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.3-1
- first try


