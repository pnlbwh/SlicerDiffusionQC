import numpy as np
import nrrd
import os
import time


def saveDecisions(prefix, directory, deletion):

    f = open(os.path.join(directory, prefix+'_QC.csv'), "w")
    f.write('Gradient #, Pass 1\Fail 0\n')
    for i in range(len(deletion)):
        f.write(str(i) + ',' + str(deletion[i]) + '\n')

    f.close()


def saveTemporary(prefix, directory, deletion, KLdiv, confidence):
    np.save(os.path.join(directory, prefix + '_QC.npy'), deletion)
    np.save(os.path.join(directory, prefix + '_KLdiv.npy'), KLdiv)
    np.save(os.path.join(directory, prefix + '_confidence.npy'), confidence)


def saveDWI(prefix, directory, deletion, hdr_in, mri_in, grad_axis):

    hdr_out = hdr_in.copy()

    good_indices = np.where(deletion == 1)[0] # good ones are marked with 1

    shape_out = list(np.shape(mri_in))
    shape_out[grad_axis] = len(good_indices)
    hdr_out['sizes'] = shape_out


    # Write the output dwi
    mri_out = np.delete(mri_in, (np.where(deletion == 0)[0]), axis=grad_axis) # bad ones are marked with 0

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

    print("Saving modified diffusion weighted MRI ...\n\n")
    print("Hang tight, writing file might take a couple of minutes ....\n\n")
    start_time= time.time()
    nrrd.write(os.path.join(directory, prefix+'_modified.nrrd'), mri_out, header=hdr_out, compression_level = 1)
    print("Elapsed time in saving results %s seconds\n\n" %(time.time() - start_time))

def saveResults(prefix, directory, deletion, KLdiv, confidence, hdr, mri, grad_axis, autoMode):

    # In autoMode, writes out the modified dwi image
    if autoMode:
        saveDecisions(prefix, directory, deletion)
        saveDWI(prefix, directory, deletion, hdr, mri, grad_axis)

    # In visualMode, writes out only the temporary results
    else:
        saveTemporary(prefix, directory, deletion, KLdiv, confidence)