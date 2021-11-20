# Please define the environment variable WORKING_DIR 
# in .pipelineharmonizationrc or in this script

## create data for ICC and I2C2
python3.8 $WORKING_DIR/run_ICC.py

# ICC
datain=$WORKING_DIR'/figures/Data_ICC_1000_All_pearson'
command=$WORKING_DIR'/ICC_commands.txt'
rm $command

for i in $(ls $datain);do
    echo $i
    filein=$datain'/'$i
    echo Rscript $WORKING_DIR/Calculate_ICC.R $filein >> $command
done

# I2C2
datain=$WORKING_DIR'/figures/Data_ICC_1000_All_pearson'
command=$WORKING_DIR'/I2C2_commands.txt'
rm $command

for i in $(ls $datain);do
    echo $i
    filein=$datain'/'$i
    echo Rscript $WORKING_DIR/Calculate_I2C2.R $filein >> $command
done

cat $WORKING_DIR/ICC_commands.txt | parallel -j 55
cat $WORKING_DIR/I2C2_commands.txt | parallel -j 55