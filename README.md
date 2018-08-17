# SlicerDiffusionQC


This is a complete slicer module for quality checking of diffusion weighted MRI. It 
identifies bad gradients by comparing distance of each gradient to a median line obtained from 
KL divergences between consecutive slices. After the above processing, it allows user to manually 
review each gradient, keep, or discard them.

A similar software based on MATLAB environment was earlier developed by a group 
under the supervision of Yogesh Rathi, Asst. Professor, Harvard Medical School. 
The MATLAB SignalDropQCTool is available at [](https://github.com/pnlbwh/SignalDropQCTool)
The SlicerDiffusionQC is a faster, cleaner, and more user oriented version of that software.

Developed by Tashrif Billah and Isaiah Norton, Brigham and Women's Hospital (Harvard Medical School)



# File description

Clone the repository `git clone https://github.com/pnlbwh/SlicerDiffusionQC.git` in your local directory.


[diffusionQC.py](https://github.com/pnlbwh/SlicerDiffusionQC/blob/speed-up/cli-modules/diffusionQC/diffusionQC.py) is the cli-module that can be run from the command line. On the other hand, [GradQC.py](https://github.com/pnlbwh/SlicerDiffusionQC/blob/speed-up/GradQC/GradQC.py) is the GUI module that is loaded into Slicer.


The [xml wrapper](https://github.com/pnlbwh/SlicerDiffusionQC/blob/tashrif-built/speed-up/diffusionQC/diffusionQC.xml) communicates between Slicer and command line call.

# Usage


```
Checks the quality of gradients in a diffusion weighted mri.
Predicts each gradient as pass or fail.

Usage:
    diffusionQC_real.py [SWITCHES] 

Meta-switches:
    -h, --help                          Prints this help message and quits
    --help-all                          Print help messages of all subcommands and quit
    -v, --version                       Prints the program's version and quits

Switches:
    -a, --auto                          Turn on this flag for command line/automatic processing w/o Slicer
                                        visualization
    -i, --input VALUE:ExistingFile      diffusion weighted mri e.g. dwi.nrrd or path/to/dwi.nrrd, accepted formats:
                                        nhdr, nrrd, nii, and nii.gz
    -m, --mask VALUE:ExistingFile       mask for the diffusion weighted mri, e.g. mask.nrrd or path/to/mask.nrrd,
                                        accepted formats: nhdr, nrrd, nii, and nii.gz, if not provided then
                                        creates the mask
    -o, --out VALUE:str                 output directory (default: input dwi directory)

```

The following are example command line calls:

# For automatic processing:

1. One time dependencies installation:

`pip install nibabel, pynrrd, nibabel`


2. If you do not have a mask and you want the pipeline to create one, edit the `config.ini` file from where executables will be used in the process.


3. After dependencies are solved, you can run the CLI module:

`python ./cli-modules/diffusionQC.py -i path/to/input.nrrd -a`

`python ./cli-modules/diffusionQC.py -i path/to/input.nrrd -m path/to/mask.nrrd -a`

`python ./cli-modules/diffusionQC.py -i path/to/input.nrrd -m path/to/mask.nrrd -o output/directory -a`

Saves `inputPrefix_modified.nrrd` and `inputPrefix_QC.txt`

# For Slicer GUI manual processing:

1. Open the Slicer Python Interactor and install the dependencies:

```
from pip._internal import main as pipmain
pipmain(['install', 'pynrrd', 'nibabel', 'plumbum'])

```

2. Add the following path to `Slicer>Edit>Application Settings>Modules>Additional module paths`:

`/home/pnl/Downloads/SlicerDiffusionQC/GradQC`

If no error shows up the Python console, all dependencies are solved and your loading is successful.

3. Type `GradQC` in `Slicer>Modules` search icon, and select it from the drop down menu.


4. Specify the input image, input mask, and output directory. Hit `Process`. Based on the power of your machine, it might take a few minutes to see the results on Slicer. The rest should be interactive.


The XML wrapper makes following command line calls and creates temporary files as explained below:

`python ./diffusionQC_real.py -i path/to/input.nrrd -m path/to/mask.nrrd`

`python ./diffusionQC_real.py -i path/to/input.nrrd -m path/to/mask.nrrd -o output/directory`

Saves `inputPrefix_decisions.npy, inputPrefix_confidence.npy, and inputPrefix_KLdiv.npy`. The temporary files are loaded in 
[Slicer GUI](https://github.com/pnlbwh/SlicerDiffusionQC/tree/speed-up/GradQC). After user interaction, when "Save"
is pressed, the results are saved as `inputPrefix_modified.nrrd and inputPrefix_QC.txt`.

The following are run modes from [GUI](https://github.com/pnlbwh/SlicerDiffusionQC/blob/tashrif-built/GradQC/GradQC.py):

i) Slicer Visual Mode (checked) and result files exist: does not do [gradient processing](https://github.com/pnlbwh/SlicerDiffusionQC/blob/speed-up/cli-modules/diffusionQC/qclib/gradient_process.py) again.
Uses existing result files to display on Slicer, wait for user interaction and 'Save' button.

ii) Slicer Visual Mode (checked) and result files do not exist: runs the whole program, uses created result files to display on Slicer, wait for user interaction and 'Save' button.

iii) Slicer Visual Mode (unchecked): irrespective of result files' existence, triggers automode and runs the [gradient processing](https://github.com/pnlbwh/SlicerDiffusionQC/blob/speed-up/cli-modules/diffusionQC/qclib/gradient_process.py) again.
Since autoMode is triggered, Slicer GUI is not pulled up.



