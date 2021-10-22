cpac_dir=/data3/cnl/xli/reproducibility/out/cpac_fmriprep_v2
fmriprep_dir=/data3/cnl/fmriprep/Lei_working/FINAL_preprocessed_2021/fmriprep_default

for ((k=27;k<57;k++)); do
    # anat mask
    anat_mask_lpi=${fmriprep_dir}/output/fmriprep/sub-00254${k}a/anat/sub-00254${k}a_run-1_desc-brain_mask.nii.gz
    anat_mask_rpi=${fmriprep_dir}/output/fmriprep/sub-00254${k}a/anat/sub-00254${k}a_run-1_desc-brain_mask_rpi.nii.gz
    3dresample -orient rpi -input ${anat_mask_lpi} -prefix ${anat_mask_rpi}

    # segmentation
    seg_lpi=${fmriprep_dir}/working/fmriprep_wf/single_subject_00254${k}a_wf/anat_preproc_wf/t1w_dseg/sub-00254${k}a_run-1_T1w_ras_valid_corrected_xform_masked_pveseg.nii.gz
    seg_rpi=${fmriprep_dir}/working/fmriprep_wf/single_subject_00254${k}a_wf/anat_preproc_wf/t1w_dseg/sub-00254${k}a_run-1_T1w_ras_valid_corrected_xform_masked_pveseg_rpi.nii.gz
    3dresample -orient rpi -input ${seg_lpi} -prefix ${seg_rpi}
    gm=${fmriprep_dir}/working/fmriprep_wf/single_subject_00254${k}a_wf/anat_preproc_wf/t1w_dseg/sub-00254${k}a_run-1_T1w_ras_valid_corrected_xform_masked_pveseg_rpi_gm.nii.gz
    wm=${fmriprep_dir}/working/fmriprep_wf/single_subject_00254${k}a_wf/anat_preproc_wf/t1w_dseg/sub-00254${k}a_run-1_T1w_ras_valid_corrected_xform_masked_pveseg_rpi_wm.nii.gz
    csf=${fmriprep_dir}/working/fmriprep_wf/single_subject_00254${k}a_wf/anat_preproc_wf/t1w_dseg/sub-00254${k}a_run-1_T1w_ras_valid_corrected_xform_masked_pveseg_rpi_csf.nii.gz

    fslmaths ${seg_rpi} -uthr 1.5 -thr 0.5 -bin ${csf}
    fslmaths ${seg_rpi} -uthr 2.5 -thr 1.5 -bin ${gm}
    fslmaths ${seg_rpi} -uthr 3.5 -thr 2.5 -bin ${wm}

    seg_rpi=${cpac_dir}/working/cpac_sub-00254${k}a_ses-1/segment_62/segment_pveseg.nii.gz
    gm=${cpac_dir}/working/cpac_sub-00254${k}a_ses-1/segment_62/segment_pveseg_gm.nii.gz
    wm=${cpac_dir}/working/cpac_sub-00254${k}a_ses-1/segment_62/segment_pveseg_wm.nii.gz
    csf=${cpac_dir}/working/cpac_sub-00254${k}a_ses-1/segment_62/segment_pveseg_csf.nii.gz

    fslmaths ${seg_rpi} -uthr 1.5 -thr 0.5 -bin ${csf}
    fslmaths ${seg_rpi} -uthr 2.5 -thr 1.5 -bin ${gm}
    fslmaths ${seg_rpi} -uthr 3.5 -thr 2.5 -bin ${wm}

    # anat mni
    # resample fMRIPrep brain
    3dresample -master ${cpac_dir}/output/cpac_cpac_fmriprep-options/sub-00254${k}a_ses-1/anat/sub-00254${k}a_ses-1_space-template_desc-brain_T1w.nii.gz \
    -prefix ${fmriprep_dir}/output/fmriprep/sub-00254${k}a/anat/sub-00254${k}a_run-1_space-MNI152NLin2009cAsym_desc-cpacbrain_T1w.nii.gz \
    -inset ${fmriprep_dir}/output/fmriprep/sub-00254${k}a/anat/sub-00254${k}a_run-1_space-MNI152NLin2009cAsym_desc-brain_T1w.nii.gz -rmode Cu
done