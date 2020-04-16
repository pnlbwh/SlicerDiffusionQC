![](Misc/pnl-bwh-hms.png)

[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.2576412.svg)](https://doi.org/10.5281/zenodo.2576412) [![Python](https://img.shields.io/badge/Python-2.7%20%7C%203.6-green.svg)]() [![Platform](https://img.shields.io/badge/Platform-linux--64%20%7C%20osx--64-orange.svg)]()

Developed by Tashrif Billah and Isaiah Norton, Brigham and Women's Hospital (Harvard Medical School).

Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [SlicerDiffusionQC](#slicerdiffusionqc)
   * [Citation](#citation)
   * [Installation](#installation)
   * [Usage](#usage)
   * [Tests](#tests)
   * [Automatic processing](#automatic-processing)
   * [Visual processing](#visual-processing)
   * [NIFTI support](#nifti-support)
   * [Executables](#executables)
   * [Development mode](#development-mode)
      * [Clone repository](#clone-repository)
      * [Download Slicer](#download-slicer)
      * [Run using Python](#run-using-python)
         * [Independent](#independent)
         * [Slicer](#slicer)
      * [Work on GUI module](#work-on-gui-module)
      * [Create mask using SlicerDMRI](#create-mask-using-slicerdmri)
   * [Submit issues](#submit-issues)
   * [Troubleshooting](#troubleshooting)
   

Table of Contents created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)


# SlicerDiffusionQC


This is a complete slicer module for quality checking of diffusion weighted MRI. It
identifies bad gradients by comparing distance of each gradient to a median line. The median line is obtained from
[KL divergences](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence) between consecutive slices. 
After above processing, it allows user to manually review each gradient: keep or discard them.

A similar software, based on MATLAB environment, was developed earlier by a group
of Yogesh Rathi, Associate Professor, Harvard Medical School.
The MATLAB SignalDropQCTool is available at [here](https://github.com/pnlbwh/SignalDropQCTool).
On the other hand, the SlicerDiffusionQC is a faster, cleaner, and more user oriented version of that software.


![Diffusion gradient checking module](Misc/DiffusionQC-screenshot.png)



# Citation

If you use our software in your research, please cite as below:

Billah, Tashrif; Norton, Isaiah; Rathi, Yogesh; Bouix, Sylvain, Come, Carquex; Slicer Diffusion QC Tool, 
https://github.com/pnlbwh/SlicerDiffusionQC, 2018, DOI: 10.5281/zenodo.2576412

# Installation

System requirement: The program has been extensively tested on Linux Centos7. However, it should run well on any Linux machine. 
But, we do not have test/support for other platforms (MAC, Windows) yet. We are working on it.

Download [Slicer-4.10.0](https://download.slicer.org/). Slicer Diffusion QC Tool is available as an extension to Slicer. 
From Extension Manager in Slicer, search `DiffusionQC` and install.

**NOTE** DiffusionQC should work with any version >= *Slicer-4.9*.

# Usage

> path/to/Slicer --launch python-real /path/to/cli-modules/diffusionQC.py -h

    Checks the quality of gradients in a diffusion weighted mri.
    Predicts each gradient as pass or fail.
    
    Usage:
        diffusionQC.py [SWITCHES] 
    
    Meta-switches:
        -h, --help                          Prints this help message and quits
        --help-all                          Prints help messages of all sub-commands and quits
        -v, --version                       Prints the program's version and quits
    
    Switches:
        -a, --auto                          Turn on this flag for command line/automatic processing w/o Slicer
                                            visualization
        -i, --input VALUE:ExistingFile      diffusion weighted mri e.g. dwi.nrrd or path/to/dwi.nrrd, accepted formats:
                                            nhdr, nrrd, nii, and nii.gz; required
        -m, --mask VALUE:ExistingFile       mask for the diffusion weighted mri, e.g. mask.nrrd or path/to/mask.nrrd,
                                            accepted formats: nhdr, nrrd, nii, and nii.gz, if not provided then looks for
                                            default: dwi_mask.format in input directory, if default is not available,
                                            then creates the mask
        -o, --out VALUE:str                 output directory (default: input dwi directory)
    



See the following sample commands:
    
    path/to/Slicer --launch python-real /path/to/cli-modules/diffusionQC.py -i sample/dwi/image.nrrd -a
    path/to/Slicer --launch python-real /path/to/cli-modules/diffusionQC.py -i sample/dwi/image.nii.gz -a -o /tmp/
    
    # with mask, notice the arbitrary combination of nrrd and nifti formats
    path/to/Slicer --launch python-real /path/to/cli-modules/diffusionQC.py -i sample/dwi/image.nrrd -m sample/dwi/mask.nii.gz -a
    path/to/Slicer --launch python-real /path/to/cli-modules/diffusionQC.py -i sample/dwi/image.nii.gz -m sample/dwi/mask.nrrd -a -o /tmp/
    

Please see [Automatic processing](#automatic-processing) and [Visual processing](#visual-processing) below for details. 


# Tests

i) Download the [sample](https://github.com/pnlbwh/SlicerDiffusionQC/blob/master/Test/Baseline/SiemensTrio-Syngo2004A-1.nrrd) dwi image. 
Type `GradQC` in `Slicer>Modules` search icon, and select it from the drop down menu. Load the sample dwi, check `Create the mask` and hit `Process`. 
If the process completes without any error, installation is successful. You can observe the output files in sample dwi image directory.


ii) From the command line, you can test as follows:

    path/to/Slicer --launch python-real /path/to/cli-modules/diffusionQC.py -i sample/dwi/image.nrrd -a


ii) (Optional) You can clone the repository and run test as follows:

    git clone https://github.com/pnlbwh/SlicerDiffusionQC.git
    cd SlicerDiffusionQC
    path/to/Slicer --launch python-real Test/run_test.py


`SlicerDiffusionQC/Test/Baseline` contains reference results.
If installation is successful, the above command will create some files in a temporary directory.
Follow STDOUT to see success.

*You need to have `git lfs` set up on your machine (run_test.py makes use of it):

[Download](https://git-lfs.github.com/) Git command line extension

    tar -xzvf git-lfs-linux-*
    PREFIX=$HOME ./install.sh
    export PATH=$PATH:$HOME/bin/
    git lfs install



# Automatic processing

Some command line calls are shown below. Although the examples show only `nrrd` format, you can use both `nrrd` and `nii.gz` 
formats with this software. A few more examples are given in [Usage](#usage) section. Notice the presence of `-a` flag 
at the end of each command shown in this section that triggers automatic workflow i.e. process given data and save modified data 
without visualization. 

i) When you do not have a mask, you want the pipeline to create one, and you are okay with saving results in the input directory:

    path/to/Slicer --launch python-real /path/to/cli-modules/diffusionQC.py -i path/to/input.nrrd -a


ii) When you have a mask, and you are okay with saving results in the input directory:

    path/to/Slicer --launch python-real /path/to/cli-modules/diffusionQC.py -i path/to/input.nrrd -m path/to/mask.nrrd -a


iii) When you want to specify an output directory:

    path/to/Slicer --launch python-real /path/to/cli-modules/diffusionQC.py -i path/to/input.nrrd -m path/to/mask.nrrd -o output/directory -a


The above command line calls save temporary `.npy` files and final results- `inputPrefix_modified.nrrd` and `inputPrefix_QC.csv`.


# Visual processing

1. Type `GradQC` in `Slicer>Modules` search icon, and select it from the drop down menu.


2. Specify the input image, input mask, and output directory. Hit `Process`. 
Based on the power of your machine, it might take a few minutes to see the results on Slicer. The rest should be interactive. 


The GUI is made in a nice way to load your inputs instantly with mask superimposed on the original image as a labelmap. 
The `Interpolate` feature is turned off so you are able to look at the actual signal drops and artifacts.


The CLI wrapper makes following command line calls and creates temporary files as explained below:

    path/to/Slicer --launch python-real /path/to/cli-modules/diffusionQC.py -i path/to/input.nrrd -m path/to/mask.nrrd
    path/to/Slicer --launch python-real /path/to/cli-modules/diffusionQC.py -i path/to/input.nrrd -m path/to/mask.nrrd -o output/directory


Saves `inputPrefix_QC.npy, inputPrefix_confidence.npy, and inputPrefix_KLdiv.npy`. The temporary files are loaded in
[Slicer GUI](GradQC). After user interaction, when `Save`
is selected, the results are saved as `inputPrefix_modified.nrrd` and `inputPrefix_QC.csv`.


If mask is not available, keep the `Input Volume Mask` field empty and check `Create the mask`. Then, `inputPrefix_bse.nrrd` and `inputPrefix_mask.nrrd` are created.


The following are run modes from [GUI](GradQC/GradQC.py):

i) `Slicer Visual Mode` (checked) and result files exist: does not do [gradient processing](cli-modules/diffusionQC/qclib/gradient_process.py) again.
Uses existing result files to display on Slicer, waits for user interaction and `Save`.

ii) `Slicer Visual Mode` (checked) and result files do not exist: runs the whole program, uses created result files to display on Slicer, 
waits for user interaction and `Save`.

iii) `Slicer Visual Mode` (unchecked): irrespective of result files' existence, triggers automode and runs the [gradient processing](cli-modules/diffusionQC/qclib/gradient_process.py) again.
Since autoMode is triggered, Slicer GUI interaction does not open.


3. Switching among gradients:

Select each row in the table and the display will update with correspoding gradient.


4. Switching among slices:

Select a point in the graph and the axial axis display will update with corresponding slice.


5. Sure/Unsure and Pass/Fail:

Click the appropriate pushbutton to classify the current gradient on display. The text in the table will change accordingly. 
The gradients marked `Fail` will be discarded when saving as a modified image.


6. Next Review:

If you have many gradients and you would want to switch among the unsure predictions only, 
hit `Next Review` and the display will update with with next unsure classification.


7. Reset Results:

During your modification, if you would like to go back to the machine learning decision, hit this button.


8. Save:

Once you are done, `Save` the results and it will replace any previous modified image with the same prefix in your output directory.

# NIFTI support

Slicer i.e. ITK can load only NRRD diffusion weighted images. It makes use of the "measurement frame" property present in 
the NRRD header. Since NIFTI diffusion weighted images does not have any such property, it cannot be loaded into Slicer. 
For that reason, SlicerDiffusionQC was developed as an NRRD-only tool. So, the way around was NRRD-->NIFTI conversion using DWIConvert. 
Over time, DWIConvert has not been found as a reliable converter due to bugs discovered. On the other hand, 
having both NRRD and NIFTI format of the same data is wasteful of memory. To overcome the above limitation, 
yet provide and elegant way of NIFTI-->NRRD conversion, we have developed an engineering solution of writing 
NHDR header of NIFTI file pointing to NIFTI as the [`data file`](http://teem.sourceforge.net/nrrd/format.html#detached). 
[conversion/nhdr_write.py](https://github.com/pnlbwh/conversion/blob/master/conversion/nhdr_write.py) script writes an NHDR header of the given NIFTI data 
and the modified NIFTI data. When NIFTI diffusion weighted image is given to this software, it writes the 
associated NHDR header in the background, loads the NHDR header i.e. NRRD diffusion weighted image, 
does all the processing, and writes back modified data in NIFTI format along with NHDR header. 
As you probably realized, there is no extra step on the user for quality checking a NIFTI diffusion weighted image.

# Executables

Clone the repository `git clone https://github.com/pnlbwh/SlicerDiffusionQC.git` in your local directory.


[diffusionQC.py](diffusionQC/diffusionQC.py) is the cli-module that can be run from the command line. 
On the other hand, [GradQC.py](GradQC/GradQC.py) is the GUI module that is loaded into Slicer.

The [SlicerExecutionModel](diffusionQC/diffusionQC.xml) wrapper describes the input/output of this script for use by Slicer. 
The Slicer scripted GUI module code is within the SlicerDiffusionQC subdirectory.


# Development mode

We welcome any contribution to this software. To facilitate contribution, we are providing the following instruction.

## Clone repository

> git clone https://github.com/pnlbwh/SlicerDiffusionQC.git    

The modules of interest are `diffusionQC/diffusionQC.py` and `SlicerDiffusionQC/GradQC.py`.

## Download Slicer

Download a fresh [Slicer-4.10.0](https://download.slicer.org/). It may be useful to remove your `~/.config/NA-MIC` directory 
(`mv ~/.config/NA-MIC ~/.config/NA-MIC.bak`) so any old settings cannot get into the fresh Slicer environment. 

## Run using Python

`diffusionQC/diffusionQC.py` module requires a Python 2.7 interpreter. You can use an independent Python 2.7 or 
the one that came with Slicer download. For development work with Python 2.7, please make sure to provide a mask.

### Independent

Install [Python 2.7](https://docs.conda.io/en/latest/miniconda.html) with the following packages:

> pip install plumbum pynrrd nibabel

Then

```bash
# Linux/MAC
export PYTHONPATH=path/to/SlicerDiffusionQC/diffusionqclib/
# Windows PowerShell
$Env:PYTHONPATH+="path\to\SlicerDiffusionQC\diffusionqclib"

~/miniconda2/bin/python \
path/to/SlicerDiffusionQC/diffusionQC/diffusionQC.py -o /tmp -i dwi_nifti_or_nrrd -m mask_nifti_or_nrrd -a
```

### Slicer

```bash
cd Slicer-4.*-linux-amd64/bin
./python-real
```

```python
from pip._internal import main as pipmain
pipmain(['install','plumbum','pynrrd','nibabel'])
exit()
```

Then

```bash
PYTHONPATH=path/to/SlicerDiffusionQC/diffusionqclib/ /path/to/Slicer-4.*-linux-amd64/Slicer/bin/python-real \
path/to/SlicerDiffusionQC/diffusionQC/diffusionQC.py -o /tmp -i dwi_nifti_or_nrrd -m mask_nifti_or_nrrd -a
```

## Work on GUI module

In the above, we have described about development in the CLI module `diffusionQC/diffusionQC.py`. Here we describe how you can 
contribute to the GUI module. Firstly, we need to append `path/to/SlicerDiffusionQC/diffusionqclib/` to `PYTHONPATH`:

    # Linux/MAC
    export PYTHONPATH=path/to/SlicerDiffusionQC/diffusionqclib/
    # Windows PowerShell
    $Env:PYTHONPATH+="path\to\SlicerDiffusionQC\diffusionqclib"
    
Then, launch `/path/to/Slicer-4.*/Slicer` from the same terminal. If you have not installed the required packages on `python-real` yet, 
you can do it now from `Python Interactor` on Slicer GUI. 
Now, add the following path to `Slicer>Edit>Application Settings>Modules>Additional module paths`:

    /path/to/SlicerDiffusionQC/diffusionQC
    /path/to/SlicerDiffusionQC/SlicerDiffusionQC/

If no error shows up the Python console, all dependencies are solved and your loading is successful. 
Now search `GradQC` in `Slicer>Modules` search icon, and select it from the drop down menu. Finally, you should be 
able to follow [Visual processing](#visual-processing). However, please make sure to provide a mask.


## Create mask using SlicerDMRI

So far we have described development infrastructure with provided mask. If you would like Slicer to generate a mask on its own, 
you need to install SlicerDMRI extension from the Extension Manager. Then, you can develop without providing a mask:

* CLI module

> path/to/Slicer --launch python-real path/to/SlicerDiffusionQC/diffusionQC/diffusionQC.py -o /tmp -i dwi_nifti_or_nrrd -a

If you would like the software to create a mask, you must use Slicer `python-real`. 
Independent Python 2.7 can not be used in this task.

* GUI module

You can check `Create a mask` box upon loading `GradQC`.
    

# Troubleshooting

1. On Windows Git Bash,
    
    
    cd /path/to/SlicerDiffusionQC
    export PYTHONPATH=`pwd`/diffusionqclib
    ~/Downloads/Slicer\ 4.10.2/Slicer.exe --launch python-real Test/run_test.py
    
does not seem to work but the following does:
    
    cd /path/to/SlicerDiffusionQC
    PYTHONPATH=`pwd`/diffusionqclib ~/Downloads/Slicer\ 4.10.2/Slicer.exe --launch python-real Test/run_test.py


# Submit issues

Feel free to submit an issue on this github repository. We shall get back to you as early as we can.

