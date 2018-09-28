#!/usr/bin/env python-real

import numpy as np
# import pandas as pd
import os, sys
import nrrd

eps = 2.2204e-16

SCRIPTDIR= os.path.abspath(os.path.dirname(__file__))
REFDIR= os.path.join(SCRIPTDIR, 'test_data', 'ref')
TESTDIR= os.path.join(SCRIPTDIR, 'test_data', 'test')


# diffusionQC is added to python search directory
sys.path.append(os.path.join(SCRIPTDIR, 'cli-modules/diffusionQC'))
from qclib.gradient_process import process


def load_results(directory, prefix):

    # csv= pd.read_csv(os.path.join(directory, prefix+'_QC.csv'))
    csv = np.load(os.path.join(directory, prefix + '_QC.npy'))
    qc= np.load(os.path.join(directory, prefix + '_QC.npy'))
    kl= np.load(os.path.join(directory, prefix + '_KLdiv.npy'))
    con= np.load(os.path.join(directory, prefix + '_confidence.npy'))
    dwi= nrrd.read(os.path.join(directory, prefix+'_modified.nrrd'))[0]

    return (csv, qc, kl, con, dwi)


def main():

    cases= ['5006-dwi-xc_test', '1001-dwi-xc_test']

    for case in cases:

        # run test case
        # process(self.dwi, self.mask, self.out, self.autoMode)
        process(os.path.join(TESTDIR, case+'.nrrd'), 'None', 'None', True)


        # load reference results
        csv, qc, kl, con, dwi = load_results(REFDIR, case)
        # load obtained results
        csv_test, qc_test, kl_test, con_test, dwi_test = load_results(TESTDIR, case)

        failed= 0
        # for attr in 'csv qc kl con dwi'.split(' '):
        for attr in 'csv qc kl con dwi'.split(' '):
            print(attr, ' test')
            if (eval(attr) - eval(attr+'_test')).sum()>eps:
                failed+=1
                print('{} : {} test failed'.format(case, attr))


    if not failed:
        print('All tests passed')


if __name__== '__main__':
    main()