import os
import subprocess
import numpy as np
import nibabel as nb

DATA_INPUT_DIR = os.environ.get("DATA_INPUT_DIR")
dataout = f'{os.environ.get("PH_SERVER_DATA_ROOT")}/3dcorrelation'
resolution = 'native' #'2mm'

mean = np.zeros( (3, 30) )
std = np.zeros( (3, 30) )
percentile = np.zeros( (9, 30) )

for s, subid in enumerate(range(27,57)):
    sub = 'sub-00254'+str(subid)+'a'
    print(sub)

    if resolution == '2mm':
        t2001=f'{DATA_INPUT_DIR}/fmriprep/fmriprep_mni2004_2mm/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI1522004_res-2_desc-brain_bold.nii.gz'
        t2006=f'{DATA_INPUT_DIR}/fmriprep/fmriprep_mni152_2mm/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI152NLin6Asym_res-2_desc-brain_bold.nii.gz'
        t2009=f'{DATA_INPUT_DIR}/fmriprep/fmriprep_mni2009_2mm/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI152NLin2009cAsym_res-2_desc-brain_bold.nii.gz'
    else:
        t2001=f'{DATA_INPUT_DIR}/fmriprep/fmriprep_mni2004_native/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI1522004_desc-brain_bold.nii.gz'
        t2006=f'{DATA_INPUT_DIR}/fmriprep/fmriprep_mni152_native/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI152NLin6Asym_desc-brain_bold.nii.gz'
        t2009=f'{FMRIPREP_OUTPUT_DIR}/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI152NLin2009cAsym_desc-brain_bold.nii.gz'

    # resample 2001 to 2006
    t2001_in_2006 = t2001.replace('brain_bold', 'brain_bold_2006')
    cmd = '3dresample -master %s -in %s -prefix %s'%(t2006, t2001, t2001_in_2006)
    os.system(cmd)

    # resample 2009 to 2006
    t2009_in_2006 = t2009.replace('brain_bold', 'brain_bold_2006')
    cmd = '3dresample -master %s -in %s -prefix %s'%(t2006, t2009, t2009_in_2006)
    os.system(cmd)

    # correlate TS
    # 2001 vs 2006
    diff_2001_2006 = os.path.join( dataout, resolution, sub+'_diff_2001_2006.nii.gz' )
    cmd = '3dTcorrelate -prefix %s %s %s'%( diff_2001_2006, t2001_in_2006, t2006 )
    os.system(cmd)

    # 2001 vs 2009
    diff_2001_2009 = os.path.join( dataout, resolution, sub+'_diff_2001_2009.nii.gz' )
    cmd = '3dTcorrelate -prefix %s %s %s'%( diff_2001_2009, t2001_in_2006, t2009_in_2006 )
    os.system(cmd)

    # 2006 vs 2009
    diff_2006_2009 = os.path.join( dataout, resolution, sub+'_diff_2006_2009.nii.gz' )
    cmd = '3dTcorrelate -prefix %s %s %s'%( diff_2006_2009, t2009_in_2006, t2006 )
    os.system(cmd)

    # 3dBrickStat -non-zero -mean -stdev diff.nii.gz
    # 2001 vs 2006
    cmd = ['3dBrickStat', '-non-zero', '-mean', '-stdev', diff_2001_2006]
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    mean[0, s] = output.split()[0]
    std[0, s] = output.split()[1]

    # 2001 vs 2009
    cmd = ['3dBrickStat', '-non-zero', '-mean', '-stdev', diff_2001_2009]
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    mean[1, s] = output.split()[0]
    std[1, s] = output.split()[1]

    # 2006 vs 2009
    cmd = ['3dBrickStat', '-non-zero', '-mean', '-stdev', diff_2006_2009]
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    mean[2, s] = output.split()[0]
    std[2, s] = output.split()[1]

    # 3dBrickStat -non-zero -percentile 5 45 95 diff.nii.gz
    # 2001 vs 2006
    cmd = ['3dBrickStat', '-non-zero', '-percentile', '5', '45', '95', diff_2001_2006]
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    percentile[0, s] = output.split()[1]
    percentile[1, s] = output.split()[3]
    percentile[2, s] = output.split()[5]

    # 2001 vs 2009
    cmd = ['3dBrickStat', '-non-zero', '-percentile', '5', '45', '95', diff_2001_2009]
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    percentile[3, s] = output.split()[1]
    percentile[4, s] = output.split()[3]
    percentile[5, s] = output.split()[5]

    # 2006 vs 2009
    cmd = ['3dBrickStat', '-non-zero', '-percentile', '5', '45', '95', diff_2006_2009]
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    percentile[6, s] = output.split()[1]
    percentile[7, s] = output.split()[3]
    percentile[8, s] = output.split()[5]

np.save(os.path.join( dataout, resolution, 'mean.npy') , mean)
np.save(os.path.join( dataout, resolution, 'std.npy') , std)
np.save(os.path.join( dataout, resolution, 'percentile.npy') , percentile)