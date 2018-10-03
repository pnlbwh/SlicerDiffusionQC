add_test(NAME diffusionQCCLI_test 
  COMMAND 
  "${Slicer_LAUNCHER_EXECUTABLE}"
  --launcher-additional-settings "${CMAKE_BINARY_DIR}/AdditionalLauncherSettings.ini"
   --launch
  "${PYTHON_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/run_test.py"
  )
