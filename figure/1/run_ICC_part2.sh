###################
# after create ICC number, need to combine them together.

for atlas in 200 600 1000;do
	if [[ $atlas == 200 ]];then
	    nn=2
	    laststart=10001
	    lastend=19900
	fi
	if [[ $atlas == 600 ]];then
	    nn=18
	    laststart=170001
	    lastend=179700
	fi
	if [[ $atlas == 1000 ]]; then
	    nn=50
	    laststart=490001
	    lastend=499500
	fi

    echo $atlas
    datain='/data3/cnl/fmriprep/Lei_working/Finalizing/Minimal/figures/All_new_ICC_Schaefer'$atlas
    dataout='/data3/cnl/fmriprep/Lei_working/Finalizing/Minimal/figures/All_new_ICC_Schaefer'$atlas'_aggreg'
    mkdir -p $dataout
    for run in $(find $datain -iname '*_ICC_1.csv*');do
        run_short=$(basename $run)
        a1_a2=${run_short/_ICC_1.csv/}
        fileout=$dataout'/'$a1_a2'_ICC.csv'
        rm $fileout
        echo $a1_a2
        for runnum in $(seq 1 $nn);do
            file=$datain'/'$a1_a2'_ICC_'$runnum'.csv'
            if [[ ! -f $file ]];then
                echo $file
            else
                cat $file >> $fileout
            fi
        done
    done
done


