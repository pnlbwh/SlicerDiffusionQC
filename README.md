# SlicerDiffusionQC

The GUI is fully functional. [diffusionQC_real.py](https://github.com/pnlbwh/SlicerDiffusionQC/blob/tashrif-built/cli-modules/diffusionQC/diffusionQC_real.py) is the cli-module.
To circumvent incompatibility of Python 2 in Slicer and Python 3, we wrote a wrapper [diffusionQC.py](https://github.com/pnlbwh/SlicerDiffusionQC/blob/tashrif-built/cli-modules/diffusionQC/diffusionQC.py)
that initiates a subprocess using exploiting Python 3. Make sure to adjust proper python path in [diffusionQC.py](https://github.com/pnlbwh/SlicerDiffusionQC/blob/tashrif-built/cli-modules/diffusionQC/diffusionQC.py)

The [xml wrapper](https://github.com/pnlbwh/SlicerDiffusionQC/blob/tashrif-built/cli-modules/diffusionQC/diffusionQC.xml) communicates between Slicer call and command line call.

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
                                        accepted formats: nhdr, nrrd, nii, and nii.gz, if not provided then looks for
                                        default: dwi_mask.format in input directory, if default is not available, then
                                        creates the mask
    -o, --out VALUE:str                 output directory (default: input dwi directory)
```

The following are example command line calls-

# For automatic processing:
`python ./diffusionQC_real.py -i path/to/input.nrrd -m path/to/mask.nrrd -auto`

`python ./diffusionQC_real.py -i path/to/input.nrrd -m path/to/mask.nrrd -o output/directory -auto`

Saves inputPrefix_modified.nrrd and inputPrefix_QC.txt

# For Slicer GUI manual processing:

First, add the paths on Slicer>Edit>Application Settings>Modules>Additional module paths:

/home/pnl/Downloads/SlicerDiffusionQC/GradQC
/home/pnl/Downloads/SlicerDiffusionQC/cli-modules/diffusionQC

The XML wrapper makes following command line calls and creates temporary files as explained below:

`python ./diffusionQC_real.py -i path/to/input.nrrd -m path/to/mask.nrrd`

`python ./diffusionQC_real.py -i path/to/input.nrrd -m path/to/mask.nrrd -o output/directory`

Saves inputPrefix_decisions.npy, inputPrefix_confidence.npy, and inputPrefix_KLdiv.npy. The temporary files are loaded in 
[Slicer GUI](https://github.com/pnlbwh/SlicerDiffusionQC/tree/tashrif-built/GradQC). After user interaction, when "Save"
is pressed, the results are saved as inputPrefix_modified.nrrd and inputPrefix_QC.txt.

The following are the run mode from [GUI](https://github.com/pnlbwh/SlicerDiffusionQC/blob/tashrif-built/GradQC/GradQC.py):
1. Slicer Visual Mode (checked) and result files exist: does not do [gradient processing](https://github.com/pnlbwh/SlicerDiffusionQC/blob/tashrif-built/cli-modules/diffusionQC/qclib/gradient_process.py) again.
Uses existing result files to display on Slicer, wait for user interaction and 'Save' button.

2. Slicer Visual Mode (checked) and result files do not exist: runs the whole program, uses created result files to display on Slicer, wait for user interaction and 'Save' button.

3. Slicer Visual Mode (unchecked): irrespective of result files' existence, triggers automode and runs the [gradient processing](https://github.com/pnlbwh/SlicerDiffusionQC/blob/tashrif-built/cli-modules/diffusionQC/qclib/gradient_process.py) again.
Since autoMode is triggered, Slicer GUI is not pulled up.


# TODO:
1. Sylvain told to use red color for fail row, yellow color for unsure row

2. The labels should be made colored and bigger

3. If mask does not exist, we have to create that

4. The controls buttons have to be properly grouped

5. (DONE) Speed up using named-tuple inside [gradient_process](https://github.com/pnlbwh/SlicerDiffusionQC/blob/tashrif-built/cli-modules/diffusionQC/qclib/gradient_process.py) instead of class being used now. Now, it takes 4s for gradient_process which is same as that of raw version.

6. (DONE) Sylvain told to write data as out.csv instead of .txt as of now 

7. Show progress bar during gradient_process (takes 52s) and saveResults (takes 36s). Durations are on Tashrif's workstation.










