# ABCD
for ((k=27;k<57;k++));do
    sub='sub-00254'$k'a'
    abcd_brain='${DATA_INPUT_DIR}/abcd_mask/abcd/'${sub}'_abcd_brain.nii.gz'
    abcd_head='${DATA_INPUT_DIR}/cpac_abcd/working/cpac_'${sub}'_ses-1/acpc_align_48/anat_acpc_6_applywarp/'${sub}'_run-1_T1w_resample_noise_corrected_corrected_warp.nii.gz'
    abcd_mask='${DATA_INPUT_DIR}/cpac_abcd/working/cpac_'${sub}'_ses-1/brain_mask_to_t1_restore_62/wmparc_maths_fill_holes_maths_warp.nii.gz'
    # to get abcd brain
    fslmaths ${abcd_head} -mul ${abcd_mask} ${abcd_brain}
done

for pipeline in 'ccs' 'fmriprep';do
    wd='${DATA_INPUT_DIR}/abcd_mask/'${pipeline}
    for ((k=27;k<57;k++));do
        sub='sub-00254'$k'a'
        echo $pipeline
        echo $sub

        abcd_brain='${DATA_INPUT_DIR}/abcd_mask/abcd/'${sub}'_abcd_brain.nii.gz'
        abcd_head='${DATA_INPUT_DIR}/cpac_abcd/working/cpac_'${sub}'_ses-1/acpc_align_48/anat_acpc_6_applywarp/'${sub}'_run-1_T1w_resample_noise_corrected_corrected_warp.nii.gz'

        pipeline_brain='${DATA_INPUT_DIR}/cpac_'${pipeline}'/output/cpac_cpac_'${pipeline}'-options/'${sub}'_ses-1/anat/'${sub}'_ses-1_desc-brain_T1w.nii.gz'
        pipeline_head='${DATA_INPUT_DIR}/cpac_'${pipeline}'/output/cpac_cpac_'${pipeline}'-options/'${sub}'_ses-1/anat/'${sub}'_ses-1_desc-preproc_T1w.nii.gz'
        pipeline_mask='${DATA_INPUT_DIR}/cpac_'${pipeline}'/output/cpac_cpac_'${pipeline}'-options/'${sub}'_ses-1/anat/'${sub}'_ses-1_space-T1w_desc-brain_mask.nii.gz'
        pipeline_mask_out='${DATA_INPUT_DIR}/abcd_mask/'${pipeline}'/'${sub}'/'${sub}'_ses-1_space-T1w_desc-brain_mask.nii.gz'

        cd ${wd}
        mkdir ${sub}
        cd ${sub}
        flirt -ref ${abcd_brain} -in ${pipeline_brain} -omat affine.mat
        fnirt --in=${pipeline_head} --ref=${abcd_head} --aff=affine.mat --cout=nonlinear_xfm
        applywarp --ref=${abcd_head} --in=${pipeline_mask} --warp=nonlinear_xfm --out=${pipeline_mask_out} --interp=nn
    done
done

pipeline='default'
wd='${DATA_INPUT_DIR}/abcd_mask/'${pipeline}
for ((k=27;k<57;k++));do
    sub='sub-00254'$k'a'
    echo $pipeline
    echo $sub

    abcd_brain='${DATA_INPUT_DIR}/abcd_mask/abcd/'${sub}'_abcd_brain.nii.gz'
    abcd_head='${DATA_INPUT_DIR}/cpac_abcd/working/cpac_'${sub}'_ses-1/acpc_align_48/anat_acpc_6_applywarp/'${sub}'_run-1_T1w_resample_noise_corrected_corrected_warp.nii.gz'

    pipeline_brain='${DATA_INPUT_DIR}/cpac_'${pipeline}'/output/cpac_cpac-'${pipeline}'-pipeline/'${sub}'_ses-1/anat/'${sub}'_ses-1_desc-brain_T1w.nii.gz'
    pipeline_head='${DATA_INPUT_DIR}/cpac_'${pipeline}'/output/cpac_cpac-'${pipeline}'-pipeline/'${sub}'_ses-1/anat/'${sub}'_ses-1_desc-preproc_T1w.nii.gz'
    pipeline_mask='${DATA_INPUT_DIR}/cpac_'${pipeline}'/output/cpac_cpac-'${pipeline}'-pipeline/'${sub}'_ses-1/anat/'${sub}'_ses-1_space-T1w_desc-brain_mask.nii.gz'
    pipeline_mask_out='${DATA_INPUT_DIR}/abcd_mask/'${pipeline}'/'${sub}'/'${sub}'_ses-1_space-T1w_desc-brain_mask.nii.gz'

    cd ${wd}
    mkdir ${sub}
    cd ${sub}
    flirt -ref ${abcd_brain} -in ${pipeline_brain} -omat affine.mat
    fnirt --in=${pipeline_head} --ref=${abcd_head} --aff=affine.mat --cout=nonlinear_xfm
    applywarp --ref=${abcd_head} --in=${pipeline_mask} --warp=nonlinear_xfm --out=${pipeline_mask_out} --interp=nn
done

# ccs_brain='${DATA_INPUT_DIR}/cpac_ccs/working/cpac_sub-0025427a_ses-1/anat_preproc_freesurfer_43/anat_freesurfer/recon_all/mri/brainmask.nii.gz'
# ccs_head='${DATA_INPUT_DIR}/cpac_ccs/working/cpac_sub-0025427a_ses-1/anat_preproc_freesurfer_43/anat_freesurfer/recon_all/mri/T1.nii.gz'
# ccs_mask='${DATA_INPUT_DIR}/abcd_mask/ccs_mask.nii.gz'
# ccs_mask_filled='${DATA_INPUT_DIR}/abcd_mask/ccs_mask_filled.nii.gz'
# ccs_mask_out='${DATA_INPUT_DIR}/abcd_mask/ccs_mask_abcd.nii.gz'

# # to get ccs brain mask
# fslmaths ${ccs_brain} -bin ${ccs_mask}
# 3dmask_tool -input ${ccs_mask} -prefix ${ccs_mask_filled} -fill_holes

# flirt -ref ${abcd_brain} -in ${ccs_brain} -omat affine.mat
# fnirt --in=${ccs_head} --ref=${abcd_head} --aff=affine.mat --cout=nonlinear_xfm
# applywarp --ref=${abcd_head} --in=${ccs_mask_filled} --warp=nonlinear_xfm --out=${ccs_mask_out} --interp=nn
# # looks good!