import os
import glob
import numpy as np
import nibabel as nb
import os
import scipy.io as sio
from scipy.stats import pearsonr

PH_SERVER_ROOT = os.environ.get('PH_SERVER_ROOT')

def zscore(data, axis):
    data -= data.mean(axis=axis, keepdims=True)
    data /= data.std(axis=axis, keepdims=True)
    return np.nan_to_num(data, copy=False)

def correlation(matrix1, matrix2):
    d1 = matrix1.shape[-1]
    d2 = matrix2.shape[-1]

    assert d1 == d2
    assert matrix1.ndim <= 2
    assert matrix2.ndim <= 2
    
    matrix1 = zscore(matrix1.astype(float), matrix1.ndim - 1) / np.sqrt(d1)
    matrix2 = zscore(matrix2.astype(float), matrix2.ndim - 1) / np.sqrt(d2)
    
    if matrix1.ndim >= matrix2.ndim:
        return np.dot(matrix1, matrix2.T)
    else:
        return np.dot(matrix2, matrix1.T)

def get_motion_params(file, pipeline = 'cpac'):

    data = np.genfromtxt(file).T
    
    if pipeline == 'abcd':
        data = np.vstack((data[3:,:],data[:3,:]))

        data = np.vstack((data[2,:]*180/np.pi,
            data[0,:]*180/np.pi,
            -data[1,:]*180/np.pi,
            data[5,:],
            data[3,:],
            -data[4,:]))
    else:
        data = np.vstack((data[2,:]*180/np.pi,
            data[0,:]*180/np.pi,
            -data[1,:]*180/np.pi,
            data[5,:],
            data[3,:],
            -data[4,:]))

    return data

path1 = f'{os.environ.get("PH_SERVER_WORKING_ROOT")}/CPAC_XCP/ABCD/preprocessed/data'
path2 = f'{os.environ.get("DATA_INPUT_DIR")}/cpac_abcd'

sub_list = list(range(25427,25457))
sub_list.remove(25430)
sub_list.remove(25448)

var_list = ['anat mask', 'CSF', 'GM', 'WM', 'func mask', 'motion', 
    'anat-mni abcd', 'anat-mni cpac', 'func-mni abcd', 'func-mni cpac', 
    'func-t1 abcd', 'func-t1 cpac', 'anat-mni', 'func-mni', 'func-t1']

if 'motion' in var_list:
    motion_index = var_list.index('motion')
corrs = np.zeros((len(sub_list), len(var_list)+5))

