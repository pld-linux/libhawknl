Summary:	HawkNL is a free, open source, game oriented network API
Name:		libhawknl
Version:	1.68
Release:	1
License:	LGPL
Group:		Libraries
URL:		http://www.hawksoft.com/hawknl/
Source0:	http://www.sonic.net/~philf/download/HawkNL168src.tar.gz
# Source0-md5:	2e4971d422b8c5cadfe2a85527ff2fcf
Patch0:		%{name}-64bit.patch
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HawkNL is a free, open source, game oriented network API released
under the GNU Library General Public License (LGPL). HawkNL (NL) is a
fairly low level API, a wrapper over Berkeley/Unix Sockets and
Winsock. But NL also provides other features including support for
many OSs, groups of sockets, socket statistics, high accuracy timer,
CRC functions, macros to read and write data to packets with endian
conversion, and support for multiple network transports.

%package devel
Summary:	Include Files and Libraries mandatory for development with hawknl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The hawknl-devel package contains libraries and header files for
developing applications that use hawknl.

%package static
Summary:	Static hawknl library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static hawknl library.

%prep
%setup -q -n hawknl%{version}
%patch0 -p1

%{__sed} -i -e 's,\r$,,' src/*.txt

# some fixups
%{__sed} -i 's|ln -s $(LIBDIR)/$(OUTPUT)|ln -s $(OUTPUT)|g' \
	src/makefile.linux
%{__sed} -i 's|-soname,NL.so|-soname,libNL.so|' \
	src/makefile.linux

%build
%{__make} -f makefile.linux \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags} -D_XOPEN_SOURCE=500"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_includedir}/hawknl
%{__make} -f makefile.linux install \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
	INCDIR=$RPM_BUILD_ROOT%{_includedir}/hawknl

rm $RPM_BUILD_ROOT%{_libdir}/NL.so

%clean
rm -rf  $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc src/readme.txt src/nlchanges.txt
%attr(755,root,root) %{_libdir}/libNL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libNL.so.1
%attr(755,root,root) %ghost %{_libdir}/libNL.so.1.6

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/hawknl
%{_includedir}/hawknl/*
%{_libdir}/libNL.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libNL.a
