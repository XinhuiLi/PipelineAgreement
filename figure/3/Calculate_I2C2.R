
library(data.table)
source('/data3/cnl/fmriprep/Lei_working/testing/ICC_Scan_duration/All_sessions/trance_only_unba.R')

args = commandArgs(trailingOnly=TRUE)


filein=args[1]
data_I2C2=t(fread(filein))
# data here is 
# sub1-pipeline1
# sub1-pipeline2
# sub2-pipeline1
# sub2-pipeline2

subn=dim(data_I2C2)[1]/2
data_I2C2=t(na.omit(t(data_I2C2)))
#I2C2_visit=c(rep(1,subn),rep(2,subn))
#I2C2_id=c(1:subn,1:subn)
I2C2_visit=c(rep(c(1,2),subn))
I2C2_id=sort(c(1:subn,1:subn))
i2c2_num=I2C2(data_I2C2,I = subn,J = 2,visit = I2C2_visit, id =I2C2_id,demean = TRUE)



write.table(i2c2_num$lambda, sub("Data_ICC","I2C2",filein), append = FALSE, sep = ",",row.names = FALSE, col.names = FALSE)
