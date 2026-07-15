### configuration plugin
set(CMAKE_INSTALL_DEFAULT_COMPONENT_NAME Settings)
add_definitions(-DTRANSLATION_DOMAIN=\"darkly_style_config\")
set(kstyle_darkly_config_PART_SRCS darklystyleconfig.cpp)

set(kstyle_darkly_config_PART_SRCS ${kstyle_darkly_config_PART_SRCS} darklystyleconfigmodule.cpp)

kconfig_add_kcfg_files(kstyle_darkly_config_PART_SRCS ../darklystyleconfigdata.kcfgc)
set(kstyle_darkly_config_PART_FORMS ui/darklystyleconfig.ui)
ki18n_wrap_ui(kstyle_darkly_config_PART_FORMS_HEADERS ${kstyle_darkly_config_PART_FORMS})

kcoreaddons_add_plugin(lingmostyleconfig SOURCES
    ${kstyle_darkly_config_PART_SRCS}
    ${kstyle_darkly_config_PART_FORMS_HEADERS}
    INSTALL_NAMESPACE "kstyle_config"
)

target_link_libraries(lingmostyleconfig Qt6::Core Qt6::Gui Qt6::Widgets Qt6::DBus)
target_link_libraries(lingmostyleconfig KF6::CoreAddons KF6::ConfigCore KF6::ConfigWidgets KF6::I18n)
if(QT_MAJOR_VERSION STREQUAL "6")
    target_link_libraries(lingmostyleconfig KF6::KCMUtils)
endif()
kcmutils_generate_desktop_file(lingmostyleconfig)

set(darkly_settings_SOURCES main.cpp)
add_executable(lingmo-appearance-settings ${darkly_settings_SOURCES})
target_link_libraries(lingmo-appearance-settings Qt6::Core Qt6::Gui Qt6::Widgets)
target_link_libraries(lingmo-appearance-settings KF6::I18n KF6::KCMUtils KF6::CoreAddons)

set_target_properties(lingmo-appearance-settings PROPERTIES OUTPUT_NAME lingmo-appearance-settings${QT_MAJOR_VERSION})

install(TARGETS lingmo-appearance-settings ${KDE_INSTALL_TARGETS_DEFAULT_ARGS}
        COMPONENT Settings)

# icon
ecm_install_icons(ICONS sc-apps-lingmo-appearance-settings.svgz
    DESTINATION ${KDE_INSTALL_ICONDIR}
    THEME hicolor )


