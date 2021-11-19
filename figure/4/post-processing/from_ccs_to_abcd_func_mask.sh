# Note: For sub-0025448a, use ABCD func mask

cd ${DATA_INPUT_DIR}/source_of_var/from_ccs_to_abcd/func_mask_v2

for ((subid=27;subid<57;subid++));do
    echo ${subid}

    head1=/outputs/working/cpac_sub-00254${subid}a_ses-1/_scan_rest_run-1/func_motion_correct_3dvolreg_115/mapflow/_func_motion_correct_3dvolreg_1150/sub-00254${subid}a_task-rest_run-1_bold_calc_despike_tshift_resample_0_volreg.nii.gz
    head2=/outputs/working/cpac_sub-00254${subid}a_ses-1/_scan_rest_run-1/func_motion_correct_3dvolreg_115/mapflow/_func_motion_correct_3dvolreg_1151/sub-00254${subid}a_task-rest_run-1_bold_calc_despike_tshift_resample_1_volreg.nii.gz
    head=sub-00254${subid}a_head.nii.gz

    xfm=/outputs/working/cpac_sub-00254${subid}a_ses-1/create_func_to_T1wtemplate_xfm_124/_scan_rest_run-1/write_composite_xfm/from-bold_to-template_mode-image_xfm.nii.gz
    abcd_func_mask=${DATA_INPUT_DIR}/cpac_abcd/working/cpac_sub-00254${subid}a_ses-1/resample_anat_brain_mask_in_standard_125/wmparc_maths_fill_holes_maths_warp_warp_warp.nii.gz
    abcd_func_mask_resampled=sub-00254${subid}a_abcd_func_mask_resampled.nii.gz
    head_std=sub-00254${subid}a_head_to_standard.nii.gz
    brain_std=sub-00254${subid}a_brain_to_standard.nii.gz

    3dTcat -prefix ${head} ${head1} ${head2}
    applywarp --in=${head} --ref=/usr/share/fsl/5.0/data/standard/MNI152_T1_3mm_brain.nii.gz --out=${head_std} --warp=/outputs/working/cpac_sub-00254${subid}a_ses-1/create_func_to_T1wtemplate_xfm_155/_scan_rest_run-1/combine_fsl_warps/MNI152_T1_3mm_brain_concatwarp.nii.gz --interp=trilinear
    3dresample -dxyz 3 3 3 -input ${abcd_func_mask} -prefix ${abcd_func_mask_resampled}
    fslmaths ${head_std} -mas ${abcd_func_mask_resampled} -thr 0 -ing 10000 ${brain_std} -odt float
done

mask=${PH_SERVER_WORKING_ROOT}/Finalizing/Schaefer_Atlas/Schaefer2018_200Parcels_7Networks_order_FSLMNI152_3mm.nii.gz
out_path=${DATA_INPUT_DIR}/source_of_var/from_ccs_to_abcd/func_mask_v2
data_path=${PH_SERVER_DATA_ROOT}/analysis/data/from_ccs_to_abcd/func_mask_v2
roi_path=${PH_SERVER_DATA_ROOT}/analysis/ROI200/from_ccs_to_abcd/func_mask_v2

mkdir ${data_path}
mkdir ${roi_path}
cd ${data_path}

for ((subid=27;subid<57;subid++));do
    brain_std=${out_path}/sub-00254${subid}a_brain_to_standard.nii.gz
    infile=sub-00254${subid}a.nii.gz
    outfile=${roi_path}/sub-00254${subid}a.1D
    echo ${infile}
    ln -s ${brain_std} ${infile}
    3dROIstats -quiet -mask ${mask} -1Dformat ${infile} > ${outfile}
done