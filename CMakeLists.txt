cmake_minimum_required(VERSION 3.5)

project(SlicerDiffusionQC)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/SlicerDiffusionQC")
set(EXTENSION_CATEGORY "Diffusion.Process")
set(EXTENSION_CONTRIBUTORS "Tashrif Billah and Isaiah Norton, Brigham and Women's Hospital (Harvard Medical School)")
set(EXTENSION_DESCRIPTION "A complete slicer module for quality checking of diffusion weighted MRI")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/SlicerDiffusionQC.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/SlicerDiffusionQC/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a space separated string, a list or 'NA' if any

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(SlicerDiffusionQC)
add_subdirectory(diffusionQC)
## NEXT_MODULE

add_subdirectory(diffusionqclib)

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
