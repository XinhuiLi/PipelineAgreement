''' CCS may require extra processing
# tissue anat/segment
3dresample -orient rpi -inset segment_csf.nii.gz -prefix segment_csf_rpi.nii.gz 
3dresample -orient rpi -inset segment_wm.nii.gz -prefix segment_wm_rpi.nii.gz 

# anat2std anat/reg
applywarp --ref=/usr/local/fsl/data/standard/MNI152_T1_2mm.nii.gz --in=highres.nii.gz --out=fnirt_highres2standard_brain.nii.gz --warp=highres2standard_warp.nii.gz

# func2std (nuisance) func1
fslmaths rest.sm0.mni152.nii.gz -Tmean -mul -1 -add rest.sm0.mni152.nii.gz rest.sm0.mni152.demeaned.nii.gz

# func2std (minimal) func1
applywarp --ref=${PH_SERVER_ROOT}/xli/cpac_features/ccs/code/Ting/CCS/templates/MNI152_T1_3mm.nii.gz --in=rest_gms.nii.gz --out=rest_gms_mni152.nii.gz --warp=../anat/reg/highres2standard_warp.nii.gz --premat=reg/example_func2highres.mat

# ccs_02_xt_funcbbregister.sh
convert_xfm -omat flirt.mat -concat flirt_rsp2rsp.mtx rpi2rsp.mat
cp flirt.mat example_func2highres.mat
convert_xfm -inverse -omat highres2example_func.mat example_func2highres.mat
'''

import glob
import numpy as np
import nibabel as nb
import os
import scipy.io as sio
from scipy.stats import pearsonr

def zscore(data, axis):
    data -= data.mean(axis=axis, keepdims=True)
    data /= data.std(axis=axis, keepdims=True)
    return np.nan_to_num(data)

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

    if type(file) == list:
        data1 = np.genfromtxt(file[0]).T
        data2 = np.genfromtxt(file[1]).T
        data = np.concatenate((data1, data2),axis=1)
    else:
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

path1 = f'{os.environ.get("PH_SERVER_WORKING_ROOT")}/FINAL_preprocessed_2021/ccs'
path2 = f'{os.environ.get("DATA_INPUT_DIR")}/cpac_ccs'

sub_list = range(25427,25457)
sub_list.remove(25430)

var_list = ['anat mask', 
    'CSF', 'WM', 
    'func mask', 'motion', 
    'anat-mni ccs', 'anat-mni cpac', 'func-mni ccs', 'func-mni ccs', 
    'anat-mni', 'func-mni']
# 'FD',
# 'func-t1 ccs', 'func-t1 cpac',
# 'func-t1'

if 'motion' in var_list:
    motion_index = var_list.index('motion')
corrs = np.zeros((len(sub_list), len(var_list)+5))

