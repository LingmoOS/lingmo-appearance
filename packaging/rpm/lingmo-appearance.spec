Name:           lingmo-appearance
Version:        0.5.25
Release:        1%{?dist}
Summary:        Adaptive Qt 6 widget style and KWin 6 decoration for Lingmo

License:        GPL-2.0-or-later
URL:            https://github.com/LingmoOS/lingmo-appearance
Source0:        %{name}-%{version}.tar.xz

# Fedora-family dependency names. Other RPM distributions can map these to
# their Qt 6, KDE Frameworks 6 and KDecoration3 development packages.
BuildRequires:  cmake >= 3.16
BuildRequires:  extra-cmake-modules >= 6.10
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  qt6-qtbase-devel >= 6.7
BuildRequires:  qt6-qtdeclarative-devel >= 6.7
BuildRequires:  kdecoration-devel
BuildRequires:  kf6-kcoreaddons-devel >= 6.10
BuildRequires:  kf6-kcolorscheme-devel >= 6.10
BuildRequires:  kf6-kconfig-devel >= 6.10
BuildRequires:  kf6-kcmutils-devel >= 6.10
BuildRequires:  kf6-frameworkintegration-devel >= 6.10
BuildRequires:  kf6-kguiaddons-devel >= 6.10
BuildRequires:  kf6-ki18n-devel >= 6.10
BuildRequires:  kf6-kiconthemes-devel >= 6.10
BuildRequires:  kf6-kwindowsystem-devel >= 6.10
BuildRequires:  kf6-kirigami-devel >= 6.10

# The primary package is a metapackage for the complete appearance stack.
Requires:       %{name}-common = %{version}-%{release}
Requires:       %{name}-qt6 = %{version}-%{release}
Requires:       %{name}-settings = %{version}-%{release}
Requires:       %{name}-decoration = %{version}-%{release}

%description
Metapackage that installs the complete Lingmo Qt 6 appearance stack.

%package common
Summary:        Shared data for LingmoAppearance
BuildArch:      noarch

%description common
Shared color-scheme data and CMake package metadata for LingmoAppearance.

%package qt6
Summary:        Lingmo Qt 6 widget style plugin
Requires:       %{name}-common = %{version}-%{release}

%description qt6
Qt 6 QStyle plugin registered under the Lingmo style key.

%package settings
Summary:        Lingmo appearance settings application and widget-style KCM
Requires:       %{name}-qt6 = %{version}-%{release}

%description settings
The Qt 6 widget-style configuration module and settings application.

%package decoration
Summary:        Lingmo KWin 6 window decoration
Requires:       %{name}-common = %{version}-%{release}

%description decoration
KDecoration3 plugin and configuration module for KWin 6.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -GNinja -DBUILD_QT5=OFF -DBUILD_QT6=ON -DBUILD_SETTINGS=ON -DBUILD_DECORATION=ON -DBUILD_COLOR_SCHEMES=ON -DBUILD_TESTING=OFF
%cmake_build

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} cmake --install %{__cmake_builddir} --component Common
DESTDIR=%{buildroot} cmake --install %{__cmake_builddir} --component Qt6Style
DESTDIR=%{buildroot} cmake --install %{__cmake_builddir} --component Settings
DESTDIR=%{buildroot} cmake --install %{__cmake_builddir} --component Decoration

%files common
%license COPYING
%doc AUTHORS README.md
%{_datadir}/color-schemes/Lingmo.colors
%{_libdir}/cmake/LingmoAppearance/

%files qt6
%{_qt6_plugindir}/styles/lingmostyle6.so
%{_datadir}/kstyle/themes/lingmo.themerc

%files settings
%{_bindir}/lingmo-appearance-settings6
%{_qt6_plugindir}/kstyle_config/lingmostyleconfig.so
%{_datadir}/icons/hicolor/scalable/apps/lingmo-appearance-settings.svgz

%files decoration
%{_qt6_plugindir}/org.kde.kdecoration3/org.lingmo.appearance.so
%{_qt6_plugindir}/org.kde.kdecoration3/kcm_lingmoappearancedecoration.so
%{_datadir}/kservices6/lingmoappearance-decorationconfig.desktop

%files
%license COPYING

%changelog
* Wed Jul 15 2026 Lingmo OS Team <team@lingmo.org> - 0.5.25-1
- Initial Qt 6 and KWin 6 packaging
