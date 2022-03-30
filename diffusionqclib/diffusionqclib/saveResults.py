import numpy as np
import nrrd
import os
import time
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)
    import nibabel as nib

from .bval_bvec_io import read_bvals, read_bvecs, write_bvals, write_bvecs
from .nhdr_write import nhdr_write

def saveDecisions(outPrefix, deletion, confidence, bvals):

    fqc = open(outPrefix+'_QC.csv', "w")
    fcon = open(outPrefix+'_confidence.csv', "w")
    fqc.write('Gradient #, Pass 1/Fail 0, b value\n')
    fcon.write('Gradient #, Sure 1/Unsure 0, b value\n')
    for i in range(len(deletion)):
        fqc.write(str(i) + ',' + str(deletion[i]) + ','+ str(bvals[i])+'\n')
        fcon.write(str(i) + ',' + str(confidence[i]) + ','+ str(bvals[i])+'\n')

    fqc.close()
    fcon.close()


def saveTemporary(outPrefix, deletion, KLdiv, confidence, bvals):
    np.save(outPrefix + '_QC.npy', deletion)
    np.save(outPrefix + '_KLdiv.npy', KLdiv)
    np.save(outPrefix + '_confidence.npy', confidence)
    np.save(outPrefix + '_bvals.npy', bvals)


def saveDWI(dwiPath, outPrefix, deletion, hdr_in, mri_in, grad_axis):
    
    print("Saving modified diffusion weighted MRI ...\n\n")
    print("Hang tight, writing file might take a couple of minutes ....\n\n")
    start_time= time.time()
    
    good_indices = np.where(deletion == 1)[0] # good ones are marked with 1
    bad_indices = np.where(deletion == 0)[0] # bad ones are marked with 0
    # Obtain the output dwi
    mri_out = np.delete(mri_in, (np.where(deletion == 0)[0]), axis=grad_axis) # bad ones are marked with 0
    
    if dwiPath.endswith('nrrd') or dwiPath.endswith('nhdr'):
    
        hdr_out = hdr_in.copy()

        shape_out = list(np.shape(mri_in))
        shape_out[grad_axis] = len(good_indices)
        hdr_out['sizes'] = shape_out

        # Write the good gradients at modified index and update the volume accordingly
        # This approach ensures maximal preservation of original header
        for new_ind, ind in enumerate(good_indices):

            # Python 3.6 (Anaconda)
            # hdr_out['DWMRI_gradient_' + f'{new_ind:04}'] = hdr_in[
            #     'DWMRI_gradient_' + f'{ind:04}']

            # Python 2.7 (Slicer)
            hdr_out['DWMRI_gradient_' + '{:04}'.format(new_ind)] = hdr_in[
                'DWMRI_gradient_' + '{:04}'.format(ind)]

        # Now delete the rest of the gradients
        for ind in range(mri_out.shape[grad_axis], mri_in.shape[grad_axis]):
            # Python 3.6 (Anaconda)
            # del hdr_out['DWMRI_gradient_' + f'{ind:04}']

            # Python 2.7 (Slicer)
            del hdr_out['DWMRI_gradient_' + '{:04}'.format(ind)]

        nrrd.write(outPrefix+'_modified.nrrd', mri_out, header=hdr_out, compression_level = 1)
        
    else:
    
        img= nib.load(dwiPath)
        
        inPrefix= dwiPath.split('.nii')[0]
        
        bvals= read_bvals(inPrefix+'.bval')
        # Delete corresponding bvals
        bvals_new= np.delete(bvals, bad_indices)
        
        bvecs= read_bvecs(inPrefix+'.bvec')
        # Delete corresponding bvecs
        bvecs_new= np.delete(bvecs, bad_indices, axis= 0)

        img_out= nib.Nifti1Image(mri_out, affine= img.affine, header= img.header)
        
        outPrefix+='_modified'
        modified_imgPath= outPrefix+'.nii.gz'
        modified_nhdrPath= outPrefix+'.nhdr'
        modified_bvalFile= outPrefix+'.bval'
        modified_bvecFile= outPrefix+'.bvec'
        
        img_out.to_filename(modified_imgPath)
        write_bvals(modified_bvalFile, bvals_new)
        write_bvecs(modified_bvecFile, bvecs_new)
        
        nhdr_write(modified_imgPath, modified_bvalFile, modified_bvecFile, modified_nhdrPath)
        
    
    print("Elapsed time in saving results %s seconds\n\n" %(time.time() - start_time))

    
def saveResults(dwiPath, outPrefix, deletion, KLdiv, confidence, bvals, hdr, mri, grad_axis, autoMode):
    
    saveTemporary(outPrefix, deletion, KLdiv, confidence, bvals)
    
    # In autoMode, writes out the modified dwi image
    if autoMode:
        saveDecisions(outPrefix, deletion, confidence, bvals)
        saveDWI(dwiPath, outPrefix, deletion, hdr, mri, grad_axis)

