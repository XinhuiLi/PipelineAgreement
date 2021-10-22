fslsplit /data3/cnl/cpac1.8.1/from_fmriprep_to_ccs_anat_reg_v2/working/cpac_sub-0025428_ses-1/func_slice_timing_correction_89/_scan_rest_run-1/slice_timing/sub-0025428_ses-1_task-rest_run-1_bold_calc_tshift.nii.gz /home/xli/ssr/prevols/vol -t

convertwarp --relout --rel --ref=/home/xli/ssr/prevols/vol0000.nii.gz --warp1=/data3/cnl/fmriprep/Lei_working/CPAC_XCP/ABCD/ABCD_Testing_With_Intermediate/sub-0025427/ses-1/files/task-rest01/task-rest01_gdc_warp.nii.gz --postmat=/data3/cnl/cpac1.8.1/from_fmriprep_to_ccs_anat_reg_v2/working/cpac_sub-0025428_ses-1/_scan_rest_run-1/func_motion_correct_mcflirt_83/sub-0025428_ses-1_task-rest_run-1_bold_calc_mcf.nii.gz.mat/MAT_0000 --out=/home/xli/ssr/warp/vol0000_gdc_warp.nii.gz

convertwarp --relout --rel --ref=/data3/cnl/cpac1.8.1/from_fmriprep_to_ccs_anat_reg_v2/output/cpac_cpac_fmriprep-options/sub-0025428_ses-1/anat/sub-0025428_ses-1_space-template_desc-brain_T1w.nii.gz --warp1=/home/xli/ssr/warp/vol0000_gdc_warp.nii.gz --warp2=${OutputTransform} --out=${MotionMatrixFolder}/${MotionMatrixPrefix}${vnum}_all_warp.nii.gz

fslmaths ${WD}/prevols/vol${vnum}.nii.gz -mul 0 -add 1 ${WD}/prevols/vol${vnum}_mask.nii.gz

applywarp --rel --interp=spline --in=${WD}/prevols/vol${vnum}.nii.gz --warp=${MotionMatrixFolder}/${MotionMatrixPrefix}${vnum}_all_warp.nii.gz --ref=${WD}/${T1wImageFile}.${FinalfMRIResolution} --out=${WD}/postvols/vol${vnum}.nii.gz

applywarp --rel --interp=nn --in=${WD}/prevols/vol${vnum}_mask.nii.gz --warp=${MotionMatrixFolder}/${MotionMatrixPrefix}${vnum}_all_warp.nii.gz --ref=${WD}/${T1wImageFile}.${FinalfMRIResolution} --out=${WD}/postvols/vol${vnum}_mask.nii.gz

###
docker run -i -t --entrypoint='/bin/bash' --rm --security-opt=apparmor:unconfined -v /home/xli:/home/xli -v /data3/cnl/cpac1.8.1/from_fmriprep_to_ccs_anat_reg_v2:/outputs -v /data3:/data3 fcpindi/c-pac:latest

fslsplit /outputs/working/cpac_sub-0025428_ses-1/func_slice_timing_correction_89/_scan_rest_run-1/slice_timing/sub-0025428_ses-1_task-rest_run-1_bold_calc_tshift.nii.gz /home/xli/ssr/prevols/vol -t

convertwarp --relout --rel --ref=/home/xli/ssr/prevols/vol0000.nii.gz --warp1=/data3/cnl/fmriprep/Lei_working/CPAC_XCP/ABCD/ABCD_Testing_With_Intermediate/sub-0025427/ses-1/files/task-rest01/task-rest01_gdc_warp.nii.gz --postmat=/outputs/working/cpac_sub-0025428_ses-1/_scan_rest_run-1/func_motion_correct_mcflirt_83/sub-0025428_ses-1_task-rest_run-1_bold_calc_mcf.nii.gz.mat/MAT_0000 --out=/home/xli/ssr/warp/vol0000_gdc_warp.nii.gz

convertwarp --ref=/usr/share/fsl/5.0/data/standard/MNI152_T1_3mm_brain.nii.gz --premat=/outputs/working/cpac_sub-0025428_ses-1/func_to_anat_bbreg_122/_scan_rest_run-1/bbreg_func_to_anat/uni_masked_flirt.mat --warp1=/home/xli/ssr/warp/vol0000_gdc_warp.nii.gz --warp2=/outputs/working/cpac_sub-0025428_ses-1/register_FSL_anat_to_template_50/cpac_sub-0025428_ses-1/anat_mni_fnirt_register/nonlinear_reg_1/sub-0025428_ses-1_run-1_T1w_resample_noise_corrected_corrected_fieldwarp.nii.gz --out=/home/xli/ssr/warp/vol0000_MNI152_T1_3mm_brain_concatwarp.nii.gz

