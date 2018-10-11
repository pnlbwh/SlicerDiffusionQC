#!/usr/bin/env python-real

from plumbum import cli
import os, sys

from diffusionqclib.gradient_process import process


class QC(cli.Application):

    """Checks the quality of gradients in a diffusion weighted mri.
    Predicts each gradient as pass or fail."""

    dwi = cli.SwitchAttr(
        ['-i', '--input'],
        cli.ExistingFile,
        help='diffusion weighted mri e.g. dwi.nrrd or path/to/dwi.nrrd, accepted formats: nhdr, nrrd, nii, and nii.gz',
        mandatory=True)

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

#    run_test = cli.SwitchAttr(
#        ['--test']
#        help='''Run self-tests against given directory (unimplemented)''',
#        mandatory=False)


    def main(self):
        #if self.run_test:
        #    import warnings
        #    warnings.warn("--test is unimplemented for the CLI mode")
        #    sys.exit(0)

        self.dwi= str(self.dwi)
        self.mask= str(self.mask)
        self.out= str(self.out)

        process(self.dwi, self.mask, self.out, self.autoMode)


if __name__ == '__main__':
    QC.run()
