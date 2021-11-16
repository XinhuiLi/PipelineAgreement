import os, glob
import numpy as np
from scipy.stats import pearsonr

sub_list = []
sub_list_file = '/data3/cnl/fmriprep/Lei_working/FD_testing/HBN_testing/sublist.txt'
with open(sub_list_file) as f:
    lines = f.readlines()
    for line in lines:
        sub_list.append(line.strip('\n').replace('_', '-'))

good_sub_list = []
good_sub_list_file = '/data3/cnl/fmriprep/Lei_working/FD_testing/HBN_testing/good_30.txt'
with open(good_sub_list_file) as f:
    lines = f.readlines()
    for line in lines:
        good_sub_list.append(line.strip('\n').replace('_', '-'))

bad_sub_list = []
for sub in sub_list:
    if sub not in good_sub_list:
        bad_sub_list.append(sub)

print('subject list length: ' + str(len(sub_list)))
print('good subject list length: ' + str(len(good_sub_list)))
print('bad subject list length: ' + str(len(bad_sub_list)))

def get_fd_corr(sub_list, type, name):

    run_path = '/data3/cnl/sgia/XinMotion/runs/'
    afni = 'v181-MotionVariation'
    afni_last_folder = 'v181-MotionVariation-last'
    fsl = 'v181-MotionVariation-MC'
    fsl_last_folder = 'v181-MotionVariation-last-MC'

    afni_mean, afni_median, afni_first, afni_last, fsl_mean, fsl_median, fsl_first, fsl_last = [], [], [], [], [], [], [], []

    for sub in sub_list:
        print(sub)
        # mean volume 1
        afni_mean_file = glob.glob(run_path+afni+'/output/cpac_cpac-default-pipeline/'+sub+'_ses-1/func/'+sub+'_ses-1_task-movieTP_desc-1_framewise-displacement-'+type+'.1D')[0]
        afni_mean.append(np.loadtxt(afni_mean_file))
        fsl_mean_file = glob.glob(run_path+fsl+'/output/cpac_cpac-default-pipeline/'+sub+'_ses-1/func/'+sub+'_ses-1_task-movieTP_desc-1_framewise-displacement-'+type+'.1D')[0]
        fsl_mean.append(np.loadtxt(fsl_mean_file))

        # median volume 2
        afni_median_file = glob.glob(run_path+afni+'/output/cpac_cpac-default-pipeline/'+sub+'_ses-1/func/'+sub+'_ses-1_task-movieTP_desc-2_framewise-displacement-'+type+'.1D')[0]
        afni_median.append(np.loadtxt(afni_median_file))
        fsl_median_file = glob.glob(run_path+fsl+'/output/cpac_cpac-default-pipeline/'+sub+'_ses-1/func/'+sub+'_ses-1_task-movieTP_desc-2_framewise-displacement-'+type+'.1D')[0]
        fsl_median.append(np.loadtxt(fsl_median_file))

        # first volume 3
        afni_first_file = glob.glob(run_path+afni+'/output/cpac_cpac-default-pipeline/'+sub+'_ses-1/func/'+sub+'_ses-1_task-movieTP_desc-3_framewise-displacement-'+type+'.1D')[0]
        afni_first.append(np.loadtxt(afni_first_file))
        fsl_first_file = glob.glob(run_path+fsl+'/output/cpac_cpac-default-pipeline/'+sub+'_ses-1/func/'+sub+'_ses-1_task-movieTP_desc-3_framewise-displacement-'+type+'.1D')[0]
        fsl_first.append(np.loadtxt(fsl_first_file))

        # last volume
        afni_last_file = glob.glob(run_path+afni_last_folder+'/output/cpac_cpac-default-pipeline/'+sub+'_ses-1/func/'+sub+'_ses-1_task-movieTP_framewise-displacement-'+type+'.1D')[0]
        afni_last.append(np.loadtxt(afni_last_file))
        fsl_last_file = glob.glob(run_path+fsl_last_folder+'/output/cpac_cpac-default-pipeline/'+sub+'_ses-1/func/'+sub+'_ses-1_task-movieTP_framewise-displacement-'+type+'.1D')[0]
        fsl_last.append(np.loadtxt(fsl_last_file))

    print('AFNI mean')
    print( np.mean(afni_mean), np.std(afni_mean) )
    print('FSL mean')
    print( np.mean(fsl_mean), np.std(fsl_mean) )
    print('AFNI median')
    print( np.mean(afni_median), np.std(afni_median) )
    print('FSL median')
    print( np.mean(fsl_median), np.std(fsl_median) )
    print('AFNI first')
    print( np.mean(afni_first), np.std(afni_first) )
    print('FSL first')
    print( np.mean(fsl_first), np.std(fsl_first) )
    print('AFNI last')
    print( np.mean(afni_last), np.std(afni_last) )
    print('FSL last')
    print( np.mean(fsl_last), np.std(fsl_last) )
    
    print('total')
    print( np.mean( [afni_mean, fsl_mean, afni_median, fsl_median, afni_first, fsl_first, afni_last, fsl_last] ), np.std([afni_mean, fsl_mean, afni_median, fsl_median, afni_first, fsl_first, afni_last, fsl_last]) )

    afni = np.zeros( (6, 30) )
    fsl = np.zeros( (6, 30) )

    for i, sub in enumerate(sub_list):
        afni[0, i], _ = pearsonr( afni_mean[i], afni_median[i] )
        afni[1, i], _ = pearsonr( afni_mean[i], afni_first[i] )
        afni[2, i], _ = pearsonr( afni_mean[i], afni_last[i] )
        afni[3, i], _ = pearsonr( afni_median[i], afni_first[i] )
        afni[4, i], _ = pearsonr( afni_median[i], afni_last[i] )
        afni[5, i], _ = pearsonr( afni_first[i], afni_last[i] )

        fsl[0, i], _ = pearsonr( fsl_mean[i], fsl_median[i] )
        fsl[1, i], _ = pearsonr( fsl_mean[i], fsl_first[i] )
        fsl[2, i], _ = pearsonr( fsl_mean[i], fsl_last[i] )
        fsl[3, i], _ = pearsonr( fsl_median[i], fsl_first[i] )
        fsl[4, i], _ = pearsonr( fsl_median[i], fsl_last[i] )
        fsl[5, i], _ = pearsonr( fsl_first[i], fsl_last[i] )
    
    np.save('/data3/cnl/xli/reproducibility/script/HBN_AFNI_FD_'+type+'_'+name+'.npy', afni)
    np.save('/data3/cnl/xli/reproducibility/script/HBN_FSL_FD_'+type+'_'+name+'.npy', fsl)

get_fd_corr(good_sub_list, 'power', 'good')
get_fd_corr(bad_sub_list, 'power', 'bad')
get_fd_corr(good_sub_list, 'jenkinson', 'good')
get_fd_corr(bad_sub_list, 'jenkinson', 'bad')