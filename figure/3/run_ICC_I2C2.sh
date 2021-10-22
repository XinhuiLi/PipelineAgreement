## creat data for ICC and I2C2

python3.8 /data3/cnl/fmriprep/Lei_working/testing/ICC_Scan_duration/All_sessions/ICC_a.py

# ICC
datain='/data3/cnl/fmriprep/Lei_working/testing/ICC_Scan_duration/All_sessions/figures/Data_ICC_1000_All_pearson'

command='/data3/cnl/fmriprep/Lei_working/testing/ICC_Scan_duration/All_sessions/ICC_commands.txt'
rm $command

for i in $(ls $datain);do
    echo $i
    filein=$datain'/'$i
    echo Rscript /data3/cnl/fmriprep/Lei_working/testing/ICC_Scan_duration/All_sessions/Calculate_ICC.R $filein >> $command
done


# I2C2
datain='/data3/cnl/fmriprep/Lei_working/testing/ICC_Scan_duration/All_sessions/figures/Data_ICC_1000_All_pearson'

command='/data3/cnl/fmriprep/Lei_working/testing/ICC_Scan_duration/All_sessions/I2C2_commands.txt'
rm $command

for i in $(ls $datain);do
    echo $i
    filein=$datain'/'$i
    echo Rscript /data3/cnl/fmriprep/Lei_working/testing/ICC_Scan_duration/All_sessions/Calculate_I2C2.R $filein >> $command
done

cat /data3/cnl/fmriprep/Lei_working/testing/ICC_Scan_duration/All_sessions/ICC_commands.txt | parallel -j 55

cat /data3/cnl/fmriprep/Lei_working/testing/ICC_Scan_duration/All_sessions/I2C2_commands.txt | parallel -j 55
