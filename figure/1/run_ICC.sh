# Please define the environment variable WORKING_DIR 
# in .pipelineharmonizationrc or in this script

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

	tmp=$WORKING_DIR'/ICC_1000_run/Reliability_general_minimal_no_parallel_tmp_'$atlas'.R'

	outfolder=$WORKING_DIR'/ICC_1000_run/fig1_running_scripts_'$atlas

	mkdir $outfolder

	declare -a runs=('cpac_default_v1.8' 'fmriprep_default' 'ABCD' 'ccs' 'dpabi')

	for i in $(seq 0 4);do
	    for j in $(seq $((i+1)) 4);do
		echo ${runs[i]} ${runs[j]}
		for runnum in $(seq 1 $nn);do
		    start_num=$(($((runnum-1))*10000+1))
		    end_num=$(($runnum*10000))
                    if [[ $runnum == $nn ]];then start_num=$laststart; end_num=$lastend; fi
		    outfile=$outfolder'/'${runs[i]}'_'${runs[j]}'_'$runnum'.R'
		    cp $tmp $outfile
		    sed -i 's/AAAA/'${runs[i]}'/g' $outfile
		    sed -i 's/BBBB/'${runs[j]}'/g' $outfile
		    sed -i 's/POSTFIX/'$runnum'/g' $outfile
		    sed -i 's/8888/'$start_num'/g' $outfile
		    sed -i 's/9999/'$end_num'/g' $outfile
		done
	    done
	done

	running=$WORKING_DIR'/ICC_1000_run/running_commands_'$atlas'_fig1.txt'

	rm $running
	for i in $(ls $outfolder);do
	    echo Rscript $outfolder'/'$i >> $running
	done
done

### parallel run
cat $WORKING_DIR/ICC_1000_run/running_commands_200_fig1.txt | parallel -j 20
cat $WORKING_DIR/ICC_1000_run/running_commands_600_fig1.txt | parallel -j 20
cat $WORKING_DIR/ICC_1000_run/running_commands_1000_fig1.txt | parallel -j 20

### combine ICC number together
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
    datain=$WORKING_DIR'/figures/All_new_ICC_Schaefer'$atlas
    dataout=$WORKING_DIR'/figures/All_new_ICC_Schaefer'$atlas'_aggreg'
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