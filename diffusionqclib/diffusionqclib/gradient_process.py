import numpy as np
import os, sys

import time
import multiprocessing

import nrrd
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)
    import nibabel as nib

from dwi_attributes import dwi_attributes
from saveResults import saveResults

POINTS = 50 # For KDE estimation
eps = 2.2204e-16  # For preventing log( ) to be -inf
percentage = 0.20  # For discretizing scaled b values
group = [50, 800]  # For separating lower b values
T = 400  # Number of non zero values in the mask for the corresponding slice to take into account

def load_mask(mask, dwi, prefix, directory):

    if mask is None:

        # Mask creation
        print('\n\nMask not specified, creating mask ...\n\n')

        import distutils.spawn
        from subprocess import check_output

        mask= os.path.join(directory, prefix+'_mask'+'.nrrd')
        bse= os.path.join(directory, prefix+'_bse'+'.nrrd')

        masking_cli = distutils.spawn.find_executable("DiffusionWeightedVolumeMasking")

        args = [masking_cli, dwi, bse, mask]

        try:
            print('Slicer --launch', masking_cli, dwi, bse, mask)
            check_output(args)
        except:
            print("Mask creation failed")
            exit(1)


    if mask.endswith('.nii') or mask.endswith('.nii.gz'):
        img = nib.load(mask)  # MRI loaded as a 256 x 256 x 176 volume
        return img.get_data()

    elif mask.endswith('.nrrd') or mask.endswith('.nhdr'):
        img = nrrd.read(mask)
        return img[0]

    else:
        print("Invalid file format")
        exit(1)


def extract_feature(volume, *args):

    sig = np.median(abs(volume - np.median(volume))) / 0.6745

    if not args:
        N = len(volume)
        # Estimate bandwidth
        if sig > 0:
            h = sig * (4.0 / (3 * N)) ** 0.2
        else:
            h = 1

        # Calculate data points where we want to find ksdensity estimate
        e1 = volume.min() - h * 3
        e2 = volume.max() + h * 3

        x = np.linspace(e1, e2, POINTS)
        x = np.array(x).reshape(1, POINTS)

    else:
        x = args[0]
        h = args[1]

    volume = np.array(volume).reshape(len(volume), 1)
    volumeMatrix = np.repeat(volume, POINTS, axis=1)
    temp = (x - volumeMatrix) / h
    Z = np.sum(np.exp(-0.5 * temp ** 2), axis=0)
    Z = Z / sum(Z)

    return (Z, x, h)


def KL(P, Q):
    # Assuming normalization inside extract feature
    P = P + eps
    Q = Q + eps

    return np.sum([P[i] * np.log(P[i] / Q[i]) for i in range(len(P))])


def find_b_shell(scaled_b_values):
    scaled_b_values[(scaled_b_values >= group[0]) & (scaled_b_values <= group[1])] = 0

    scaled_b_values = sorted(scaled_b_values)

    b_shell = []
    b_shell.append(scaled_b_values[0])
    for i in range(1, len(scaled_b_values)):
        if scaled_b_values[i] > (1 + percentage) * scaled_b_values[i - 1]:
            b_shell.append(scaled_b_values[i])

    b_shell.append(-1)

    return b_shell




def grad_process(grad_id):

    print("Processing gradient {}/{} ...".format(grad_id+1,totalGradients)) # counter may be different from grad_id+1
    if visualMode:
        # Each gradient contributes (70/totalGradients) % work
        print("<filter-progress>{}</filter-progress>".format(0.1+0.7*(grad_id+1)/totalGradients))
        sys.stdout.flush()


    # load the specific volume
    if grad_axis == 0:
        I = mri[grad_id, :, :, :]

    elif grad_axis == 1:
        I = mri[:, grad_id, :, :]

    elif grad_axis == 2:
        I = mri[:, :, grad_id, :]

    elif grad_axis == 3:
        I = mri[:, :, :, grad_id]


    sim = np.zeros(M.shape[slice_axis] - 1, dtype='float')
    for n in range(M.shape[slice_axis] - 1):

        # load two consecutive slices and their masks
        if slice_axis == 0:
            s1 = I[n, :, :]
            s2 = I[n + 1, :, :]
            m1 = M[n, :, :]
            m2 = M[n + 1, :, :]

        elif slice_axis == 1:
            s1 = I[:, n, :]
            s2 = I[:, n + 1, :]
            m1 = M[:, n, :]
            m2 = M[:, n + 1, :]

        elif slice_axis == 2:
            s1 = I[:, :, n]
            s2 = I[:, :, n + 1]
            m1 = M[:, :, n]
            m2 = M[:, :, n + 1]


        if np.count_nonzero(m1) < T or np.count_nonzero(m2) < T:
            sim[n] = 0
            continue

        r1 = s1[m1 == 1]
        r2 = s2[m2 == 1]


        if r1.max() > r2.max():
            f1, x, bw = extract_feature(r1)  # Find the bins, bw for the 1st slice
            f2, _, _ = extract_feature(r2, x, bw)  # Use the same bins, bw to calculate KDE for the 2nd slice
        else:
            f1, x, bw = extract_feature(r2)  # Find the bins, bw for the 1st slice
            f2, _, _ = extract_feature(r1, x, bw)  # Use the same bins, bw to calculate KDE for the 2nd slice

        sim[n] = 0.5 * (KL(f1, f2) + KL(f2, f1))


    return sim



