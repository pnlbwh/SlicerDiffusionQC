cmake_minimum_required(VERSION 3.5)

project(DiffusionQC)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.github.com/pnlbwh/SlicerDiffusionQC")
set(EXTENSION_CATEGORY "Diffusion.Process")
set(EXTENSION_CONTRIBUTORS "Tashrif Billah and Isaiah Norton, Brigham and Women's Hospital (Harvard Medical School)")
set(EXTENSION_DESCRIPTION "A Slicer module for automated and interactive quality checking of diffusion weighted MRI.")
set(EXTENSION_ICONURL "https://raw.githubusercontent.com/pnlbwh/SlicerDiffusionQC/master/Misc/DiffusionQC-icon-128x128.png")
set(EXTENSION_SCREENSHOTURLS "https://github.com/pnlbwh/SlicerDiffusionQC/raw/master/Misc/DiffusionQC-screenshot.jpg")
set(EXTENSION_DEPENDS "SlicerDMRI") # Specified as a space separated string, a list or 'NA' if any
set(EXTENSION_BUILD_SUBDIRECTORY inner-build)

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})
mark_as_superbuild(Slicer_DIR)

find_package(Git REQUIRED)
mark_as_superbuild(GIT_EXECUTABLE)

#-----------------------------------------------------------------------------
# SuperBuild setup
option(${EXTENSION_NAME}_SUPERBUILD "Build ${EXTENSION_NAME} and the projects it depends on." ON)
mark_as_advanced(${EXTENSION_NAME}_SUPERBUILD)
if(${EXTENSION_NAME}_SUPERBUILD)
  include("${CMAKE_CURRENT_SOURCE_DIR}/SuperBuild.cmake")
  return()
endif()

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(SlicerDiffusionQC)
add_subdirectory(diffusionQC)
add_subdirectory(Test)

## NEXT_MODULE

#-----------------------------------------------------------------------------
# Install extension python packages
install(CODE "message(\"CPack: - Install directory: ${python_packages_DIR}\")")
install(
    DIRECTORY "${python_packages_DIR}/"
    DESTINATION ${Slicer_INSTALL_ROOT}${Slicer_BUNDLE_EXTENSIONS_LOCATION}
    COMPONENT RuntimeLibraries
    )

#-----------------------------------------------------------------------------
set(CPACK_INSTALL_CMAKE_PROJECTS "${CPACK_INSTALL_CMAKE_PROJECTS};${CMAKE_BINARY_DIR};${EXTENSION_NAME};ALL;/")
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
