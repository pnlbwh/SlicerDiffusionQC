import os, sys
import vtk, qt, ctk, slicer, mrml
from slicer.ScriptedLoadableModule import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gradqclib.slicerUserInteraction import slicerGUI

#
# GradQC
#

class GradQC(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "GradQC"
    self.parent.categories = ["Diffusion.Process"]
    self.parent.dependencies = [ ]
    self.parent.contributors = ["Tashrif Billah and Isaiah Norton, Brigham and Women's Hospital (Harvard Medical School)"]
    self.parent.helpText = """
      This is a complete slicer module for quality checking of diffusion weighted MRI. It 
      identifies bad gradients by comparing distance of each gradient to a median line obtained from 
      KL divergences between consecutive slices. After the above processing, it allows user to manually 
      review each gradient, keep, or discard them.
      
      """
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
      A similar software based on MATLAB environment was earlier developed by a group 
      under the supervision of Yogesh Rathi, Asst. Professor, Harvard Medical School. 
      The MATLAB SignalDropQCTool is available at https://github.com/pnlbwh/SignalDropQCTool
      The SlicerDiffusionQC is a faster, cleaner, and more user oriented version of that software.
      
      """

#
# GradQCWidget
#

class GradQCWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # input/output collapsible area
    #
    inputOutputCollapsibleButton = ctk.ctkCollapsibleButton()
    inputOutputCollapsibleButton.text = "Input/Output"
    self.layout.addWidget(inputOutputCollapsibleButton)

    # Layout within the i/o collapsible button
    ioFormLayout = qt.QFormLayout(inputOutputCollapsibleButton)

    #
    # input volume selector
    #
    self.inputSelector = ctk.ctkPathLineEdit()
    self.inputSelector.filters = ctk.ctkPathLineEdit.Files
    self.inputSelector.setToolTip("Specify the input dwi")
    ioFormLayout.addRow("Input Volume: ", self.inputSelector)

    #
    # input mask selector
    #
    self.maskSelector = ctk.ctkPathLineEdit()
    self.maskSelector.filters = ctk.ctkPathLineEdit.Files
    self.maskSelector.setToolTip("Specify the mask of input dwi")
    ioFormLayout.addRow("Input Volume Mask: ", self.maskSelector)

    #
    # Create Mask
    #
    self.createMaskCheckBox = qt.QCheckBox('Create the mask')
    self.createMaskCheckBox.toolTip= "Check if you don't have a mask or would like to create one"
    self.createMaskCheckBox.enabled = True
    self.createMaskCheckBox.checked = False
    ioFormLayout.addWidget(self.createMaskCheckBox)
    self.createMask= False

    #
    # output directory selector
    #
    self.outputDirSelector = ctk.ctkPathLineEdit()
    self.outputDirSelector.filters = ctk.ctkPathLineEdit.Dirs
    self.outputDirSelector.setToolTip("Specify the output directory, default: same as input dwi directory")
    ioFormLayout.addRow("Output Directory:", self.outputDirSelector)

    #
    # processing collapsible area
    #
    processCollapsibleButton = ctk.ctkCollapsibleButton()
    processCollapsibleButton.text = "Processing"
    self.layout.addWidget(processCollapsibleButton)

    # Layout within the processing collapsible button
    processFormLayout = qt.QFormLayout(processCollapsibleButton)
    processFormLayout.setSpacing(10)

    #
    # Visual Mode
    #
    self.visualMode = qt.QCheckBox('Slicer Visual Mode')
    self.visualMode.toolTip= '''Uncheck for auto processing w/o 
                      Slicer visualization and user interaction'''
    self.visualMode.enabled = True
    self.visualMode.checked = True
    processFormLayout.addWidget(self.visualMode)
    self.autoMode= True # Default initialization, used to trigger Slicer GUI



    #
    # Process Button
    #
    self.applyButton = qt.QPushButton("Process")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    processFormLayout.addRow(self.applyButton)

    #
    # Progress Bar
    #
    self.progressBar = slicer.qSlicerCLIProgressBar( )
    self.progressBar.setToolTip("Progress of the algorithm")
    processFormLayout.addWidget(self.progressBar)


    #
    # Decision Labelling
    #
    self.decisionLabel = qt.QLabel("Gradient information")
    self.decisionLabel.setToolTip("Machine learning decision for current gradient on display")
    self.decisionLabel.setStyleSheet("font: bold")
    processFormLayout.addWidget(self.decisionLabel)

    #
    # Summary Labelling
    #
    self.summaryLabel = qt.QLabel("QC summary")
    self.summaryLabel.setToolTip("Quality check summary")
    self.summaryLabel.setStyleSheet("font: bold")
    processFormLayout.addWidget(self.summaryLabel)

    #
    # Reset Result Button
    #
    self.resetResultsButton = qt.QPushButton("Reset Results")
    self.resetResultsButton.toolTip = "Reset to machine learning results."
    self.resetResultsButton.enabled = True
    processFormLayout.addRow(self.resetResultsButton)


    #
    # Decision collapsible area
    #
    processCollapsibleButton = ctk.ctkCollapsibleButton()
    processCollapsibleButton.text = "Decision"
    self.layout.addWidget(processCollapsibleButton)

    # Layout within the processing collapsible button
    decisionFormLayout = qt.QFormLayout(processCollapsibleButton)
    decisionFormLayout.setSpacing(10)
    # -------------------------------------------------------------------------
    qualityPanel = qt.QHBoxLayout()

    #
    # Keep Gradient Button
    #
    self.keepButton = qt.QPushButton("Keep")
    self.keepButton.toolTip = "Keep the current gradient."
    self.keepButton.enabled = True
    qualityPanel.addWidget(self.keepButton)

    #
    # Discard Gradient Button
    #
    self.discardButton = qt.QPushButton("Discard")
    self.discardButton.toolTip = "Discard the current gradient."
    self.discardButton.enabled = True
    self.discardButton.setStyleSheet("background-color: red")
    qualityPanel.addWidget(self.discardButton)

    decisionFormLayout.addRow(qualityPanel)
    # -------------------------------------------------------------------------


    # -------------------------------------------------------------------------
    confidencePanel = qt.QHBoxLayout()

    #
    # Make it sure Button
    #
    self.sureButton = qt.QPushButton("Sure")
    self.sureButton.toolTip = "Make it sure."
    self.sureButton.enabled = True
    confidencePanel.addWidget(self.sureButton)

    # Make it unsure Button
    #
    self.unsureButton = qt.QPushButton("Unsure")
    self.unsureButton.toolTip = "Make it unsure."
    self.unsureButton.enabled = True
    self.unsureButton.setStyleSheet("background-color: yellow")
    confidencePanel.addWidget(self.unsureButton)

    decisionFormLayout.addRow(confidencePanel)
    # -------------------------------------------------------------------------

    #
    # Next Review Button
    #
    self.nextReviewButton = qt.QPushButton("Next Review")
    self.nextReviewButton.toolTip = "Pull up the next gradient for review."
    self.nextReviewButton.enabled = True
    decisionFormLayout.addRow(self.nextReviewButton)


    #
    # Finish collapsible area
    #
    processCollapsibleButton = ctk.ctkCollapsibleButton()
    processCollapsibleButton.text = "Finish"
    self.layout.addWidget(processCollapsibleButton)

    # Layout within the processing collapsible button
    finishFormLayout = qt.QFormLayout(processCollapsibleButton)

    #
    # Save Result Button
    #
    self.saveResultsButton = qt.QPushButton("Save")
    self.saveResultsButton.toolTip = "Save the results."
    self.saveResultsButton.enabled = True
    finishFormLayout.addRow(self.saveResultsButton)


    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentPathChanged(QString)", self.onSelectInput)
    self.maskSelector.connect("currentPathChanged(QString)", self.onSelectMask)
    self.outputDirSelector.connect("currentPathChanged(QString)", self.onSelectOutput)
    self.visualMode.connect('toggled(bool)', self.onVisualMode)
    self.createMaskCheckBox.connect('toggled(bool)', self.withoutMask)




  def cleanup(self):
    pass

  def withoutMask(self, status):
    self.createMask= status # status= True when checked
    self.applyButton.enabled = self.inputSelector.currentPath \
                               and self.outputDirSelector.currentPath and self.createMask


  def onSelectMask(self):

    # We want to load mask as labelmap outline
    _, self.maskNode = slicer.util.loadLabelVolume(self.maskSelector.currentPath, returnNode=True)
    slicer.util.getNode('vtkMRMLSliceNodeRed').SetUseLabelOutline(1)
    slicer.util.getNode('vtkMRMLSliceNodeYellow').SetUseLabelOutline(1)
    slicer.util.getNode('vtkMRMLSliceNodeGreen').SetUseLabelOutline(1)

    layoutManager = slicer.app.layoutManager()
    for sliceViewName in layoutManager.sliceViewNames():
      sliceLogic = layoutManager.sliceWidget(sliceViewName).sliceLogic()
      compositeNode = sliceLogic.GetSliceCompositeNode()
      compositeNode.SetSliceIntersectionVisibility(1)


    self.applyButton.enabled = self.inputSelector.currentPath \
        and self.outputDirSelector.currentPath and self.maskSelector



  def onSelectInput(self):

    # Load dwi into slicer
    _, self.dwiNode= slicer.util.loadVolume(self.inputSelector.currentPath, returnNode= True)
    self.dwiNode.GetDiffusionWeightedVolumeDisplayNode().InterpolateOff() # RA's prefer looking at the image this way


    self.outputDirSelector.currentPath= os.path.dirname(self.inputSelector.currentPath)
    self.applyButton.enabled = self.inputSelector.currentPath \
        and self.maskSelector.currentPath and self.outputDirSelector.currentPath


  def onSelectOutput(self):
    self.applyButton.enabled = self.inputSelector.currentPath \
        and self.maskSelector.currentPath and self.outputDirSelector.currentPath


  def onVisualMode(self, status):
    self.autoMode= status # status= True when checked


  def onApplyButton(self):

    # Gradient processing
    parameters = {}
    parameters["input"] = self.inputSelector.currentPath
    parameters["mask"] = self.maskSelector.currentPath
    parameters["output"] = self.outputDirSelector.currentPath

    # if self.autoMode= False (check box unchecked), then automatic processing triggers, otherwise visual
    parameters["auto"] = not self.autoMode

    # if result files exist already, don't call cli-module again
    files= os.listdir(os.path.dirname(self.inputSelector.currentPath))
    success= 0
    resultsExist= 0
    for f in files:
      if f.endswith('QC.npy') or f.endswith('confidence.npy') or f.endswith('KLdiv.npy'):
        resultsExist+=1

    if resultsExist==3:
      self.GUI()
      success= 1

    # if results don't exist or autoMode is specified, run cli-module, this may overwrite previous results
    if not success or not self.autoMode: # (not self.autoMode) = True when check box unchecked

        diffusionQCcli = slicer.modules.diffusionqc
        cliNode= slicer.cli.run(diffusionQCcli, None, parameters)

        # Track progress of the algorithm
        self.progressBar.setCommandLineModuleNode(cliNode)

        def observeStatus(caller,_):
          # Check if CLI completed w/o any error
          if caller.GetStatusString()=='Completed' and cliNode.GetErrorText()=='':

            # If mask was not given, created in the pipeline, load now
            if self.createMask:

              # TODO: check if the mask is loading after creation
              # Determine prefix and directory
              directory = os.path.dirname(os.path.abspath(self.inputSelector.currentPath))
              prefix = os.path.basename(self.inputSelector.currentPath.split('.')[0])

              self.maskSelector.currentPath= os.path.join(directory, prefix+'_mask'+'.nrrd')
              self.onSelectMask()

            self.GUI()

        cliNode.AddObserver('ModifiedEvent', observeStatus)


  def GUI(self):

      # If in autoMode, don't call the Slicer GUI below, negative logic used for self.autoMode
      if self.autoMode:  # self.autoMode = True when check box checked

        slicerGUI().slicerUserInterface(self.inputSelector.currentPath, self.dwiNode, self.decisionLabel,
                                        self.summaryLabel, self.discardButton, self.keepButton,
                                        self.sureButton, self.unsureButton,
                                        self.nextReviewButton, self.resetResultsButton, self.saveResultsButton)
