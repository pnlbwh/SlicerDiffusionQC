set(proj python-diffusionqclib)

#-----------------------------------------------------------------------------
# Set dependency list
set(${proj}_DEPENDENCIES "")

# Include dependent projects if any
ExternalProject_Include_Dependencies(${proj} PROJECT_VAR proj DEPENDS_VAR ${proj}_DEPENDENCIES)

#-----------------------------------------------------------------------------
# Project to install diffusionqclib
set(python_packages_DIR "${CMAKE_BINARY_DIR}/python-packages-install")
file(TO_NATIVE_PATH ${python_packages_DIR} python_packages_DIR_NATIVE_DIR)

set(_install_pynrrd COMMAND ${CMAKE_COMMAND}
    -E env
    PYTHONNOUSERSITE=1
    ${PYTHON_EXECUTABLE} -m pip install git+https://github.com/mhe/pynrrd.git@eeb4df8dc96eff2d6aaa0e419e04c469daf78cdc
                         --prefix ${python_packages_DIR_NATIVE_DIR} --upgrade
    )

set(_install_diffusionqclib COMMAND ${CMAKE_COMMAND}
    -E env
    PYTHONNOUSERSITE=1
    ${PYTHON_EXECUTABLE} -m pip install . --prefix ${python_packages_DIR_NATIVE_DIR} --upgrade
    )

ExternalProject_Add(${proj}
    ${${proj}_EP_ARGS}
    SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/diffusionqclib
    BUILD_IN_SOURCE 1
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    INSTALL_COMMAND ${CMAKE_COMMAND} -E  echo_append ""
    ${_install_pynrrd}
    ${_install_diffusionqclib}
    DEPENDS
        ${${proj}_DEPENDENCIES}
    )

#-----------------------------------------------------------------------------
# Launcher voodoo to get the PYTHONPATH we need
ExternalProject_GenerateProjectDescription_Step(${proj})

set(${proj}_PYTHONPATH_LAUNCHER_BUILD
    ${python_packages_DIR}/${PYTHON_STDLIB_SUBDIR}
    ${python_packages_DIR}/${PYTHON_STDLIB_SUBDIR}/lib-dynload
    ${python_packages_DIR}/${PYTHON_SITE_PACKAGES_SUBDIR}
    )

mark_as_superbuild(
    VARS ${proj}_PYTHONPATH_LAUNCHER_BUILD
    LABELS "PYTHONPATH_LAUNCHER_BUILD"
    )
mark_as_superbuild(python_packages_DIR:PATH)


#-----------------------------------------------------------------------------
# Clean the EP stamp so 'make clean' is more useful for testing
ExternalProject_Get_Property(${proj} STAMP_DIR)
set_directory_properties(PROPERTIES ADDITIONAL_MAKE_CLEAN_FILES "${STAMP_DIR}")

