import glob
import numpy as np
import pandas as pd 
import nibabel as nb
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

path1 = '/data3/cnl/fmriprep/Lei_working/FINAL_preprocessed_2021/fmriprep_default'
path2 = '/data3/cnl/xli/reproducibility/out/cpac_fmriprep_v2'

sub_list = range(25427,25457)
sub_list.remove(25430)

var_list = ['anat mask', 'CSF', 'GM', 'WM', 'func mask', 'motion', 
    'anat-mni fmriprep', 'anat-mni cpac', 'func-mni fmriprep', 'func-mni cpac', 'anat-mni', 'func-mni']

# 'func-t1 fmriprep', 'func-t1 cpac', 'func-t1'
if 'motion' in var_list:
    motion_index = var_list.index('motion')
corrs = np.zeros((len(sub_list), len(var_list)+5))

for num_sub, sub in enumerate(sub_list):

    sub = '00'+str(sub)

    path_list1 = [path1+'/output/fmriprep/sub-'+sub+'a/anat/sub-'+sub+'a_run-1_desc-brain_mask_rpi.nii.gz', # anat mask
                path1+'/working/fmriprep_wf/single_subject_'+sub+'a_wf/anat_preproc_wf/t1w_dseg/sub-'+sub+'a_run-1_T1w_ras_valid_corrected_xform_masked_pveseg_rpi_csf.nii.gz', # CSF
                path1+'/working/fmriprep_wf/single_subject_'+sub+'a_wf/anat_preproc_wf/t1w_dseg/sub-'+sub+'a_run-1_T1w_ras_valid_corrected_xform_masked_pveseg_rpi_gm.nii.gz', # GM
                path1+'/working/fmriprep_wf/single_subject_'+sub+'a_wf/anat_preproc_wf/t1w_dseg/sub-'+sub+'a_run-1_T1w_ras_valid_corrected_xform_masked_pveseg_rpi_wm.nii.gz', # WM
                path1+'/working/fmriprep_wf/single_subject_'+sub+'a_wf/func_preproc_task_rest_run_1_wf/final_boldref_wf/enhance_and_skullstrip_bold_wf/combine_masks/ref_bold_corrected_brain_mask_maths.nii.gz', # func mask
                glob.glob(path1+'/working/fmriprep_wf/single_subject_'+sub+'a_wf/func*/bold_hmc_wf/mcflirt/*par')[0],
                glob.glob(path1+'/output/fmriprep/sub-'+sub+'a/anat/*MNI152NLin2009cAsym_desc-brain_T1w.nii.gz')[0],
                path2+'/output/cpac_cpac_fmriprep-options/sub-'+sub+'a_ses-1/anat/sub-'+sub+'a_ses-1_space-template_desc-brain_T1w.nii.gz', # C-PAC anat to standard
                glob.glob(path1+'/output/fmriprep/sub-'+sub+'a/func/*MNI152NLin2009cAsym_desc-mean_bold.nii.gz')[0], # fMRIPrep func to standard
                path2+'/output/cpac_cpac_fmriprep-options/sub-'+sub+'a_ses-1/func/sub-'+sub+'a_ses-1_task-rest_run-1_space-template_desc-mean_bold.nii.gz', # C-PAC func to standard
                glob.glob(path1+'/output/fmriprep/sub-'+sub+'a/anat/*MNI152NLin2009cAsym_desc-cpacbrain_T1w.nii.gz')[0], # fMRIPrep anat to standard
                glob.glob(path1+'/output/fmriprep/sub-'+sub+'a/func/*MNI152NLin2009cAsym_desc-mean_bold.nii.gz')[0]] # fMRIPrep func to standard

    path_list2 = [path2+'/output/cpac_cpac_fmriprep-options/sub-'+sub+'a_ses-1/anat/sub-'+sub+'a_ses-1_space-T1w_desc-brain_mask.nii.gz',
                path2+'/working/cpac_sub-'+sub+'a_ses-1/segment_62/segment_pveseg_csf.nii.gz',
                path2+'/working/cpac_sub-'+sub+'a_ses-1/segment_62/segment_pveseg_gm.nii.gz',
                path2+'/working/cpac_sub-'+sub+'a_ses-1/segment_62/segment_pveseg_wm.nii.gz',
                path2+'/output/cpac_cpac_fmriprep-options/sub-'+sub+'a_ses-1/func/sub-'+sub+'a_ses-1_task-rest_run-1_space-bold_desc-brain_mask.nii.gz',
                glob.glob(path2+'/working/cpac_sub-'+sub+'a_ses-1/_*/*mcflirt_97/*par')[0],
                '/data3/cnl/fmriprep/cpac_run/Template/fmriprep_template/tpl-MNI152NLin2009cAsym_res-01_T1w_reference_ss.nii.gz',
                # path1+'/working/fmriprep_wf/single_subject_'+sub+'a_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/gen_ref/tpl-MNI152NLin2009cAsym_res-01_T1w_reference.nii.gz', # fMRIPrep anat template
                '/data3/cnl/fmriprep/cpac_run/Template/fmriprep_template/tpl-MNI152NLin2009cAsym_res-01_desc-brain_T1w.nii.gz', # C-PAC anat template
                '/data3/cnl/fmriprep/cpac_run/Template/fmriprep_template/tpl-MNI152NLin2009cAsym_res-02_T1w_reference_ss.nii.gz', # fMRIPrep func template
                '/data3/cnl/fmriprep/cpac_run/Template/fmriprep_template/tpl-MNI152NLin2009cAsym_res-02_T1w_reference_ss.nii.gz', # C-PAC func template
                path2+'/output/cpac_cpac_fmriprep-options/sub-'+sub+'a_ses-1/anat/sub-'+sub+'a_ses-1_space-template_desc-brain_T1w.nii.gz', # C-PAC anat to standard
                path2+'/output/cpac_cpac_fmriprep-options/sub-'+sub+'a_ses-1/func/sub-'+sub+'a_ses-1_task-rest_run-1_space-template_desc-mean_bold.nii.gz'] # C-PAC func to standard

    for num_var, var in enumerate(var_list):

        file1 = path_list1[num_var]
        file2 = path_list2[num_var]

        if '.par' in file1:
            data1 = get_motion_params(file1)
            data2 = get_motion_params(file2)
        elif '.nii.gz' in file1:
            img1 = nb.load(file1)
            # data1 = img1.get_fdata()
            data1 = img1.get_data()
            img2 = nb.load(file2)
            # data2 = img2.get_fdata()
            data2 = img2.get_data()
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
np.save('/data3/cnl/xli/reproducibility/script/fmriprep_corrs.npy', corrs)

# 3dSkullStrip -input /data3/cnl/fmriprep/Lei_working/FINAL_preprocessed_2021/fmriprep_default/working/fmriprep_wf/single_subject_0025427a_wf/anat_preproc_wf/anat_derivatives_wf/_in_tuple_MNI152NLin2009cAsym.resnative/gen_ref/tpl-MNI152NLin2009cAsym_res-01_T1w_reference.nii.gz -prefix /data3/cnl/fmriprep/cpac_run/Template/fmriprep_template/tpl-MNI152NLin2009cAsym_res-01_T1w_reference_ss.nii.gz