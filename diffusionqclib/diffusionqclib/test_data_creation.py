#!/usr/bin/env python

import nrrd
import numpy as np
import sys

from dwi_attributes import dwi_attributes


def main():

    img_file= sys.argv[1]

    hdr_in, mri_in, grad_axis, axialViewAxis, b_value, gradients= dwi_attributes(img_file)

    # select odd indexed slices
    indices= [i for i in range(0, mri_in.shape[axialViewAxis],2)]


    hdr_out = hdr_in.copy()
    shape_out = list(np.shape(mri_in))
    shape_out[axialViewAxis] = len(indices)
    hdr_out['sizes'] = shape_out

    mri_out= np.delete(mri_in, indices, axis= axialViewAxis)

    nrrd.write(img_file.split('.')[0]+'_test.nrrd', mri_out, header= hdr_out, compression_level= 1)


if __name__== '__main__':
    main()
    'test_data_creation.py dwi.nrrd'