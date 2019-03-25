#
# Conditional build:
%bcond_without	tests		# build without tests

# TODO:
# - runtime Requires if any

%define		kdeframever	5.56
%define		qtver		5.9.0
%define		kfname		attica
Summary:	A Qt library that implements the Open Collaboration Services API
Name:		kf5-%{kfname}
Version:	5.56.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	b0b58d82e5047796eeebdac4bf969aa4
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
%if %{with tests}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
%endif
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Attica is a Qt library that implements the Open Collaboration Services
API version 1.6. The REST API is defined here:
<http://freedesktop.org/wiki/Specifications/open-collaboration-services-draft/>.

It grants easy access to the services such as querying information
about persons and contents. The library is used in KNewStuff3 as
content provider. In order to integrate with KDE's Plasma Desktop, a
platform plugin exists in kdebase.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%{?with_tests:%ninja_build test}

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_libdir}/libKF5Attica.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libKF5Attica.so.5
/etc/xdg/attica.categories

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKF5Attica.so
%{_includedir}/KF5/Attica
%{_includedir}/KF5/attica_version.h
%{_libdir}/cmake/KF5Attica
%{_pkgconfigdir}/libKF5Attica.pc
%{_libdir}/qt5/mkspecs/modules/qt_Attica.pri
