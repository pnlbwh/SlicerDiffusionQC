#!/usr/bin/env python-real

import numpy as np
import os, tempfile
import nrrd
import subprocess
from plumbum import local

eps = 2.2204e-16

SCRIPTDIR= os.path.abspath(os.path.dirname(__file__))
REFDIR= os.path.join(SCRIPTDIR, 'Baseline')

from diffusionqclib.gradient_process import process


def load_results(directory, prefix):

    csv = np.loadtxt(os.path.join(directory, prefix + '_QC.csv'), delimiter= ',',
                     skiprows=1, usecols=1)

    qc  = np.load(os.path.join(directory, prefix + '_QC.npy'))
    kl  = np.load(os.path.join(directory, prefix + '_KLdiv.npy'))
    con = np.load(os.path.join(directory, prefix + '_confidence.npy'))

    # read the modified gradients
    hdr = nrrd.read(os.path.join(directory, prefix+'_modified.nrrd'))[1]
    grads= np.array([[float(x)
                      for x in hdr['DWMRI_gradient_' + '{:04}'.format(ind)].split(' ') if x]
                        for ind in range(len(np.where(csv==1)))])

    return (csv, qc, kl, con, grads)


def main():

    subprocess.check_call(['git', 'lfs', 'pull', '--exclude='], cwd=REFDIR, )

    cases= ['SiemensTrio-Syngo2004A-1']

    for case in cases:
        tmpdir = tempfile.mkdtemp()
        print(tmpdir)

        # run test case
        process(local.path(REFDIR).join(case+'.nrrd'), outDir=tmpdir)


        # load reference results
        csv, qc, kl, con, dwi = load_results(REFDIR, case)
        # load obtained results
        csv_test, qc_test, kl_test, con_test, dwi_test = load_results(tmpdir, case)

        failed= 0
        for attr in 'csv qc kl con dwi'.split(' '):

            if (eval(attr) - eval(attr+'_test')).sum()>eps:
                failed+=1
                print('{} : {} test failed'.format(case, attr))
            else:
                print(attr, ' test passed')


    if not failed:
        print('All tests passed')


if __name__== '__main__':
    main()
