# Return headers, mri data, axis index along which gradients are listed, axialViewAxis, b-value, gradient directions
import nrrd
import numpy as np
from nhdr_write import nhdr_write
import os

def dwi_attributes(file_name, inPrefix):
    
    # If executed from Slicer GUI, the following conversion is already done in SlicerDiffusionQC/GradQC.py
    if '.nii' in file_name:
        nhdr= inPrefix+'.nhdr'
        if not os.path.exists(nhdr): 
            nhdr_write(file_name, inPrefix+'.bval', inPrefix+'.bvec', nhdr)
        file_name= nhdr
    
    
    dwi= nrrd.read(file_name)

    hdr= dwi[1] # header file
    mri= dwi[0] # voxel data

    axis_elements= hdr['kinds']
    for i in range(4):
        if axis_elements[i] == 'list' or axis_elements[i] == 'vector':
            grad_axis= i
            break

    view= hdr['space'].split('-')
    for i in range(3):
        if view[i] == 'superior' or view[i]=='inferior':
            axialViewAxis= i

    b_value = float(hdr['DWMRI_b-value'])
    gradients = np.zeros((mri.shape[grad_axis],3), dtype= 'float')

    for i in range(mri.shape[grad_axis]):
        # Python 3.6
        # gradients[i,: ]= [float(x) for x in hdr['DWMRI_gradient_'+f'{i:04}'].split( )]

        #Python 2.7
        gradients[i, :] = [float(x) for x in hdr['DWMRI_gradient_' + '{:04}'.format(i)].split()]


    return hdr, mri, grad_axis, axialViewAxis, b_value, gradients

