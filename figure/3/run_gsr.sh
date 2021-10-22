# default output
input=/data3/cnl/xli/reproducibility/out/cpac_default_all/output/cpac_cpac-default-pipeline
output=/data3/cnl/xli/reproducibility/out/gsr/cpac_default_all
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
input=/data3/cnl/xli/reproducibility/out/cpac_fmriprep_all_v2/output/cpac_cpac_fmriprep-options
output=/data3/cnl/xli/reproducibility/out/gsr/cpac_fmriprep_all
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
input=/data3/cnl/xli/reproducibility/out/cpac_abcd_all/output/cpac_cpac_abcd-options
output=/data3/cnl/xli/reproducibility/out/gsr/cpac_abcd_all
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

# For ABCD sub-0025448a
# 3dTcat -prefix scout.nii.gz /data3/cnl/fmriprep/Lei_working/CPAC_XCP/ABCD/preprocessed/data/sub-0025448/ses-1/files/MNINonLinear/Results/task-rest01/task-rest01.nii.gz[0]
# fslmaths scout.nii.gz -bin mask_orig.nii.gz
# 3dmask_tool -prefix mask_filled.nii.gz -input mask_orig.nii.gz -fill_holes
# 3dROIstats -1Dformat -mask mask_filled.nii.gz /data3/cnl/fmriprep/Lei_working/CPAC_XCP/ABCD/preprocessed/data/sub-0025448/ses-1/files/MNINonLinear/Results/task-rest01/task-rest01.nii.gz > gs.1D
# 3dTproject -input /data3/cnl/fmriprep/Lei_working/CPAC_XCP/ABCD/preprocessed/data/sub-0025448/ses-1/files/MNINonLinear/Results/task-rest01/task-rest01.nii.gz -mask mask_filled.nii.gz -ort gs.1D -polort 2 -prefix func_gsr.nii.gz

# CCS-options output
input=/data3/cnl/xli/reproducibility/out/cpac_ccs_all/output/cpac_cpac_ccs-options
output=/data3/cnl/xli/reproducibility/out/gsr/cpac_ccs_all
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