datain='/data3/cnl/xli/reproducibility/out/gsr'
dataout='/data3/cnl/fmriprep/Lei_working/Finalizing/All_sessions_new/data'
for run in 'cpac_default_all' 'cpac_abcd_all' 'cpac_fmriprep_all' 'cpac_ccs_all';do
    rm -rf $dataout'/'$run'_gsr'
    mkdir -p $dataout'/'$run'_gsr'
    for ((k=27;k<57;k++));do
        for ses in 'a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j';do
            sub='sub-00254'${k}${ses}
            i=$datain'/'$run'/'$sub'/func_gsr.nii.gz'
            ln -s $i $dataout'/'$run'_gsr/'$sub'.nii.gz'
        done
    done
done

datain='/data3/cnl/xli/reproducibility/out'
dataout='/data3/cnl/fmriprep/Lei_working/Finalizing/All_sessions_new/data'
for run in 'cpac_ccs_all';do
    rm -rf $dataout'/'$run
    mkdir -p $dataout'/'$run
    for ((k=27;k<57;k++));do
        sub='sub-00254'${k}
        j=0
        for ses in 'a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j';do
            j=$((j+1))
            i=$datain'/'$run'/output/cpac_*/'$sub'a_ses-1/func/'$sub'a_ses-1_task-rest_run-'$j'_space-template_desc-brain_bold.nii.gz'
            ln -s $i $dataout'/'$run'/'$sub$ses'.nii.gz'
        done
    done
done

datain='/data3/cnl/xli/reproducibility/out'
dataout='/data3/cnl/fmriprep/Lei_working/Finalizing/All_sessions_new/data'
for run in 'cpac_default_all';do
    rm -rf $dataout'/'$run
    mkdir -p $dataout'/'$run
    for ((k=27;k<57;k++));do
        for ses in 'a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j';do
            sub='sub-00254'${k}${ses}
            i=$datain'/'$run'/output/cpac_*/'$sub'_ses-1/func/'$sub'_ses-1_task-rest_space-template_desc-brain_bold.nii.gz'
            ln -s $i $dataout'/'$run'/'$sub'.nii.gz'
        done
    done
done

datain='/data3/cnl/xli/reproducibility/out'
dataout='/data3/cnl/fmriprep/Lei_working/Finalizing/All_sessions_new/data'
for run in 'cpac_abcd_all' 'cpac_fmriprep_all';do
    rm -rf $dataout'/'$run
    mkdir -p $dataout'/'$run
    for ((k=27;k<57;k++));do
        for ses in 'a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j';do
            sub='sub-00254'${k}${ses}
            i=$datain'/'$run'/output/cpac_*/'$sub'_ses-1/func/'$sub'_ses-1_task-rest_space-template_desc-brain_bold.nii.gz'
            ln -s $i $dataout'/'$run'/'$sub'.nii.gz'
        done
    done
done

############## extract ROIs
datain='/data3/cnl/fmriprep/Lei_working/Finalizing/All_sessions_new/data'

commandlist='/data3/cnl/fmriprep/Lei_working/Finalizing/All_sessions_new/Shaefer_ROI_commands.txt'   
rm $commandlist

for num_rois in 200;do
    echo $num_rois
    mni2004_2mm='/data3/cnl/fmriprep/Lei_working/Finalizing/Schaefer_Atlas/Schaefer2018_'$num_rois'Parcels_7Networks_order_FSLMNI152_2mm.nii.gz'
    mni2004_3mm='/data3/cnl/fmriprep/Lei_working/Finalizing/Schaefer_Atlas/Schaefer2018_'$num_rois'Parcels_7Networks_order_FSLMNI152_3mm.nii.gz'
    mni2009='/data3/cnl/fmriprep/Lei_working/Finalizing/Schaefer_Atlas/Schaefer2018_'$num_rois'Parcels_7Networks_order_FSLMNI152_2mm_NLin2009cAsym.nii.gz'

    dataout='/data3/cnl/fmriprep/Lei_working/Finalizing/All_sessions_new/ROI/ROI_Schaefer'$num_rois
    mkdir -p $dataout

    for run in 'cpac_default_all_gsr' 'cpac_abcd_all_gsr' 'cpac_fmriprep_all_gsr' 'cpac_ccs_all_gsr'; do
        if [[ $run == 'cpac_fmriprep_all' ]];then mask=$mni2009;fi
        if [[ $run == 'cpac_abcd_all' ]];then mask=$mni2004_2mm;fi
        if [[ $run == 'cpac_ccs_all' ]];then mask=$mni2004_3mm;fi
        if [[ $run == 'cpac_default_all' ]];then mask=$mni2004_3mm;fi

        if [[ $run == 'cpac_fmriprep_all_gsr' ]];then mask=$mni2009;fi
        if [[ $run == 'cpac_abcd_all_gsr' ]];then mask=$mni2004_2mm;fi
        if [[ $run == 'cpac_ccs_all_gsr' ]];then mask=$mni2004_3mm;fi
        if [[ $run == 'cpac_default_all_gsr' ]];then mask=$mni2004_3mm;fi

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

cat $commandlist | parallel -j 20