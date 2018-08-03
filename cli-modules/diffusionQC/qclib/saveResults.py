import numpy as np
# import pandas as pd
import nrrd
import os


def saveDecisions(prefix, directory, deletion):

    # fix pandas for Slicer Python 2.7
    # df= pd.DataFrame({'Gradient #':[i for i in range(len(deletion))],'Pass 1, Fail 0':deletion})
    # df.to_csv(os.path.join(directory, prefix+'_QC.csv'), index= False)

    # instead we can write as a .txt file
    f = open(os.path.join(directory, prefix+'_QC.txt'), "w")
    f.write('Gradient labels: Pass 1, Fail 0\n\n')
    for i in range(len(deletion)):
        f.write('Gradient # '+ str(i) + ': ' + str(deletion[i]) + '\n')

    f.close()

    # TODO: Sylvain told to save as a .csv file



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
        # hdr_out['keyvaluepairs']['DWMRI_gradient_' + f'{new_ind:04}'] = hdr_in['keyvaluepairs'][
        #     'DWMRI_gradient_' + f'{ind:04}']

        # Python 2.7 (Slicer)
        hdr_out['keyvaluepairs']['DWMRI_gradient_' + '{:04}'.format(new_ind)] = hdr_in['keyvaluepairs'][
            'DWMRI_gradient_' + '{:04}'.format(ind)]



    # Now delete the rest of the gradients
    for ind in range(mri_out.shape[grad_axis], mri_in.shape[grad_axis]):
        # Python 3.6 (Anaconda)
        # del hdr_out['keyvaluepairs']['DWMRI_gradient_' + f'{ind:04}']

        # Python 2.7 (Slicer)
        del hdr_out['keyvaluepairs']['DWMRI_gradient_' + '{:04}'.format(ind)]

    nrrd.write(os.path.join(directory, prefix+'_modified.nrrd'), mri_out, options=hdr_out)


def saveResults(prefix, directory, deletion, KLdiv, confidence, hdr, mri, grad_axis, autoMode):

    if autoMode:
        saveDecisions(prefix, directory, deletion)
        saveDWI(prefix, directory, deletion, hdr, mri, grad_axis)
    else:
        saveTemporary(prefix, directory, deletion, KLdiv, confidence)

