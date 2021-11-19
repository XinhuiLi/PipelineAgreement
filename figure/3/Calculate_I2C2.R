
library(data.table)
source('trance_only_unba.R')

args = commandArgs(trailingOnly=TRUE)

filein=args[1]
data_I2C2=t(fread(filein))

subn=dim(data_I2C2)[1]/2
data_I2C2=t(na.omit(t(data_I2C2)))

I2C2_visit=c(rep(c(1,2),subn))
I2C2_id=sort(c(1:subn,1:subn))
i2c2_num=I2C2(data_I2C2,I = subn,J = 2,visit = I2C2_visit, id =I2C2_id,demean = TRUE)

write.table(i2c2_num$lambda, sub("Data_ICC","I2C2",filein), append = FALSE, sep = ",",row.names = FALSE, col.names = FALSE)