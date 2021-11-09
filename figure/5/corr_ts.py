import os
import math
import numpy as np
import nibabel as nb

dataout = '/data3/cnl/xli/reproducibility/correlation'

resolution = 'native' #'2mm'

if resolution == '2mm':
    img3d = '/data3/cnl/xli/reproducibility/out/fmriprep/fmriprep_mni152_2mm/output/fmriprep/sub-0025427a/func/sub-0025427a_task-rest_run-1_space-MNI152NLin6Asym_res-2_desc-mean_brain_bold.nii.gz'
else:
    img3d = '/data3/cnl/xli/reproducibility/out/fmriprep/fmriprep_mni2004_native/output/fmriprep/sub-0025427a/func/sub-0025427a_task-rest_run-1_space-MNI1522004_desc-mean_brain_bold.nii.gz'

for s, subid in enumerate(range(27,57)):
    sub = 'sub-00254'+str(subid)+'a'
    print(sub)

    if resolution == '2mm':
        dimx = 91
        dimy = 109
        dimz = 91
    else:
        dimx = 54
        dimy = 64
        dimz = 54
    
    corr2001_2006 = np.zeros( ( dimx, dimy, dimz ) )
    corr2001_2009 = np.zeros( ( dimx, dimy, dimz ) )
    corr2006_2009 = np.zeros( ( dimx, dimy, dimz ) )

    if resolution == '2mm':
        t2001_path='/data3/cnl/xli/reproducibility/out/fmriprep/fmriprep_mni2004_2mm/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI1522004_res-2_desc-resampled_brain_bold_lpi.nii.gz'
        t2006_path='/data3/cnl/xli/reproducibility/out/fmriprep/fmriprep_mni152_2mm/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI152NLin6Asym_res-2_desc-brain_bold.nii.gz'
        t2009_path='/data3/cnl/xli/reproducibility/out/fmriprep/fmriprep_mni2009_2mm/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI152NLin2009cAsym_res-2_desc-resampled_brain_bold_lpi.nii.gz'
    else:
        t2001_path='/data3/cnl/xli/reproducibility/out/fmriprep/fmriprep_mni2004_native/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI1522004_desc-brain_bold.nii.gz'
        t2006_path='/data3/cnl/xli/reproducibility/out/fmriprep/fmriprep_mni152_native/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI152NLin6Asym_desc-brain_bold.nii.gz'
        t2009_path='/data3/cnl/fmriprep/Lei_working/FINAL_preprocessed_2021/fmriprep_default/output/fmriprep/'+sub+'/func/'+sub+'_task-rest_run-1_space-MNI152NLin2009cAsym_desc-resampled_brain_bold.nii.gz'

    t2001 = nb.load(t2001_path).get_data()
    t2006 = nb.load(t2006_path).get_data()
    t2009 = nb.load(t2009_path).get_data()

    for x in range(dimx):
        for y in range(dimy):
            for z in range(dimz):
                corr2001_2006[x, y, z] = np.corrcoef(t2001[x, y, z], t2006[x, y, z])[1,0]
                if math.isnan(corr2001_2006[x,y,z]):
                    corr2001_2006[x, y, z] = 0
                # print('2001 vs 2006 completed')
                
                corr2001_2009[x, y, z] = np.corrcoef(t2001[x, y, z], t2009[x, y, z])[1,0]
                if math.isnan(corr2001_2009[x,y,z]):
                    corr2001_2009[x, y, z] = 0
                # print('2001 vs 2009 completed')

                corr2006_2009[x, y, z] = np.corrcoef(t2006[x, y, z], t2009[x, y, z])[1,0]
                if math.isnan(corr2006_2009[x,y,z]):
                    corr2006_2009[x, y, z] = 0
                # print('2006 vs 2009 completed')

    output_img = nb.Nifti1Image(corr2001_2006, affine=nb.load(img3d).get_affine())
    out_file = os.path.join(dataout, '2001_2006_'+resolution, sub+'.nii.gz')
    output_img.to_filename(out_file)

    output_img = nb.Nifti1Image(corr2001_2009, affine=nb.load(img3d).get_affine())
    out_file = os.path.join(dataout, '2001_2009_'+resolution, sub+'.nii.gz')
    output_img.to_filename(out_file)

    output_img = nb.Nifti1Image(corr2006_2009, affine=nb.load(img3d).get_affine())
    out_file = os.path.join(dataout, '2006_2009_'+resolution, sub+'.nii.gz')
    output_img.to_filename(out_file)