applywarp --in=/home/xli/ssr/prevols/vol0000.nii.gz --ref=/usr/share/fsl/5.0/data/standard/MNI152_T1_3mm_brain.nii.gz --out=/home/xli/ssr/postvols/vol0000.nii.gz --warp=/home/xli/ssr/warp/vol0000_MNI152_T1_3mm_brain_concatwarp.nii.gz --interp=trilinear

applywarp --in=/outputs/output/cpac_cpac_fmriprep-options/sub-0025428_ses-1/func/sub-0025428_ses-1_task-rest_run-1_space-bold_desc-brain_mask.nii.gz --ref=/usr/share/fsl/5.0/data/standard/MNI152_T1_3mm_brain.nii.gz --out=/home/xli/ssr/postvols/vol0000_mask.nii.gz --warp=/home/xli/ssr/warp/vol0000_MNI152_T1_3mm_brain_concatwarp.nii.gz --interp=nn

fslmaths vol0000.nii.gz -mul vol0000_mask.nii.gz vol0000_brain.nii.gz

3dTcat -prefix vol0000_brain_ccs.nii.gz /data3/cnl/xli/reproducibility/out/cpac_ccs/output/cpac_cpac_ccs-options/sub-0025428a_ses-1/func/sub-0025428a_ses-1_task-rest_run-1_space-template_desc-brain_bold.nii.gz[0]

3dTcat -prefix vol0000_brain_fp-ccs.nii.gz /data3/cnl/cpac1.8.1/from_fmriprep_to_ccs_anat_reg_v4/output/cpac_cpac_fmriprep-options/sub-0025428_ses-1/func/sub-0025428_ses-1_task-rest_run-1_space-template_desc-brain_bold.nii.gz[0]
###

# Apply combined transformations to fMRI (combines gradient non-linearity distortion, motion correction, and registration to T1w space, but keeping fMRI resolution)
WD='/home/xli/ssr'
InputfMRI='/data3/cnl/cpac1.8.1/from_fmriprep_to_ccs_anat_reg_v2/working/cpac_sub-0025428_ses-1/func_slice_timing_correction_89/_scan_rest_run-1/slice_timing/sub-0025428_ses-1_task-rest_run-1_bold_calc_tshift.nii.gz' # STC

mkdir -p ${WD}/prevols
mkdir -p ${WD}/postvols

NumFrames=`fslval ${InputfMRI} dim4`
fslsplit ${InputfMRI} ${WD}/prevols/vol -t
FrameMergeSTRING=""
FrameMergeSTRINGII=""
for ((k=0; k < $NumFrames; k++)); do
  vnum=`zeropad $k 4`
  convertwarp --relout --rel --ref=${WD}/prevols/vol${vnum}.nii.gz --warp1=${GradientDistortionField} --postmat=${MotionMatrixFolder}/${MotionMatrixPrefix}${vnum} --out=${MotionMatrixFolder}/${MotionMatrixPrefix}${vnum}_gdc_warp.nii.gz
  convertwarp --relout --rel --ref=${WD}/${T1wImageFile}.${FinalfMRIResolution} --warp1=${MotionMatrixFolder}/${MotionMatrixPrefix}${vnum}_gdc_warp.nii.gz --warp2=${OutputTransform} --out=${MotionMatrixFolder}/${MotionMatrixPrefix}${vnum}_all_warp.nii.gz
  fslmaths ${WD}/prevols/vol${vnum}.nii.gz -mul 0 -add 1 ${WD}/prevols/vol${vnum}_mask.nii.gz
  applywarp --rel --interp=spline --in=${WD}/prevols/vol${vnum}.nii.gz --warp=${MotionMatrixFolder}/${MotionMatrixPrefix}${vnum}_all_warp.nii.gz --ref=${WD}/${T1wImageFile}.${FinalfMRIResolution} --out=${WD}/postvols/vol${vnum}.nii.gz
  applywarp --rel --interp=nn --in=${WD}/prevols/vol${vnum}_mask.nii.gz --warp=${MotionMatrixFolder}/${MotionMatrixPrefix}${vnum}_all_warp.nii.gz --ref=${WD}/${T1wImageFile}.${FinalfMRIResolution} --out=${WD}/postvols/vol${vnum}_mask.nii.gz
  FrameMergeSTRING="${FrameMergeSTRING}${WD}/postvols/vol${vnum}.nii.gz " 
  FrameMergeSTRINGII="${FrameMergeSTRINGII}${WD}/postvols/vol${vnum}_mask.nii.gz "
