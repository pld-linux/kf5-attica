# TODO:
# - runtime Requires if any
# - dir /usr/include/KF5 not packaged

%bcond_without	tests

%define		_state		stable
%define		orgname		attica
%define		kdeframever	5.4
%define		qt_ver		5.3.2

Summary:	A Qt library that implements the Open Collaboration Services API
Name:		kf5-%{orgname}
Version:	5.4.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/%{_state}/frameworks/%{kdeframever}/%{orgname}-%{version}.tar.xz
# Source0-md5:	493c08ce82d5ab34bf2efeb1a01349ab
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qt_ver}
BuildRequires:	Qt5Gui-devel >= %{qt_ver}
BuildRequires:	Qt5Network-devel >= %{qt_ver}
BuildRequires:	Qt5Test-devel >= %{qt_ver}
%if %{with tests}
BuildRequires:	Qt5Gui-devel >= %{qt_ver}
BuildRequires:	Qt5Widgets-devel >= %{qt_ver}
%endif
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Attica is a Qt library that implements the Open Collaboration Services
API version 1.6. The REST API is defined here:
http://freedesktop.org/wiki/Specifications/open-collaboration-services-draft/

It grants easy access to the services such as querying information
about persons and contents. The library is used in KNewStuff3 as
content provider. In order to integrate with KDE's Plasma Desktop, a
platform plugin exists in kdebase.

%package devel
Summary:	Header files for %{orgname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{orgname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{orgname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{orgname}.

%prep
%setup -q -n %{orgname}-%{version}

%build
install -d build
cd build
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/ install \
        DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %ghost %{_libdir}/libKF5Attica.so.5
%attr(755,root,root) %{_libdir}/libKF5Attica.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKF5Attica.so
%{_includedir}/KF5/Attica
%{_includedir}/KF5/attica_version.h
%{_libdir}/cmake/KF5Attica
%{_pkgconfigdir}/libKF5Attica.pc
%{_libdir}/qt5/mkspecs/modules/qt_Attica.pri
