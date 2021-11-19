from_fmriprep_to_ccs=${PH_SERVER_DATA_ROOT}/analysis/data/from_fmriprep_to_ccs/anat_reg
output_path=${PH_SERVER_DATA_ROOT}/analysis/data/from_fmriprep_to_ccs/anat_reg_rpi
roi_path=${PH_SERVER_DATA_ROOT}/analysis/ROI200/from_fmriprep_to_ccs/anat_reg_rpi
mni2009=${PH_SERVER_WORKING_ROOT}/Finalizing/Schaefer_Atlas/Schaefer2018_200Parcels_7Networks_order_FSLMNI152_2mm_NLin2009cAsym.nii.gz
mni2009rpi=${PH_SERVER_WORKING_ROOT}/Finalizing/Schaefer_Atlas/Schaefer2018_200Parcels_7Networks_order_FSLMNI152_2mm_NLin2009cAsym_rpi.nii.gz

for ((k=27;k<57;k++));do
    sub='sub-00254'$k'a'
    echo $sub
    i=$from_fmriprep_to_ccs'/'$sub'.nii.gz'
    o=$from_fmriprep_to_ccs'/'$sub'_rpi.nii.gz'
    # 3dresample -orient rpi -prefix $o -inset $i
    # ln -s $o $output_path'/'$sub'.nii.gz'
    # rm $o

    3dROIstats -quiet -mask $mni2009rpi -1Dformat $output_path'/'$sub'.nii.gz' >> $roi_path'/'$sub'.1D'
done