done
# Merge together results and restore the TR (saved beforehand)
fslmerge -tr ${OutputfMRI} $FrameMergeSTRING $TR_vol
fslmerge -tr ${OutputfMRI}_mask $FrameMergeSTRINGII $TR_vol
fslmaths ${OutputfMRI}_mask -Tmin ${OutputfMRI}_mask

# Combine transformations: gradient non-linearity distortion + fMRI_dc to standard
convertwarp --relout --rel --ref=${WD}/${T1wImageFile}.${FinalfMRIResolution} --warp1=${GradientDistortionField} --warp2=${OutputTransform} --out=${WD}/Scout_gdc_MNI_warp.nii.gz
applywarp --rel --interp=spline --in=${ScoutInput} -w ${WD}/Scout_gdc_MNI_warp.nii.gz -r ${WD}/${T1wImageFile}.${FinalfMRIResolution} -o ${ScoutOutput}


### input ###
WD=/data3/cnl/xli/cpac_features/abcd/last_piece/cpac_mcref_head
InputfMRI=/data3/cnl/fmriprep/Lei_working/preprocessed_AllNew_New_2021/CPAC_ABCD_scratch_0225/sub-0025427/working/resting_preproc_sub-0025427a_ses-1/func_preproc_anatomical_refined_selected_volume_mcflirt_0/_scan_rest_run-1/func_reorient/sub-0025427a_task-rest_run-1_bold_calc_resample.nii.gz
OutputfMRIBasename=task-rest01
# 3dTcat -prefix ${Scout} ${InputfMRI}[0]
Scout=/data3/cnl/fmriprep/Lei_working/preprocessed_AllNew_New_2021/CPAC_ABCD_scratch_0225/sub-0025427/working/resting_preproc_sub-0025427a_ses-1/func_preproc_anatomical_refined_selected_volume_mcflirt_0/_scan_rest_run-1/func_reorient/sub-0025427a_task-rest_run-1_bold_calc_resample_first.nii.gz
# /data3/cnl/fmriprep/Lei_working/preprocessed_AllNew_New_2021/CPAC_ABCD_scratch_0225/sub-0025427/working/resting_preproc_sub-0025427a_ses-1/func_preproc_anatomical_refined_selected_volume_mcflirt_0/_scan_rest_run-1/get_func_volume/sub-0025427a_task-rest_run-1_bold_calc_resample_mcf_calc_calc.nii.gz

OutputfMRI=task-rest01_nonlin
GradientDistortionField=/data3/cnl/fmriprep/Lei_working/CPAC_XCP/ABCD/ABCD_Testing_With_Intermediate/sub-0025427/ses-1/files/task-rest01/task-rest01_gdc_warp.nii.gz # 3 empty volumes
MotionMatrixFolder=${WD}/task-rest01
MotionMatrixPrefix=MAT_

T1wImage=/data3/cnl/fmriprep/Lei_working/preprocessed_AllNew_New_2021/CPAC_ABCD_scratch_0225/sub-0025427/working/resting_preproc_sub-0025427a_ses-1/anat_preproc_freesurfer_abcd_0/acpc_align/anat_acpc_6_applywarp/sub-0025427a_run-1_T1w_resample_noise_corrected_corrected_warp.nii.gz
T1wImageFilefMRIResolution=/data3/cnl/fmriprep/Lei_working/preprocessed_AllNew_New_2021/CPAC_ABCD_scratch_0225/sub-0025427/working/resting_preproc_sub-0025427a_ses-1/resample_anatomical_brain_in_standard_0/sub-0025427a_run-1_T1w_resample_noise_corrected_corrected_warp_maths_restore_maths_warp_masked_warp.nii.gz
OutputTransform=task-rest012standard.nii.gz
fMRIToStructuralInputMat=/data3/cnl/fmriprep/Lei_working/preprocessed_AllNew_New_2021/CPAC_ABCD_scratch_0225/sub-0025427/working/resting_preproc_sub-0025427a_ses-1/func_to_anat_FLIRT_0/_scan_rest_run-1/linear_func_to_anat/sub-0025427a_task-rest_run-1_bold_calc_resample_mcf_calc_flirt.mat
StructuralToStandard=/data3/cnl/fmriprep/Lei_working/preprocessed_AllNew_New_2021/CPAC_ABCD_scratch_0225/sub-0025427/working/resting_preproc_sub-0025427a_ses-1/merge_xfms/e1_merged.nii.gz
BrainMask=/data3/cnl/fmriprep/Lei_working/preprocessed_AllNew_New_2021/CPAC_ABCD_scratch_0225/sub-0025427/output/pipeline_analysis/sub-0025427a_ses-1/functional_brain_mask_to_standard_abcd/wmparc_maths_fill_holes_maths_warp_warp_warp.nii.gz