for num_sub, sub in enumerate(sub_list):

    sub = '00'+str(sub)

    path_list1 = [path1+'/sub-'+sub+'/ses-1/files/T1w/brainmask_fs.nii.gz',
                path1+'/sub-'+sub+'/ses-1/files/T1w/T1w_fast_pve_0.nii.gz',
                path1+'/sub-'+sub+'/ses-1/files/T1w/T1w_fast_pve_1.nii.gz',
                path1+'/sub-'+sub+'/ses-1/files/T1w/T1w_fast_pve_2.nii.gz',
                path1+'/sub-'+sub+'/ses-1/files/task-rest01/brainmask_fs.2.0.nii.gz',
                path1+'/sub-'+sub+'/ses-1/files/task-rest01/MotionCorrection/task-rest01_mc.par',
                # path1+'/sub-'+sub+'/ses-1/files/MNINonLinear/Results/task-rest01/DCANBOLDProc_v4.0.0/FD.mat',
                path1+'/sub-'+sub+'/ses-1/files/MNINonLinear/T1w_restore_brain.nii.gz', # ABCD anat to standard
                path2+'/output/cpac_cpac_abcd-options/sub-'+sub+'a_ses-1/anat/sub-'+sub+'a_ses-1_space-template_desc-brain_T1w.nii.gz', # C-PAC anat to standard
                path1+'/sub-'+sub+'/ses-1/files/MNINonLinear/Results/task-rest01/task-rest01_mean.nii.gz', # ABCD func to standard
                path2+'/output/cpac_cpac_abcd-options/sub-'+sub+'a_ses-1/func/sub-'+sub+'a_ses-1_task-rest_run-1_space-template_desc-mean_bold.nii.gz', # C-PAC func to standard
                path1+'/sub-'+sub+'/ses-1/files/task-rest01/Scout2T1w_masked.nii.gz', # ABCD func in T1 space
                glob.glob(path2+'/working/cpac_sub-'+sub+'a_ses-1/func_to_anat_FLIRT_*/_*/linear_func_to_anat/*flirt.nii.gz')[0], # C-PAC func in T1 space
                path1+'/sub-'+sub+'/ses-1/files/MNINonLinear/T1w_restore_brain.nii.gz', # ABCD anat to standard
                path1+'/sub-'+sub+'/ses-1/files/MNINonLinear/Results/task-rest01/task-rest01_mean.nii.gz', # ABCD func to standard
                path1+'/sub-'+sub+'/ses-1/files/task-rest01/Scout2T1w_masked.nii.gz'] # ABCD func in T1 space

    path_list2 = [path2+'/output/cpac_cpac_abcd-options/sub-'+sub+'a_ses-1/anat/sub-'+sub+'a_ses-1_space-T1w_desc-brain_mask.nii.gz',
                path2+'/output/cpac_cpac_abcd-options/sub-'+sub+'a_ses-1/anat/sub-'+sub+'a_ses-1_label-CSF_mask.nii.gz',
                path2+'/output/cpac_cpac_abcd-options/sub-'+sub+'a_ses-1/anat/sub-'+sub+'a_ses-1_label-GM_mask.nii.gz',
                path2+'/output/cpac_cpac_abcd-options/sub-'+sub+'a_ses-1/anat/sub-'+sub+'a_ses-1_label-WM_mask.nii.gz',
                path2+'/working/cpac_sub-'+sub+'a_ses-1/resample_anat_brain_mask_in_standard_125/wmparc_maths_fill_holes_maths_warp_warp_warp.nii.gz',
                glob.glob(path2+'/working/cpac_sub-'+sub+'a_ses-1/_*/*mcflirt_122/*par')[0], 
                # glob.glob(path2+'/sub-'+sub+'/output/*/sub-'+sub+ses+'_ses-1/frame_wise_displacement_power/*/FD.1D')[0], # TODO find FD, only max/rel disp
                f'{PH_SERVER_ROOT}/freesurfer/DCAN-HCP/global/templates/MNI152_T1_1mm_brain.nii.gz', # ABCD anat template
                f'{PH_SERVER_ROOT}/freesurfer/DCAN-HCP/global/templates/MNI152_T1_1mm_brain.nii.gz', # C-PAC anat template
                '/usr/local/fsl/data/standard/MNI152_T1_2mm_brain.nii.gz', # ABCD func template on Lisa
                '/usr/local/fsl/data/standard/MNI152_T1_2mm_brain.nii.gz', # C-PAC func template on Lisa
                # '/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz', # ABCD func template on Ned
                # '/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz', # C-PAC func template on Ned
                path1+'/sub-'+sub+'/ses-1/files/T1w/T1w_acpc_dc_restore_brain.nii.gz', # ABCD T1
                glob.glob(path2+'/working/cpac_sub-'+sub+'a_ses-1/brain_extraction_*/*.nii.gz')[0], # C-PAC T1
                path2+'/output/cpac_cpac_abcd-options/sub-'+sub+'a_ses-1/anat/sub-'+sub+'a_ses-1_space-template_desc-brain_T1w.nii.gz', # C-PAC anat to standard
                path2+'/output/cpac_cpac_abcd-options/sub-'+sub+'a_ses-1/func/sub-'+sub+'a_ses-1_task-rest_run-1_space-template_desc-mean_bold.nii.gz', # C-PAC func to standard
                glob.glob(path2+'/working/cpac_sub-'+sub+'a_ses-1/func_to_anat_FLIRT_*/_*/linear_func_to_anat/*flirt.nii.gz')[0]] # C-PAC func in T1 space

    for num_var, var in enumerate(var_list):

        file1 = path_list1[num_var]
        file2 = path_list2[num_var]

        if '.nii.gz' in file1:
            img1 = nb.load(file1)
            data1 = img1.get_fdata()
            # data1 = img1.get_data()
            img2 = nb.load(file2)
            data2 = img2.get_fdata()
            # data2 = img2.get_data()
        elif '.par' in file1:
            data1 = get_motion_params(file1, 'abcd')
            data2 = get_motion_params(file2)
        elif '.mat' in file1:
            data1 = sio.loadmat(file1)['FD']
            data2 = np.expand_dims(np.loadtxt(file2)[1:], axis=1)

        if var == 'motion':
            motion_params = correlation(data1, data2)
            corr = motion_params.diagonal()
        elif isinstance(data1, np.ndarray) and data1.shape == data2.shape:
            corr, _ = pearsonr(data1.flatten(), data2.flatten())

        print(sub + ' ' + str(num_var) + ' ' + var)
        print(corr)

        if num_var < motion_index:
            corrs[num_sub][num_var] = round(corr, 3)
        elif num_var == motion_index:
            corrs[num_sub][num_var:num_var+6] = corr
        elif num_var > motion_index:
            corrs[num_sub][num_var+5] = round(corr, 3)

print(corrs)
np.save(f'{os.environ.get("SCRIPT_DIR")}/abcd_corrs.npy', corrs)