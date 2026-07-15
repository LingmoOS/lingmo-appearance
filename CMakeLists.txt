cmake_minimum_required(VERSION 3.16)

# Get version
file(READ "${CMAKE_SOURCE_DIR}/VERSION" VER_RAW)
string(STRIP ${VER_RAW} VER)

project(
    LingmoAppearance
    DESCRIPTION "Adaptive Qt Widgets style and KWin decoration for Lingmo."
    VERSION ${VER}
)

set(KF5_MIN_VERSION "5.102.0")
set(KF6_MIN_VERSION "6.10.0")
set(KDE_COMPILERSETTINGS_LEVEL "5.82")
set(QT5_MIN_VERSION "5.15.2")
set(QT_MIN_VERSION "6.7.0")

include(GenerateExportHeader)
include(WriteBasicConfigVersionFile)
include(FeatureSummary)
include(GNUInstallDirs)

find_package(ECM ${KF6_MIN_VERSION} REQUIRED NO_MODULE)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${ECM_MODULE_PATH}  ${CMAKE_SOURCE_DIR}/cmake)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


include(CMakePackageConfigHelpers)
include(ECMInstallIcons)
include(KDECompilerSettings NO_POLICY_SCOPE)
include(KDEClangFormat)
include(KDEGitCommitHooks)

include(GtkUpdateIconCache)

option(FOR_FLATPAK "Build LingmoAppearance for Flatpak" OFF)
option(BUILD_QT5 "Build the legacy Qt 5 style plugin (unsupported)" OFF)
option(BUILD_QT6 "Build the Qt 6 style plugin" ON)
option(BUILD_SETTINGS "Build the Qt 6 style KCM and settings application" ON)
option(BUILD_DECORATION "Build the KWin 6 / KDecoration3 window decoration" ON)
option(BUILD_COLOR_SCHEMES "Install bundled color schemes" ON)

# Compatibility for existing Flatpak and downstream build invocations.
if(DEFINED WITH_DECORATIONS)
    message(DEPRECATION "WITH_DECORATIONS is deprecated; use BUILD_DECORATION instead.")
    set(BUILD_DECORATION "${WITH_DECORATIONS}" CACHE BOOL
        "Build the KWin 6 / KDecoration3 window decoration" FORCE)
endif()

set(QT_NO_CREATE_VERSIONLESS_TARGETS ON)
set(QT_NO_CREATE_VERSIONLESS_FUNCTIONS ON)

if(WIN32 OR APPLE OR FOR_FLATPAK)
    set(BUILD_DECORATION OFF CACHE BOOL
        "Build the KWin 6 / KDecoration3 window decoration" FORCE)
endif()

function(build_qt5)
    set(QT_MAJOR_VERSION 5)
    include(KDEInstallDirs5)
    include(KDECMakeSettings)
    find_package(Qt5 ${QT5_MIN_VERSION} REQUIRED CONFIG COMPONENTS Widgets DBus)
    find_package(KF5 ${KF5_MIN_VERSION} REQUIRED COMPONENTS
            CoreAddons
            Config
            GuiAddons
            I18n
            IconThemes
            WindowSystem)
        if(NOT WIN32 AND NOT APPLE)
            find_package(KF5KCMUtils ${KF5_MIN_VERSION})
            set_package_properties(KF5KCMUtils PROPERTIES
                TYPE REQUIRED
                DESCRIPTION "Helps create configuration modules"
                PURPOSE "KCMUtils used for the configuration modules or the decoration and Qt Style"
            )
        endif()

    find_package(Qt5 ${QT5_MIN_VERSION} OPTIONAL_COMPONENTS Quick)
        if(${Qt5Quick_FOUND})
        find_package(KF5 ${KF5_MIN_VERSION} REQUIRED COMPONENTS Kirigami2)
        endif()

    find_package(KF5FrameworkIntegration ${KF5_MIN_VERSION} CONFIG )
        set_package_properties(KF${QT_MAJOR_VERSION}FrameworkIntegration PROPERTIES
            DESCRIPTION "KF${QT_MAJOR_VERSION} Framework Integration"
            URL "https://projects.kde.org/projects/frameworks/frameworkintegration"
            TYPE OPTIONAL
            PURPOSE "Required to use KStyle convenience functionalities in style")

    set(DARKLY_HAVE_KSTYLE ${KF5FrameworkIntegration_FOUND})
    set(DARKLY_HAVE_QTQUICK ${Qt5Quick_FOUND})


    #add_subdirectory(colors)
    add_subdirectory(libdarklycommon libdarklycommon5)
    add_subdirectory(kstyle kstyle5)
    #add_subdirectory(misc)
    unset(QUERY_EXECUTABLE CACHE)