# motion correction
/data3/cnl/freesurfer/DCAN-HCP/global/scripts/mcflirt.sh ${InputfMRI} ${OutputfMRIBasename} ${Scout}

TR_vol=`${FSLDIR}/bin/fslval ${InputfMRI} pixdim4 | cut -d " " -f 1` # TR
NumFrames=`${FSLDIR}/bin/fslval ${InputfMRI} dim4` # num of TR

# convert warp
convertwarp --relout --rel -m ${fMRIToStructuralInputMat} --ref=${T1wImage} --out=${WD}/fMRI2str.nii.gz
convertwarp --relout --rel --warp1=${WD}/fMRI2str.nii.gz --warp2=${StructuralToStandard} --ref=${T1wImageFilefMRIResolution} --out=${OutputTransform}

mkdir -p ${WD}/prevols
mkdir -p ${WD}/postvols

fslsplit ${InputfMRI} ${WD}/prevols/vol -t
FrameMergeSTRING=""
FrameMergeSTRINGII=""
# apply warp
for ((k=0; k < $NumFrames; k++)); do
  vnum=`zeropad $k 4`
  convertwarp --relout --rel --ref=${WD}/prevols/vol${vnum}.nii.gz --warp1=${GradientDistortionField} --postmat=${MotionMatrixFolder}/${MotionMatrixPrefix}${vnum}.mat --out=${MotionMatrixFolder}/${MotionMatrixPrefix}${vnum}_gdc_warp.nii.gz
  convertwarp --relout --rel --ref=${T1wImageFilefMRIResolution} --warp1=${MotionMatrixFolder}/${MotionMatrixPrefix}${vnum}_gdc_warp.nii.gz --warp2=${OutputTransform} --out=${MotionMatrixFolder}/${MotionMatrixPrefix}${vnum}_all_warp.nii.gz
  fslmaths ${WD}/prevols/vol${vnum}.nii.gz -mul 0 -add 1 ${WD}/prevols/vol${vnum}_mask.nii.gz
  applywarp --rel --interp=spline --in=${WD}/prevols/vol${vnum}.nii.gz --warp=${MotionMatrixFolder}/${MotionMatrixPrefix}${vnum}_all_warp.nii.gz --ref=${T1wImageFilefMRIResolution} --out=${WD}/postvols/vol${vnum}.nii.gz
  applywarp --rel --interp=nn --in=${WD}/prevols/vol${vnum}_mask.nii.gz --warp=${MotionMatrixFolder}/${MotionMatrixPrefix}${vnum}_all_warp.nii.gz --ref=${T1wImageFilefMRIResolution} --out=${WD}/postvols/vol${vnum}_mask.nii.gz
  FrameMergeSTRING="${FrameMergeSTRING}${WD}/postvols/vol${vnum}.nii.gz " 
  FrameMergeSTRINGII="${FrameMergeSTRINGII}${WD}/postvols/vol${vnum}_mask.nii.gz "
done

# Merge together results and restore the TR (saved beforehand)
fslmerge -tr ${OutputfMRI} $FrameMergeSTRING $TR_vol
fslmerge -tr ${OutputfMRI}_mask $FrameMergeSTRINGII $TR_vol

# intensity normalization
fslmaths ${OutputfMRI} -mas ${BrainMask} -mas ${OutputfMRI}_mask -thr 0 -ing 10000 task-rest01_nonlin_norm -odt float