add_library(lingmoappearancecommon${QT_MAJOR_VERSION} OBJECT darklyboxshadowrenderer.cpp)

set_target_properties(lingmoappearancecommon${QT_MAJOR_VERSION} PROPERTIES POSITION_INDEPENDENT_CODE TRUE)

target_link_libraries(lingmoappearancecommon${QT_MAJOR_VERSION}
    PUBLIC
        Qt${QT_MAJOR_VERSION}::Core
        Qt${QT_MAJOR_VERSION}::Gui)