def process(dwiPath, maskPath=None, outDir=None, autoMode=True):

    # Global definitions, attributes shared among functions and processes
    global mri, M, grad_axis, slice_axis, totalGradients, visualMode
    visualMode= not autoMode

    hdr, mri, grad_axis, slice_axis, b_value, gradients = dwi_attributes(dwiPath)
    totalGradients = gradients.shape[0]

    print("\n\nInput image loaded ...\n\n")
    if visualMode:
        # 5% work done
        print("<filter-progress>0.05</filter-progress>")
        sys.stdout.flush()


    # Determine prefix and directory
    if outDir is None:
        directory = os.path.dirname(os.path.abspath(dwiPath))
    else:
        directory = outDir

    prefix = os.path.basename(os.path.splitext(dwiPath)[0])

    # Load/create mask
    M = load_mask(maskPath, dwiPath, prefix, directory)
    print("\n\nMask loaded ...\n\n")
    if visualMode:
        # 10% work done
        print("<filter-progress>0.10</filter-progress>")
        sys.stdout.flush()

    start_time = time.time()

    print("\n\nCalculating KL divergences ...\n\n")
    pool = multiprocessing.Pool()  # Use all available cores, otherwise specify the number you want as an argument

    res = pool.map_async(grad_process, range(mri.shape[grad_axis]))

    # The output is a (# gradients x # valid slices-1) array
    S = res.get()  # when pool.map_async
    # S= res # when pool.map

    pool.close()
    pool.join()

    S = np.array(S)

    # Calculating scaled b values
    scaled_b_values = np.zeros(mri.shape[grad_axis], dtype=float)
    for i in range(mri.shape[grad_axis]):
        scaled_b_values[i] = b_value * np.linalg.norm(gradients[i, :]) ** 2

    # Finding b-shell
    b_shell = find_b_shell(scaled_b_values.copy())

    # Finding median among the gradients in the same b-shell
    da = np.zeros(np.shape(S), dtype='float')
    dr = np.zeros(np.shape(S), dtype='float')

    # For each value in the b-shell, the median should be a (1 x # valid slices-1) array
    for b in b_shell:

        if b == -1:
            same_shell_mask = (scaled_b_values > group[0]) & (scaled_b_values < group[1])
        else:
            same_shell_mask = (scaled_b_values >= b * (1 - percentage)) & (scaled_b_values <= b * (1 + percentage))

        if np.count_nonzero(same_shell_mask) < 2:
            ref = [0.01] * S.shape[1]
        else:
            # Find ref(b,n) for all the gradients in the same b shell
            ref = np.median(S[same_shell_mask, :], axis=0)

        for n in range(S.shape[1]):

            if not ref[n]:
                ref[n] = eps  # To prevent divide by zero

            da[same_shell_mask, n] = S[same_shell_mask, n] - ref[n]
            dr[same_shell_mask, n] = da[same_shell_mask, n] / ref[n]


    print("\n\nElapsed time in calculation %s seconds\n\n" %(time.time() - start_time))

    # Discard some slices at the beginning and at the end for not having significant voxels
    # We are keeping 'end' one less because we don't want to go beyond the last slice that satisfies the area condition
    start = 2
    end = M.shape[slice_axis] - 3

    da[:, 0:start] = -1
    da[:, end:M.shape[slice_axis]] = -1
    dr[:, 0:start] = -1
    dr[:, end:M.shape[slice_axis]] = -1

    QC = np.zeros((S.shape[0], 2), dtype='float')
    good_bad = np.ones(gradients.shape[0], dtype=int)
    confidence= np.ones(gradients.shape[0], dtype=int)
    for k in range(S.shape[0]):
        QC[k, :] = [max(da[k, :]), max(dr[k, :])]

        # Good/bad gradients
        if QC[k, 0] >= 0.15 or QC[k, 1] >= 10:
            good_bad[k] = 0

        # Sure/unsure classification
        if (QC[k, 0] >= 0.05 and QC[k, 0]<= 0.3) and (QC[k, 1] >= 5 and QC[k, 0]<= 20):
            confidence[k]= 0

    print("\n\nPrediction completed ...\n\n")
    if visualMode:
        # 90% work done
        print("<filter-progress>0.90</filter-progress>")
        sys.stdout.flush()

    # Save QC results
    # Pass prefix and directory to saveResults()
    saveResults(prefix, directory, good_bad, S, confidence, hdr, mri, grad_axis, autoMode)
