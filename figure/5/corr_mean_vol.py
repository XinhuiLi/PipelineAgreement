import subprocess
import numpy as np

# 2mm
corr = np.zeros( (3,30) )
for i, subid in enumerate(range(27,57)):
    sub = 'sub-00254'+str(subid)+'a'
    print(sub)

    t2004='/data3/cnl/xli/reproducibility/out/fmriprep/fmriprep_mni2004_2mm/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI1522004_res-2_desc-mean_brain_bold_lpi.nii.gz'
    t2006='/data3/cnl/xli/reproducibility/out/fmriprep/fmriprep_mni152_2mm/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI152NLin6Asym_res-2_desc-mean_brain_bold.nii.gz'
    t2009='/data3/cnl/xli/reproducibility/out/fmriprep/fmriprep_mni2009_2mm/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI152NLin2009cAsym_res-2_desc-mean_resampled_brain_bold.nii.gz'

    cmd = ['3ddot', t2004, t2006]
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    corr[0,i] = float(output[-10:-2])

    cmd = ['3ddot', t2004, t2009]
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    corr[1,i] = float(output[-10:-2])

    cmd = ['3ddot', t2006, t2009]
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    corr[2,i] = float(output[-10:-2])

np.save('/data3/cnl/xli/reproducibility/script/corr_2mm.npy', corr)

# native
corr = np.zeros( (3,30) )
for i, subid in enumerate(range(27,57)):
    sub = 'sub-00254'+str(subid)+'a'
    print(sub)

    t2004='/data3/cnl/xli/reproducibility/out/fmriprep/fmriprep_mni2004_native/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI1522004_desc-mean_brain_bold.nii.gz'
    t2006='/data3/cnl/xli/reproducibility/out/fmriprep/fmriprep_mni152_native/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI152NLin6Asym_desc-mean_brain_bold.nii.gz'
    t2009='/data3/cnl/fmriprep/Lei_working/FINAL_preprocessed_2021/fmriprep_default/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI152NLin2009cAsym_desc-mean_resampled_brain_bold.nii.gz'

    cmd = ['3ddot', t2004, t2006]
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    corr[0,i] = float(output[-10:-2])

    cmd = ['3ddot', t2004, t2009]
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    corr[1,i] = float(output[-10:-2])

    cmd = ['3ddot', t2006, t2009]
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    corr[2,i] = float(output[-10:-2])

np.save('/data3/cnl/xli/reproducibility/script/corr_native.npy', corr)