endfunction()
if(BUILD_QT5)
    message("-- **** Build QT5 - On ****")
    build_qt5()
endif()

function(build_qt6)
    set(QT_MAJOR_VERSION 6)
    include(KDEInstallDirs6)
    include(KDECMakeSettings)

    find_package(Qt6 ${QT_MIN_VERSION} REQUIRED CONFIG COMPONENTS Widgets DBus Quick QuickWidgets)
    find_package(KF6 ${KF6_MIN_VERSION} REQUIRED COMPONENTS
            CoreAddons
            ColorScheme
            Config
            GuiAddons
            I18n
            IconThemes
            WindowSystem)
        if((BUILD_SETTINGS OR BUILD_DECORATION) AND NOT WIN32 AND NOT APPLE)
            find_package(KF6KCMUtils ${KF6_MIN_VERSION} REQUIRED)
        endif()

    find_package(KF6KirigamiPlatform ${KF6_MIN_VERSION} REQUIRED)

    find_package(KF6FrameworkIntegration ${KF6_MIN_VERSION} CONFIG )
        set_package_properties(KF${QT_MAJOR_VERSION}FrameworkIntegration PROPERTIES
            DESCRIPTION "KF${QT_MAJOR_VERSION} Framework Integration"
            URL "https://projects.kde.org/projects/frameworks/frameworkintegration"
            TYPE OPTIONAL
            PURPOSE "Required to use KStyle convenience functionalities in style")

    set(DARKLY_HAVE_KSTYLE ${KF6FrameworkIntegration_FOUND})
    set(DARKLY_HAVE_QTQUICK ON)


    add_library(Qt::Core ALIAS Qt6::Core)
    add_library(Qt::Gui ALIAS Qt6::Gui)
    add_library(Qt::OpenGL ALIAS Qt6::OpenGL)
    add_library(Qt::Network ALIAS Qt6::Network)
    if(Qt6_VERSION_MINOR GREATER 6)
        add_library(Qt::PlatformModuleInternal ALIAS Qt6::PlatformModuleInternal)
    endif()

    add_subdirectory(libdarklycommon libdarklycommon6)
    add_subdirectory(kstyle kstyle6)

    if(BUILD_DECORATION)
        find_package(KDecoration3 REQUIRED)
        add_subdirectory(kdecoration)
    endif()

    set(CMAKE_INSTALL_DEFAULT_COMPONENT_NAME Common)
    ki18n_install(po)

    # create a Config.cmake and a ConfigVersion.cmake file and install them
    include(ECMSetupVersion)
    ecm_setup_version(${PROJECT_VERSION} VARIABLE_PREFIX LINGMOAPPEARANCE
                    PACKAGE_VERSION_FILE "${CMAKE_CURRENT_BINARY_DIR}/LingmoAppearanceConfigVersion.cmake"
                    VERSION_HEADER "${CMAKE_CURRENT_BINARY_DIR}/kstyle6/config/darklystyleversion.h"
    )

    set(CMAKECONFIG_INSTALL_DIR "${KDE_INSTALL_CMAKEPACKAGEDIR}/LingmoAppearance")

    if (NOT FOR_FLATPAK)
        configure_package_config_file("${CMAKE_CURRENT_SOURCE_DIR}/DarklyConfig.cmake.in"
                                        "${CMAKE_CURRENT_BINARY_DIR}/LingmoAppearanceConfig.cmake"
                                        PATH_VARS KDE_INSTALL_FULL_DATADIR
                                        INSTALL_DESTINATION ${CMAKECONFIG_INSTALL_DIR}
                                    )

        install(FILES "${CMAKE_CURRENT_BINARY_DIR}/LingmoAppearanceConfig.cmake"
                      "${CMAKE_CURRENT_BINARY_DIR}/LingmoAppearanceConfigVersion.cmake"
                DESTINATION "${CMAKECONFIG_INSTALL_DIR}"
                COMPONENT Common
        )
    endif()
    unset(QUERY_EXECUTABLE CACHE)
endfunction()

if(BUILD_QT6)
    message("-- **** Build QT6 - On ****")
    build_qt6()
endif()

function(build_colors)
    include(KDEInstallDirs)
    add_subdirectory(colors)
endfunction()

if(BUILD_COLOR_SCHEMES AND NOT FOR_FLATPAK)
    build_colors()
endif()

# add clang-format target for all our real source files
file(GLOB_RECURSE ALL_CLANG_FORMAT_SOURCE_FILES *.cpp *.h)
kde_clang_format(${ALL_CLANG_FORMAT_SOURCE_FILES})
kde_configure_git_pre_commit_hook(CHECKS CLANG_FORMAT)

feature_summary(WHAT ALL INCLUDE_QUIET_PACKAGES FATAL_ON_MISSING_REQUIRED_PACKAGES)
