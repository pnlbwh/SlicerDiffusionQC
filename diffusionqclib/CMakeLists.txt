set(proj python-diffusionqclib)

#-----------------------------------------------------------------------------
# Project to install diffusionqclib
set(python_packages_DIR "${CMAKE_BINARY_DIR}/python-packages-install")
file(TO_NATIVE_PATH ${python_packages_DIR} python_packages_DIR_NATIVE_DIR)

set(_install_diffusionqclib COMMAND ${CMAKE_COMMAND}
    -E env
    PYTHONNOUSERSITE=1
    ${PYTHON_EXECUTABLE} -m pip install . --prefix ${python_packages_DIR_NATIVE_DIR} --upgrade
    )

ExternalProject_Add(${proj}
    ${${proj}_EP_ARGS}
    SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/
    BUILD_IN_SOURCE 1
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    INSTALL_COMMAND ${CMAKE_COMMAND} -E  echo_append ""
    ${_install_diffusionqclib}
    DEPENDS
    )