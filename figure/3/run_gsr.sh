# default output
input=${DATA_INPUT_DIR}/cpac_default_all/output/cpac_cpac-default-pipeline
output=${DATA_INPUT_DIR}/gsr/cpac_default_all
for ((k=27;k<57;k++));do
    for ses in 'a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j';do
        sub='sub-00254'${k}${ses}
        cd ${output}
        mkdir ${sub}
        cd ${sub}
        func=$input'/'$sub'_ses-1/func/'$sub'_ses-1_task-rest_space-template_desc-brain_bold.nii.gz'
        mask=$input'/'$sub'_ses-1/func/'$sub'_ses-1_task-rest_space-template_desc-bold_mask.nii.gz'
        3dROIstats -1Dformat -mask ${mask} ${func} > gs.1D
        3dTproject -input ${func} -mask ${mask} -ort gs.1D -polort 2 -prefix func_gsr.nii.gz
    done
done

# fMRIPrep-options output
input=${DATA_INPUT_DIR}/cpac_fmriprep_all_v2/output/cpac_cpac_fmriprep-options
output=${DATA_INPUT_DIR}/gsr/cpac_fmriprep_all
for ((k=27;k<57;k++));do
    for ses in 'a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j';do
        sub='sub-00254'${k}${ses}
        cd ${output}
        mkdir ${sub}
        cd ${sub}
        func=$input'/'$sub'_ses-1/func/'$sub'_ses-1_task-rest_space-template_desc-brain_bold.nii.gz'
        # generate func mask in template space
        mask_orig='mask_orig.nii.gz'
        mask='mask_filled.nii.gz'
        scout='scout.nii.gz'
        3dTcat -prefix ${scout} ${func}[0]
        fslmaths ${scout} -bin ${mask_orig}
        3dmask_tool -prefix ${mask} -input ${mask_orig} -fill_holes
        # run GSR
        3dROIstats -1Dformat -mask ${mask} ${func} > gs.1D
        3dTproject -input ${func} -mask ${mask} -ort gs.1D -polort 2 -prefix func_gsr.nii.gz
    done
done

# ABCD-options output
input=${DATA_INPUT_DIR}/cpac_abcd_all/output/cpac_cpac_abcd-options
output=${DATA_INPUT_DIR}/gsr/cpac_abcd_all
for ((k=27;k<57;k++));do
    for ses in 'a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j';do
        sub='sub-00254'${k}${ses}
        cd ${output}
        mkdir ${sub}
        cd ${sub}
        func=$input'/'$sub'_ses-1/func/'$sub'_ses-1_task-rest_space-template_desc-brain_bold.nii.gz'
        # generate func mask in template space
        mask_orig='mask_orig.nii.gz'
        mask='mask_filled.nii.gz'
        scout='scout.nii.gz'
        3dTcat -prefix ${scout} ${func}[0]
        fslmaths ${scout} -bin ${mask_orig}
        3dmask_tool -prefix ${mask} -input ${mask_orig} -fill_holes
        # run GSR
        3dROIstats -1Dformat -mask ${mask} ${func} > gs.1D
        3dTproject -input ${func} -mask ${mask} -ort gs.1D -polort 2 -prefix func_gsr.nii.gz
    done
done

# CCS-options output
input=${DATA_INPUT_DIR}/cpac_ccs_all/output/cpac_cpac_ccs-options
output=${DATA_INPUT_DIR}/gsr/cpac_ccs_all
for ((k=27;k<57;k++));do
    sub='sub-00254'${k}
    j=0
    for ses in 'a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j';do
        j=$((j+1))
        cd ${output}
        mkdir ${sub}${ses}
        cd ${sub}${ses}
        func=$input'/'$sub'a_ses-1/func/'$sub'a_ses-1_task-rest_run-'$j'_space-template_desc-brain_bold.nii.gz'
        mask=$input'/'$sub'a_ses-1/func/'$sub'a_ses-1_task-rest_run-'$j'_space-template_desc-bold_mask.nii.gz'
        3dROIstats -1Dformat -mask ${mask} ${func} > gs.1D
        3dTproject -input ${func} -mask ${mask} -ort gs.1D -polort 2 -prefix func_gsr.nii.gz
    done
done