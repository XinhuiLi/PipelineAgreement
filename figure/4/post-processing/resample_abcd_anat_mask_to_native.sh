abcd_dir=/data3/cnl/xli/reproducibility/out/cpac_abcd

# sub-0025448a anat mask: /data3/cnl/fmriprep/Lei_working/CPAC_XCP/ABCD/preprocessed/data/sub-0025448/ses-1/files/MNINonLinear/brainmask_fs.nii.gz
# flirt -in /data3/cnl/fmriprep/Lei_working/CPAC_XCP/ABCD/preprocessed/data/sub-0025448/ses-1/files/MNINonLinear/brainmask_fs.nii.gz -ref /data3/cnl/xli/reproducibility/out/cpac_abcd/output/cpac_cpac_abcd-options/sub-0025448a_ses-1/anat/sub-0025448a_ses-1_desc-n4_T1w.nii.gz -out /data3/cnl/xli/reproducibility/out/cpac_abcd_native_anat_mask/sub-0025448a_mask.nii.gz -interp nearestneighbour

for ((k=27;k<57;k++));do
    sub='sub-00254'$k'a'
    echo $sub
    r=$abcd_dir'/output/cpac_cpac_abcd-options/'$sub'_ses-1/anat/'$sub'_ses-1_desc-n4_T1w.nii.gz'
    i=$abcd_dir'/working/cpac_'$sub'_ses-1/FSL-ABCD_T1_brain_mask_to_template_81/wmparc_maths_fill_holes_maths_warp_warp.nii.gz'
    o='/data3/cnl/xli/reproducibility/out/cpac_abcd_native_anat_mask/'$sub'_mask.nii.gz'
    flirt -in $i -ref $r -out $o -interp nearestneighbour
done

for ((k=27;k<57;k++));do
    sub='sub-00254'$k'a'
    echo $sub
    out='/data3/cnl/xli/reproducibility/out/cpac_abcd_native_anat_mask/'$sub'_mask.nii.gz'
    bidsout='/data3/cnl/xli/reproducibility/out/cpac_abcd_native_anat_mask/'$sub'_run-1_T1w_mask.nii.gz'
    cp $out $bidsout
done