for num_sub, sub in enumerate(sub_list):

    sub = '00'+str(sub)

    # TODO segment
    # anat mask and segmentations are in different space
    path_list1 = [path1+'/sub-'+sub+'/anat/vcheck/brain_fs_mask.nii.gz', # FS brain mask
                path1+'/sub-'+sub+'/anat/segment/segment_csf.nii.gz',
                path1+'/sub-'+sub+'/anat/segment/segment_wm.nii.gz',
                path1+'/sub-'+sub+'/func/rest_pp_mask.nii.gz',
                path1+'/sub-'+sub+'/func/rest_mc.1D', # 6 motion parameters # FD
                # path1+'/sub-'+sub+'/func/QC/FD1.mat', # mat file
                path1+'/sub-'+sub+'/anat/reg/fnirt_highres2standard_brain.nii.gz', # CCS anat to standard head # TODO SS, which mask?
                path2+'/output/cpac_cpac_ccs-options/sub-'+sub+'a_ses-1/anat/sub-'+sub+'a_ses-1_space-template_desc-brain-1_T1w.nii.gz', # C-PAC anat to standard
                path1+'/sub-'+sub+'/func/rest_gms_mni152_mean.nii.gz', # CCS func to standard brain
                path2+'/output/cpac_cpac_ccs-options/sub-'+sub+'a_ses-1/func/sub-'+sub+'a_ses-1_task-rest_run-1_space-template_desc-mean_bold.nii.gz', # C-PAC func to standard
                # path1+'/sub-'+sub+'/func/reg/example_func2standard.nii.gz', # CCS func in T1 brain 91x109x91
                # glob.glob(path2+'/working/cpac_sub-'+sub+'_ses-1/func_to_anat_bbreg_*/_*/bbreg_func_to_anat/*flirt.nii.gz')[0], # C-PAC func in T1 brain 256x256x256
                path1+'/sub-'+sub+'/anat/reg/fnirt_highres2standard_brain.nii.gz', # CCS anat to standard
                path1+'/sub-'+sub+'/func/rest_gms_mni152_mean.nii.gz'] # CCS func to standard brain
                # path1+'/sub-'+sub+'/func/reg/example_func2standard.nii.gz']

    path_list2 = [path2+'/working/cpac_sub-'+sub+'a_ses-1/anat_preproc_freesurfer_43/anat_freesurfer/recon_all/mri/brainmask_rpi_abs_bin.nii.gz',
                path2+'/working/cpac_sub-'+sub+'a_ses-1/anat_preproc_freesurfer_43/anat_freesurfer/recon_all/mri/segment_csf.nii.gz',
                path2+'/working/cpac_sub-'+sub+'a_ses-1/anat_preproc_freesurfer_43/anat_freesurfer/recon_all/mri/segment_wm.nii.gz',
                glob.glob(path2+'/working/cpac_sub-'+sub+'a_ses-1/_*/func_mask_*/*.nii.gz')[0],
                [glob.glob(path2+'/working/cpac_sub-'+sub+'a_ses-1/_*/func_motion_correct_3dvolreg*/mapflow/_*/*resample_0.1D')[0],glob.glob(path2+'/working/cpac_sub-'+sub+'a_ses-1/_*/func_motion_correct_3dvolreg*/mapflow/_*/*resample_1.1D')[0]],
                # path2+'/output/cpac_cpac_ccs-options/sub-'+sub+'_ses-1/func/sub-'+sub+'_ses-1_task-rest_run-1_framewise-displacement-power.1D',
                '/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz', # CCS anat template
                '/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz', # C-PAC anat template
                '/usr/share/fsl/5.0/data/standard/MNI152_T1_3mm_brain.nii.gz', # CCS func template
                '/usr/share/fsl/5.0/data/standard/MNI152_T1_3mm_brain.nii.gz', # C-PAC func template
                path2+'/output/cpac_cpac_ccs-options/sub-'+sub+'a_ses-1/anat/sub-'+sub+'a_ses-1_space-template_desc-brain-1_T1w.nii.gz', # C-PAC anat to standard
                path2+'/output/cpac_cpac_ccs-options/sub-'+sub+'a_ses-1/func/sub-'+sub+'a_ses-1_task-rest_run-1_space-template_desc-mean_bold.nii.gz'] # C-PAC func to standard

    for num_var, var in enumerate(var_list):

        file1 = path_list1[num_var]
        file2 = path_list2[num_var]

        if '.nii.gz' in file1:
            img1 = nb.load(file1)
            # data1 = img1.get_fdata()
            data1 = img1.get_data() # ned
            img2 = nb.load(file2)
            # data2 = img2.get_fdata()
            data2 = img2.get_data() # ned
        elif '.1D' in file1:
            data1 = get_motion_params(file1)
            data2 = get_motion_params(file2)
        elif '.mat' in file1:
            data1 = sio.loadmat(file1)['FD1']
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
np.save(f'{os.environ.get("SCRIPT_DIR")}/ccs_corrs.npy', corrs)