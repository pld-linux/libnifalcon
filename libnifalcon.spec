#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	swig		# SWIG based Java and Python bindings

Summary:	Open Source Driver for the Novint Falcon Haptic Controller
Summary(pl.UTF-8):	Sterownik z otwartymi źródłami dla kontrolerów haptycznych Novint Falcon
Name:		libnifalcon
Version:	1.1
Release:	4
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/qdot/libnifalcon/releases
Source0:	https://github.com/qdot/libnifalcon/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3723b16749ddfa13fb6ddd1a8a95d58c
Patch0:		%{name}-link.patch
URL:		https://github.com/qdot/libnifalcon
BuildRequires:	boost-devel
BuildRequires:	cmake >= 2.6.0
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXtst-devel
%if %{with swig}
BuildRequires:	jdk
BuildRequires:	python-devel >= 2
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	swig
BuildRequires:	swig-python
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libnifalcon is a development library for the NovInt Falcon haptic
controller, and is an open source, crossplatform alternative to
NovInt's SDK.

%description -l pl.UTF-8
libnifalcon to biblioteka programistyczna dla kontrolerów haptycznych
NovInt Falcon. Jest mającą otwarte źródła, wieloplatformową
alternatywą dla SDK firmy NovInt.

%package devel
Summary:	Header files for libnifalcon library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libnifalcon
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libusb-devel >= 1.0

%description devel
Header files for libnifalcon library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libnifalcon.

%package static
Summary:	Static libnifalcon library
Summary(pl.UTF-8):	Statyczna biblioteka libnifalcon
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libnifalcon library.

%description static -l pl.UTF-8
Statyczna biblioteka libnifalcon.

%package apidocs
Summary:	libnifalcon API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libnifalcon
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libnifalcon library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libnifalcon.

%package -n java-libnifalcon
Summary:	JNI interface to libnifalcon library
Summary(pl.UTF-8):	Interfejs JNI do biblioteki libnifalcon
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}
Requires:	jre

%description -n java-libnifalcon
JNI interface to libnifalcon library.

%description -n java-libnifalcon -l pl.UTF-8
Interfejs JNI do biblioteki libnifalcon.

%package -n python-pynifalcon
Summary:	Python interface to libnifalcon library
Summary(pl.UTF-8):	Interfejs Pythona do biblioteki libnifalcon
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs

%description -n python-pynifalcon
Python interface to libnifalcon library.

%description -n python-pynifalcon -l pl.UTF-8
Interfejs Pythona do biblioteki libnifalcon.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	%{?with_swig:-DBUILD_SWIG_BINDINGS=ON} \
	-DLIBRARY_INSTALL_DIR:PATH=%{_libdir}

%{__make} -j1

%if %{with apidocs}
cd ../doc
doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with swig}
install -d $RPM_BUILD_ROOT%{py_sitedir}
install -p build/lib/libJNIFalcon.so $RPM_BUILD_ROOT%{_libdir}
install -p build/lib/_pynifalcon.so $RPM_BUILD_ROOT%{py_sitedir}
cp -p build/lang/swig/pynifalcon.py $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n java-libnifalcon -p /sbin/ldconfig
%postun	-n java-libnifalcon -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog.txt README.asciidoc linux/40-novint-falcon-udev.rules license/{LICENSE_GMTL_ADDENDUM.txt,LICENSE_LIBNIF_BSD.txt,LICENSE_NOVINT.txt}
%attr(755,root,root) %{_bindir}/barrow_mechanics
%attr(755,root,root) %{_bindir}/falcon_led
%attr(755,root,root) %{_bindir}/falcon_mouse
%attr(755,root,root) %{_bindir}/falcon_test_cli
%attr(755,root,root) %{_bindir}/findfalcons
%attr(755,root,root) %{_bindir}/findfalcons_multi
%attr(755,root,root) %{_libdir}/libnifalcon.so.*.*.*
%attr(755,root,root) %{_libdir}/libnifalcon_cli_base.so.*.*.*
%attr(755,root,root) %{_libdir}/libnifalcon_device_thread.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnifalcon.so
%attr(755,root,root) %{_libdir}/libnifalcon_cli_base.so
%attr(755,root,root) %{_libdir}/libnifalcon_device_thread.so
%{_includedir}/falcon
%{_pkgconfigdir}/libnifalcon.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libnifalcon.a
%{_libdir}/libnifalcon_cli_base.a
%{_libdir}/libnifalcon_device_thread.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/* doc/*.asciidoc
%endif

%if %{with swig}
%files -n java-libnifalcon
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libJNIFalcon.so

%files -n python-pynifalcon
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_pynifalcon.so
%{py_sitedir}/pynifalcon.py[co]
%endif
