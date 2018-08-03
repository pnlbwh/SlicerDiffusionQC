#!/usr/bin/env python-real

from plumbum import cli
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # diffusionQC is added to python search directory
from qclib.dwi_attributes import dwi_attributes
from qclib.saveResults import saveResults
from qclib.gradient_process import calc


class QC(cli.Application):

    """Checks the quality of gradients in a diffusion weighted mri.
    Predicts each gradient as pass or fail."""

    dwi = cli.SwitchAttr(
        ['-i', '--input'],
        cli.ExistingFile,
        help='diffusion weighted mri e.g. dwi.nrrd or path/to/dwi.nrrd, accepted formats: nhdr, nrrd, nii, and nii.gz',
        mandatory=False)

    mask = cli.SwitchAttr(
        ['-m', '--mask'],
        cli.ExistingFile,
        help='''mask for the diffusion weighted mri, e.g. mask.nrrd or path/to/mask.nrrd,
            accepted formats: nhdr, nrrd, nii, and nii.gz, 
            if not provided then looks for default: dwi_mask.format in input directory,
            if default is not available, then creates the mask''',
        mandatory=False)

    out = cli.SwitchAttr(
        ['-o', '--out'],
        help='''output directory (default: input dwi directory)''',
        mandatory=False)


    autoMode= cli.Flag(
        ['-a', '--auto'],
        help= 'Turn on this flag for command line/automatic processing w/o Slicer visualization',
        mandatory= False,
        default= False)

    def main(self):

        self.dwi= str(self.dwi)
        self.mask= str(self.mask)
        self.out= str(self.out)

        hdr, mri, grad_axis, axialViewAxis, b_value, gradients = dwi_attributes(self.dwi)
        # TODO: Check if mask exists, take necessary steps
        KLdiv, good_bad, confidence= calc().process(hdr, mri, grad_axis, b_value, gradients, self.mask, axialViewAxis)


        # Save QC results
        if self.out== 'None':
            directory = os.path.dirname(os.path.abspath(self.dwi))
        else:
            directory= self.out

        # Extract prefix from dwi
        prefix = os.path.basename(self.dwi.split('.')[0])

        # Pass prefix and directory to saveResults()
        saveResults(prefix, directory, good_bad, KLdiv, confidence, hdr, mri, grad_axis, self.autoMode)


if __name__ == '__main__':
    QC.run()
