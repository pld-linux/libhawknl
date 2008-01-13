Summary:	Game oriented network API
Summary(pl.UTF-8):	API sieciowe zorientowane na gry
Name:		libhawknl
Version:	1.68
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://www.hawksoft.com/download/files/HawkNL%(echo %{version} |tr -d .)src.tar.gz
# Source0-md5:	2e4971d422b8c5cadfe2a85527ff2fcf
Patch0:		%{name}-64bit.patch
Patch1:		hawknl-makefile.patch
URL:		http://www.hawksoft.com/hawknl/
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

%description -l pl.UTF-8
HawkNL (NL) to darmowe, mające otwarte źródła, wydane na licencji LGPL
API sieciowe zorientowane na gry. Jest to dosyć niskopoziomowe API,
obudowujące gniazda uniksowe (berkeleyowskie) i Winsock. Jednak
udostępnia także takie elementy jak obsługa wielu systemów
operacyjnych, grupy gniazd, statystyki gniazd, zegar o dużej
dokładności, funkcje do sum kontrolnych, makra do odczytu i zapisu
danych z/do pakietów z konwersją kolejności bajtów w słowie oraz
obsługę wielu transportów sieciowych.

%package devel
Summary:	Header files for HawkNL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki HawkNL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for HawkNL library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki HawkNL.

%package static
Summary:	Static HawkNL library
Summary(pl.UTF-8):	Statyczna biblioteka HawkNL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static HawkNL library.

%description static -l pl.UTF-8
Statyczna biblioteka HawkNL.

%prep
%setup -q -n hawknl%{version}
%patch0 -p1
%patch1 -p1

%{__sed} -i -e 's,\r$,,' src/*.txt

%build
%{__make} -f makefile.linux \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags} -ffast-math%{!?debug: -fomit-frame-pointer}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/hawknl}

%{__make} -f makefile.linux install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=%{_libdir} \
	INCDIR=%{_includedir}/hawknl

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc src/readme.txt src/nlchanges.txt
%attr(755,root,root) %{_libdir}/libNL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libNL.so.1.6

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/hawknl
%{_includedir}/hawknl/nl.h
%{_libdir}/libNL.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libNL.a
