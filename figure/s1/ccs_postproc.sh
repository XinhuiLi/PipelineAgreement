SUBJECTS_DIR=${PH_SERVER_WORKING_ROOT}/FINAL_preprocessed_2021/ccs
for ((k=27;k<57;k++)); do
    cd ${SUBJECTS_DIR}/sub-00254${k}/anat/segment
    3dresample -orient rpi -inset segment_csf.nii.gz -prefix segment_csf_rpi.nii.gz
    3dresample -orient rpi -inset segment_wm.nii.gz -prefix segment_wm_rpi.nii.gz
done

CPAC_DIR=${DATA_INPUT_DIR}/cpac_ccs
for ((k=27;k<57;k++)); do
    cd ${CPAC_DIR}/working/cpac_sub-00254${k}a_ses-1/anat_preproc_freesurfer_43/anat_freesurfer/recon_all/mri
    # brain mask
    3dresample -input brainmask.nii.gz -prefix brainmask_rpi.nii.gz -orient rpi
    fslmaths brainmask_rpi.nii.gz -abs -bin brainmask_rpi_abs_bin.nii.gz
    
    # segmentation
    mri_binarize --i aseg.mgz --o segment_wm.nii.gz --match 2 41 7 46 251 252 253 254 255 --erode 1
    mri_binarize --i aseg.mgz --o segment_csf.nii.gz --match 4 5 43 44 31 63 --erode 1
done