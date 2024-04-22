cmake_minimum_required(VERSION 3.5)

project(DiffusionQC)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://github.com/pnlbwh/SlicerDiffusionQC")
set(EXTENSION_CATEGORY "Diffusion")
set(EXTENSION_CONTRIBUTORS "Tashrif Billah (Brigham & Women's Hospital), Isaiah Norton (Brigham & Women's Hospital), Yogesh Rathi (Brigham & Women's Hospital), Sylvain Bouix (Brigham & Women's Hospital)")
set(EXTENSION_DESCRIPTION "DiffusionQC provides a quality-checking algorithm for diffusion-weighted MRIs, paired with an interactive graphical review tool.")
set(EXTENSION_ICONURL "https://github.com/pnlbwh/SlicerDiffusionQC/raw/master/Misc/DiffusionQC-icon-128x128.png")
set(EXTENSION_SCREENSHOTURLS "https://raw.githubusercontent.com/pnlbwh/SlicerDiffusionQC/master/Misc/DiffusionQC-screenshot.png")
set(EXTENSION_DEPENDS "SlicerDMRI") # Specified as a space separated string, a list or 'NA' if any

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

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
