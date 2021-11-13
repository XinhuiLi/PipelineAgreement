import os, glob
import numpy as np

sub_list = []
sub_list_file = '/data3/cnl/fmriprep/Lei_working/FD_testing/HBN_testing/sublist.txt'
with open(sub_list_file) as f:
    lines = f.readlines()
    for line in lines:
        sub_list.append(line.strip('\n').replace('_', '-'))
sub_list.remove('sub-000000')
sub_list.remove('sub-5463599')
sub_list.remove('sub-5713772')

run_path = '/data3/cnl/sgia/XinMotion/runs/'
afni = 'v181-MotionVariation'
afni_last_folder = 'v181-MotionVariation-last'
fsl = 'v181-MotionVariation-MC'
fsl_last_folder = 'v181-MotionVariation-last-MC'

out_dir = '/data3/cnl/fmriprep/Lei_working/Finalizing/Minimal/data/'
os.chdir(out_dir)

for tool in ['afni', 'fsl']:
    for ref in ['mean', 'median', 'first', 'last']:
        folder_name = 'motion_' + str(tool) + '_' + str(ref) + ''
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

for sub in sub_list:
    print(sub)
    # mean volume 1
    afni_mean_file = glob.glob(run_path+afni+'/output/cpac_cpac-default-pipeline/'+sub+'_ses-1/func/'+sub+'_ses-1_task-movieTP_space-EPItemplate_desc-brain-1_bold.nii.gz')[0]
    fsl_mean_file = glob.glob(run_path+fsl+'/output/cpac_cpac-default-pipeline/'+sub+'_ses-1/func/'+sub+'_ses-1_task-movieTP_space-EPItemplate_desc-brain-1_bold.nii.gz')[0]

    cmd = 'ln -s %s %s' % (afni_mean_file, out_dir+'motion_afni_mean/'+sub+'.nii.gz')
    os.system(cmd)
    
    cmd = 'ln -s %s %s' % (fsl_mean_file, 'motion_fsl_mean/'+sub+'.nii.gz')
    os.system(cmd)

    # median volume 2
    afni_median_file = glob.glob(run_path+afni+'/output/cpac_cpac-default-pipeline/'+sub+'_ses-1/func/'+sub+'_ses-1_task-movieTP_space-EPItemplate_desc-brain-2_bold.nii.gz')[0]
    fsl_median_file = glob.glob(run_path+fsl+'/output/cpac_cpac-default-pipeline/'+sub+'_ses-1/func/'+sub+'_ses-1_task-movieTP_space-EPItemplate_desc-brain-2_bold.nii.gz')[0]

    cmd = 'ln -s %s %s' % (afni_median_file, 'motion_afni_median/'+sub+'.nii.gz')
    os.system(cmd)
    
    cmd = 'ln -s %s %s' % (fsl_median_file, 'motion_fsl_median/'+sub+'.nii.gz')
    os.system(cmd)

    # first volume 3
    afni_first_file = glob.glob(run_path+afni+'/output/cpac_cpac-default-pipeline/'+sub+'_ses-1/func/'+sub+'_ses-1_task-movieTP_space-EPItemplate_desc-brain-3_bold.nii.gz')[0]
    fsl_first_file = glob.glob(run_path+fsl+'/output/cpac_cpac-default-pipeline/'+sub+'_ses-1/func/'+sub+'_ses-1_task-movieTP_space-EPItemplate_desc-brain-3_bold.nii.gz')[0]

    cmd = 'ln -s %s %s' % (afni_first_file, 'motion_afni_first/'+sub+'.nii.gz')
    os.system(cmd)
    
    cmd = 'ln -s %s %s' % (fsl_first_file, 'motion_fsl_first/'+sub+'.nii.gz')
    os.system(cmd)

    # last volume
    afni_last_file = glob.glob(run_path+afni_last_folder+'/output/cpac_cpac-default-pipeline/'+sub+'_ses-1/func/'+sub+'_ses-1_task-movieTP_space-EPItemplate_desc-brain_bold.nii.gz')[0]
    fsl_last_file = glob.glob(run_path+fsl_last_folder+'/output/cpac_cpac-default-pipeline/'+sub+'_ses-1/func/'+sub+'_ses-1_task-movieTP_space-EPItemplate_desc-brain_bold.nii.gz')[0]

    cmd = 'ln -s %s %s' % (afni_last_file, 'motion_afni_last/'+sub+'.nii.gz')
    os.system(cmd)
    
    cmd = 'ln -s %s %s' % (fsl_last_file, 'motion_fsl_last/'+sub+'.nii.gz')
    os.system(cmd)