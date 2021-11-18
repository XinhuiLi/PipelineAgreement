# Please define the environment variables DATA_INPUT_DIR, DATA_OUTPUT_DIR, WORKING_DIR
# in .pipelineharmonizationrc or in this script

datain=$DATA_INPUT_DIR
dataout=$DATA_OUTPUT_DIR

### C-PAC ABCD BBR ###
for run in 'cpac_abcd_bbr';do
    rm -rf $dataout'/cpac_abcd_bbr'
    mkdir -p $dataout'/cpac_abcd_bbr'
    for ((k=27;k<57;k++));do
        sub='sub-00254'${k}'a'
        i=$datain'/'$run'/output/cpac_*/'$sub'_ses-1/func/'$sub'_ses-1_task-rest_run-1_space-template_desc-brain-1_bold.nii.gz'
        ln -s $i $dataout'/cpac_abcd_bbr/'$sub'.nii.gz'
    done
done

### C-PAC Default v1.8 ###
for run in 'cpac_default_all';do
    rm -rf $dataout'/cpac_default_v1.8'
    mkdir -p $dataout'/cpac_default_v1.8'
    for ((k=27;k<57;k++));do
        sub='sub-00254'${k}'a'
        i=$datain'/'$run'/output/cpac_*/'$sub'_ses-1/func/'$sub'_ses-1_task-rest_space-template_desc-brain_bold.nii.gz'
        ln -s $i $dataout'/cpac_default_v1.8/'$sub'.nii.gz'
    done
done

### C-PAC fMRIPrep/CCS/ABCD-options: MNI2006 + 2mm func write-out ###
for run in 'cpac_fmriprep_mni2006_2mm' 'cpac_fmriprep' 'cpac_ccs' 'cpac_abcd';do
    rm -rf $dataout'/'$run'_v1.8'
    mkdir -p $dataout'/'$run'_v1.8'
    for ((k=27;k<57;k++));do
        sub='sub-00254'$k'a'
        i=$datain'/'$run'/output/cpac_*/'$sub'_ses-1/func/'$sub'_ses-1_task-rest_run-1_space-template_desc-brain_bold.nii.gz'
        ln -s $i $dataout'/'$run'_v1.8/'$sub'.nii.gz'
    done
done

### fMRIPrep LTS default: MNI2009 + native func write-out ###
for run in fmriprep_default;do
    mkdir -p $dataout'/'$run
    for sub in $(ls $datain'/'$run'/output/fmriprep');do
        if [[ $sub == *"html"* ]];then continue;fi
        if [[ ${sub: -1} == *"b"* ]];then continue;fi
        sub_new=${sub/_ses-1/}

        if [[ -f $datain'/'$run'/output/fmriprep/'$sub ]];then continue;fi
        if [[ $sub == "logs" ]];then continue;fi
        i=$datain'/'$run'/output/fmriprep/'$sub'/func/'$sub'_task-rest_run-1_space-MNI152NLin2009cAsym_desc-brain_bold.nii.gz'
        ln -s $i $dataout'/'$run'/'$sub_new'.nii.gz'
    done
done

### CCS ###
for run in ccs;do
    mkdir -p $dataout'/'$run'_rerun'
    for ((k=27;k<57;k++));do
        sub='sub-00254'$k
        i=$datain'/'$run'/'$sub'/func/rest_gms_mni152.nii.gz'
        ln -s $i $dataout'/'$run'_rerun/'$sub'a.nii.gz'
    done
done

##########
datain=$DATA_OUTPUT_DIR
commandlist=$DATA_OUTPUT_DIR'/Schaefer_ROI_commands.txt'   
rm $commandlist

for num_rois in 200 600 1000;do
    echo $num_rois
    mni2004_2mm=$WORKING_DIR'/Schaefer_Atlas/Schaefer2018_'$num_rois'Parcels_7Networks_order_FSLMNI152_2mm.nii.gz'
    mni2004_3mm=$WORKING_DIR'/Schaefer_Atlas/Schaefer2018_'$num_rois'Parcels_7Networks_order_FSLMNI152_3mm.nii.gz'
    mni2009=$WORKING_DIR'/Schaefer_Atlas/Schaefer2018_'$num_rois'Parcels_7Networks_order_FSLMNI152_2mm_NLin2009cAsym.nii.gz'

    dataout=$WORKING_DIR'/ROI/ROI_Schaefer'$num_rois
    mkdir -p $dataout

    for run in 'cpac_fmriprep_v1.8' 'cpac_ccs_v1.8' 'cpac_abcd_v1.8';do
        if [[ $run == 'ABCD' ]];then mask=$mni2004_2mm;fi
        if [[ $run == 'ccs' ]];then mask=$mni2004_3mm;fi
        if [[ $run == 'fmriprep_default' ]];then mask=$mni2009;fi
        if [[ $run == 'dpabi' ]];then mask=$mni2004_3mm;fi

        if [[ $run == 'cpac_abcd_v1.8' ]];then mask=$mni2004_2mm;fi
        if [[ $run == 'cpac_ccs_v1.8' ]];then mask=$mni2004_3mm;fi
        if [[ $run == 'cpac_fmriprep_v1.8' ]];then mask=$mni2009;fi

        mkdir -p $dataout'/'$run
        for i in $(ls $datain'/'$run);do
            if [[ $i == *"csv"* ]];then continue;fi
            if [[ $i == *"b_"* ]];then continue;fi
            if [[ $i == *"dmt"* ]];then continue;fi
            infile=$datain'/'$run'/'$i
            if [[ -f $infile ]];then
                echo $infile
                infile_base=$(basename $infile)
                outfile=$dataout'/'$run'/'${infile_base/.nii.gz/.1D}
                if [[ ! -f $outfile ]];then
                   echo "3dROIstats -quiet -mask $mask -1Dformat $infile >> $outfile" >> $commandlist
                fi
            fi
        done
    done
done

cat $commandlist | parallel -j 30