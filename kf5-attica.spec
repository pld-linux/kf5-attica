# TODO:
# - proper place for *.pri,
# - set ECM_MKSPECS_INSTALL_DIR in kde5-extra-cmake-modules
# - runtime Requires if any
# - dir /usr/include/KF5 not packaged
%define         _state          stable
%define		orgname		attica

Summary:	A Qt library that implements the Open Collaboration Services API
Name:		kf5-%{orgname}
Version:	5.0.0
Release:	0.1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	ftp://ftp.kde.org/pub/kde/%{_state}/frameworks/%{version}/%{orgname}-%{version}.tar.xz
# Source0-md5:	73d1d1953b12eda42f6f4010df889b73
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= 5.2.0
BuildRequires:	Qt5Gui-devel >= 5.3.1
BuildRequires:	Qt5Network-devel
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5Widgets-devel >= 5.2.0
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= 1.0.0
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

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
	-DBIN_INSTALL_DIR=%{_bindir} \
	-DKCFG_INSTALL_DIR=%{_datadir}/config.kcfg \
	-DPLUGIN_INSTALL_DIR=%{qt5dir}/plugins \
	-DQT_PLUGIN_INSTALL_DIR=%{qt5dir}/plugins \
	-DQML_INSTALL_DIR=%{qt5dir}/qml \
	-DIMPORTS_INSTALL_DIR=%{qt5dirs}/imports \
	-DSYSCONF_INSTALL_DIR=%{_sysconfdir} \
	-DLIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DKF5_LIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DKF5_INCLUDE_INSTALL_DIR=%{_includedir} \
	-DECM_MKSPECS_INSTALL_DIR=%{qt5dir}/mkspecs/modules \
	-D_IMPORT_PREFIX=%{_prefix} \
	..
%{__make}

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
%attr(755,root,root) %{_libdir}/libKF5Attica.so.5.0.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/Attica
%{_includedir}/KF5/attica_version.h
%{_libdir}/cmake/KF5Attica
%attr(755,root,root) %{_libdir}/libKF5Attica.so
%{_pkgconfigdir}/libKF5Attica.pc
%{qt5dir}/mkspecs/modules/qt_Attica.pri
