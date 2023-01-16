# This file will be configured to contain variables for CPack. These variables
# should be set in the CMake list file of the project before CPack module is
# included. The list of available CPACK_xxx variables and their associated
# documentation may be obtained using
#  cpack --help-variable-list
#
# Some variables are common to all generators (e.g. CPACK_PACKAGE_NAME)
# and some are specific to a generator
# (e.g. CPACK_NSIS_EXTRA_INSTALL_COMMANDS). The generator specific variables
# usually begin with CPACK_<GENNAME>_xxxx.


set(CPACK_BUILD_SOURCE_DIRS "/Users/seonggukim/Desktop/Work/ACON3D/line-renderer-standalone;/Users/seonggukim/Desktop/Work/ACON3D/line-renderer-standalone/cmake-build-debug")
set(CPACK_CMAKE_GENERATOR "Ninja")
set(CPACK_COMPONENT_LIBRARIES_HIDDEN "TRUE")
set(CPACK_COMPONENT_UNSPECIFIED_HIDDEN "TRUE")
set(CPACK_COMPONENT_UNSPECIFIED_REQUIRED "TRUE")
set(CPACK_CREATE_DESKTOP_LINKS "blender-launcher;blender")
set(CPACK_DATE "20230116")
set(CPACK_DEFAULT_PACKAGE_DESCRIPTION_FILE "/Users/seonggukim/Library/Application Support/JetBrains/Toolbox/apps/CLion/ch-0/223.7571.171/CLion.app/Contents/bin/cmake/mac/share/cmake-3.24/Templates/CPack.GenericDescription.txt")
set(CPACK_DEFAULT_PACKAGE_DESCRIPTION_SUMMARY "Blender built using CMake")
set(CPACK_DMG_SLA_USE_RESOURCE_FILE_LICENSE "ON")
set(CPACK_GENERATOR "TBZ2;TGZ;TXZ;TZ")
set(CPACK_IGNORE_FILES "/CVS/;/\\.svn/;/\\.bzr/;/\\.hg/;/\\.git/;\\.swp\$;\\.#;/#")
set(CPACK_INSTALLED_DIRECTORIES "/Users/seonggukim/Desktop/Work/ACON3D/line-renderer-standalone;/")
set(CPACK_INSTALL_CMAKE_PROJECTS "")
set(CPACK_INSTALL_PREFIX "/Users/seonggukim/Desktop/Work/ACON3D/line-renderer-standalone/cmake-build-debug/bin/${BUILD_TYPE}")
set(CPACK_MODULE_PATH "/Users/seonggukim/Desktop/Work/ACON3D/line-renderer-standalone/build_files/cmake/Modules;/Users/seonggukim/Desktop/Work/ACON3D/line-renderer-standalone/build_files/cmake/platform")
set(CPACK_NSIS_DISPLAY_NAME "/Users/seonggukim/Desktop/Work/ACON3D/line-renderer-standalone/cmake-build-debug")
set(CPACK_NSIS_INSTALLER_ICON_CODE "")
set(CPACK_NSIS_INSTALLER_MUI_ICON_CODE "")
set(CPACK_NSIS_INSTALL_ROOT "$PROGRAMFILES")
set(CPACK_NSIS_PACKAGE_NAME "/Users/seonggukim/Desktop/Work/ACON3D/line-renderer-standalone/cmake-build-debug")
set(CPACK_NSIS_UNINSTALL_NAME "Uninstall")
set(CPACK_OSX_SYSROOT "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX13.1.sdk")
set(CPACK_OUTPUT_CONFIG_FILE "/Users/seonggukim/Desktop/Work/ACON3D/line-renderer-standalone/cmake-build-debug/CPackConfig.cmake")
set(CPACK_OVERRIDE_PACKAGENAME "")
set(CPACK_PACKAGE_CONTACT "foundation@blender.org")
set(CPACK_PACKAGE_DEFAULT_LOCATION "/")
set(CPACK_PACKAGE_DESCRIPTION "Blender is the free and open source 3D creation suite software.")
set(CPACK_PACKAGE_DESCRIPTION_FILE "/Users/seonggukim/Library/Application Support/JetBrains/Toolbox/apps/CLion/ch-0/223.7571.171/CLion.app/Contents/bin/cmake/mac/share/cmake-3.24/Templates/CPack.GenericDescription.txt")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Blender built using CMake")
set(CPACK_PACKAGE_EXECUTABLES "blender-launcher;blender")
set(CPACK_PACKAGE_FILE_NAME "Blender-2.96.1-Source")
set(CPACK_PACKAGE_INSTALL_DIRECTORY "/Users/seonggukim/Desktop/Work/ACON3D/line-renderer-standalone/cmake-build-debug")
set(CPACK_PACKAGE_INSTALL_REGISTRY_KEY "/Users/seonggukim/Desktop/Work/ACON3D/line-renderer-standalone/cmake-build-debug")
set(CPACK_PACKAGE_NAME "Blender")
set(CPACK_PACKAGE_RELOCATABLE "true")
set(CPACK_PACKAGE_VENDOR "Blender Foundation")
set(CPACK_PACKAGE_VERSION "2.96.1")
set(CPACK_PACKAGE_VERSION_MAJOR "2")
set(CPACK_PACKAGE_VERSION_MINOR "96")
set(CPACK_PACKAGE_VERSION_PATCH "1")
set(CPACK_RESOURCE_FILE_LICENSE "/Users/seonggukim/Desktop/Work/ACON3D/line-renderer-standalone/COPYING")
set(CPACK_RESOURCE_FILE_README "/Users/seonggukim/Library/Application Support/JetBrains/Toolbox/apps/CLion/ch-0/223.7571.171/CLion.app/Contents/bin/cmake/mac/share/cmake-3.24/Templates/CPack.GenericDescription.txt")
set(CPACK_RESOURCE_FILE_WELCOME "/Users/seonggukim/Library/Application Support/JetBrains/Toolbox/apps/CLion/ch-0/223.7571.171/CLion.app/Contents/bin/cmake/mac/share/cmake-3.24/Templates/CPack.GenericWelcome.txt")
set(CPACK_RPM_PACKAGE_SOURCES "ON")
set(CPACK_SET_DESTDIR "OFF")
set(CPACK_SOURCE_GENERATOR "TBZ2;TGZ;TXZ;TZ")
set(CPACK_SOURCE_IGNORE_FILES "/CVS/;/\\.svn/;/\\.bzr/;/\\.hg/;/\\.git/;\\.swp\$;\\.#;/#")
set(CPACK_SOURCE_INSTALLED_DIRECTORIES "/Users/seonggukim/Desktop/Work/ACON3D/line-renderer-standalone;/")
set(CPACK_SOURCE_OUTPUT_CONFIG_FILE "/Users/seonggukim/Desktop/Work/ACON3D/line-renderer-standalone/cmake-build-debug/CPackSourceConfig.cmake")
set(CPACK_SOURCE_PACKAGE_FILE_NAME "Blender-2.96.1-Source")
set(CPACK_SOURCE_RPM "OFF")
set(CPACK_SOURCE_TBZ2 "ON")
set(CPACK_SOURCE_TGZ "ON")
set(CPACK_SOURCE_TOPLEVEL_TAG "Darwin-Source")
set(CPACK_SOURCE_TXZ "ON")
set(CPACK_SOURCE_TZ "ON")
set(CPACK_SOURCE_ZIP "OFF")
set(CPACK_STRIP_FILES "")
set(CPACK_SYSTEM_NAME "Darwin")
set(CPACK_THREADS "1")
set(CPACK_TOPLEVEL_TAG "Darwin-Source")
set(CPACK_WIX_SIZEOF_VOID_P "8")

if(NOT CPACK_PROPERTIES_FILE)
  set(CPACK_PROPERTIES_FILE "/Users/seonggukim/Desktop/Work/ACON3D/line-renderer-standalone/cmake-build-debug/CPackProperties.cmake")
endif()

if(EXISTS ${CPACK_PROPERTIES_FILE})
  include(${CPACK_PROPERTIES_FILE})
endif()
