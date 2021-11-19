import os
import glob
import nibabel as nb

orig_path = '/data3/cnl/xli/reproducibility/out/source_of_var'
output_data_path = '/data3/cnl/xli/reproducibility/analysis/data'
output_roi_path = '/data3/cnl/xli/reproducibility/analysis/ROI200'
command_list = '/data3/cnl/xli/reproducibility/analysis/Schaefer_ROI_commands.txt'   

cmd = 'rm %s' % (command_list)
os.system(cmd)

run_list = os.listdir(orig_path)
run_list.sort()

for run in run_list:
    if not os.path.exists(os.path.join(output_data_path, run)):
        os.mkdir(os.path.join(output_data_path, run))

    if not os.path.exists(os.path.join(output_roi_path, run)):
        os.mkdir(os.path.join(output_roi_path, run))

    var_list = os.listdir(os.path.join(orig_path, run))
    var_list.sort()

    for var in var_list:
        if not os.path.exists(os.path.join(output_data_path, run, var)):
            os.mkdir(os.path.join(output_data_path, run, var))
        
        if not os.path.exists(os.path.join(output_roi_path, run, var)):
            os.mkdir(os.path.join(output_roi_path, run, var))
        
        print('Running', run, var)

        # check one subject's data dimension
        try:
            atlas_bold = glob.glob( os.path.join(orig_path, run, var, 'output', '*', 'sub-0025427*', 'func', '*space-template_desc-bold_mask.nii.gz') )[0]
        except:
            try:
                atlas_bold = glob.glob( os.path.join(orig_path, run, var, 'output', '*', 'sub-0025427*', 'func', '*space-template_desc-mean_bold.nii.gz') )[0]
            except:
                print('File not found. Check!')
                continue

        dim = nb.load(atlas_bold).get_data().shape

        for num_roi in [200]: # , 600, 1000
            mni2004_2mm = '/data3/cnl/fmriprep/Lei_working/Finalizing/Schaefer_Atlas/Schaefer2018_'+str(num_roi)+'Parcels_7Networks_order_FSLMNI152_2mm.nii.gz'
            mni2004_3mm = '/data3/cnl/fmriprep/Lei_working/Finalizing/Schaefer_Atlas/Schaefer2018_'+str(num_roi)+'Parcels_7Networks_order_FSLMNI152_3mm.nii.gz'
            mni2009 = '/data3/cnl/fmriprep/Lei_working/Finalizing/Schaefer_Atlas/Schaefer2018_'+str(num_roi)+'Parcels_7Networks_order_FSLMNI152_2mm_NLin2009cAsym.nii.gz' # RPI

            if dim == (91, 109, 91):
                mask = mni2004_2mm # MNI 2004 2mm
            elif dim == (61, 73, 61):
                mask = mni2004_3mm # MNI 2004 3mm
            elif dim == (57, 68, 58):
                mask = mni2009 # MNI 2009

        for sub in range(27,57):
            try: 
                src = glob.glob( os.path.join(orig_path, run, var, 'output', '*', 'sub-00254'+str(sub)+'*', 'func', '*space-template_desc-brain_bold.nii.gz') )[0]
                dest = os.path.join(output_data_path, run, var, 'sub-00254'+str(sub)+'a.nii.gz')
                cmd = 'ln -s %s %s'%(src, dest)
                os.system(cmd)

                dest1D = dest.replace('nii.gz', '1D')
                dest1D = dest1D.replace('/data/', '/ROI200/')
                cmd = "echo '3dROIstats -quiet -mask %s -1Dformat %s >> %s' >> %s" % (mask, dest, dest1D, command_list)
                os.system(cmd)
            except IndexError:
                print(run, var, 'sub-00254'+str(sub), 'not found')

cmd = "cat %s | parallel -j 20" % (command_list)
os.system(cmd)