#-----------------------------------------------------------------------------
set(MODULE_NAME diffusionQCCLI)

set(CLICODE diffusionQC)


set(CLI_DEST "${CMAKE_BINARY_DIR}/${Slicer_CLIMODULES_BIN_DIR}/")
set(CLI_SOURCE "${CMAKE_CURRENT_SOURCE_DIR}/")

add_custom_command(
  OUTPUT "${CLI_DEST}/${CLICODE}.py" "${CLI_DEST}/${CLICODE}.xml"
  COMMAND "${CMAKE_COMMAND}" -E make_directory "${CLI_DEST}"
  COMMAND "${CMAKE_COMMAND}" -E copy "${CLI_SOURCE}/${CLICODE}.py" "${CLI_DEST}"
  COMMAND "${CMAKE_COMMAND}" -E copy "${CLI_SOURCE}/${CLICODE}.xml" "${CLI_DEST}"
  DEPENDS "${CLI_SOURCE}/${CLICODE}.xml" "${CLI_SOURCE}/${CLICODE}.py"
  COMMENT ""
)
add_custom_target(${CLICODE} ALL
  SOURCES "${CLI_SOURCE}/${CLICODE}.py" "${CLI_SOURCE}/${CLICODE}.py"
  DEPENDS "${CLI_DEST}/${CLICODE}.py" "${CLI_DEST}/${CLICODE}.py")

install(FILES ${CLICODE}.py ${CLICODE}.xml
  DESTINATION "${Slicer_INSTALL_CLIMODULES_BIN_DIR}")

set(TESTDATA "${SlicerDMRI_SOURCE_DIR}/Testdata/")
add_test(NAME ${CLICODE}_Test
  COMMAND "${PYTHON_EXECUTABLE}" "${CLI_DEST}/${CLICODE}.py" --test "${TESTDATA}"
  )