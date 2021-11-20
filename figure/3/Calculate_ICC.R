library(ICC)
library(gplots)
library(gridGraphics)
library(grid)
#library(lme4)
library('lme4',lib.loc='/home/lai/R/x86_64-pc-linux-gnu-library/3.2')
library(R.matlab)
library(data.table)

args = commandArgs(trailingOnly=TRUE)

filein=args[1]
d=t(fread(filein))

d_mean=rowMeans(d,na.rm = TRUE)

subn=dim(d)[1]/2
num_roi=200
num_edge=num_roi*num_roi/2-num_roi/2

    ICC_all=vector()
    for (i in 1:num_edge){
    #for (i in 1:100){
        
      #print(i)
      if (i %% 100 == 0){
        print(100*i/num_edge)
      }
      iccdata=data.frame(matrix(, nrow = subn*2, ncol = 4))
      colnames(iccdata)=c('Subject','Session','data','FCMean')
      iccdata$Subject[1:subn]=1:subn
      iccdata$Session[1:subn]=1
      iccdata$data[1:subn]=d[seq(1,2*subn,2),i]
      iccdata$FCMean[1:subn]=d_mean[seq(1,2*subn,2)]
      
      iccdata$Subject[(subn+1):(subn*2)]=1:subn
      iccdata$Session[(subn+1):(subn*2)]=2
      iccdata$data[(subn+1):(subn*2)]=d[seq(2,2*subn,2),i] 
      iccdata$FCMean[(subn+1):(subn*2)]=d_mean[seq(2,2*subn,2)]
      
      # ICC

        lm=tryCatch({summary(lmer(data ~ FCMean + (1 | Subject),data=iccdata))}, error=function(e) {return('NA')})

      
      if (typeof(lm) != 'list'){
        ICC=0
      }else{
      Var_between=as.numeric(attributes(lm$varcor$Subject)$stddev)^2
      Var_within=as.numeric(attributes(lm$varcor)$sc)^2
      ICC=(Var_between)/(Var_between+Var_within)
      # Var_within: same subject, different pipelines
      # Var_between: different subjects, each subject has two samples
      }
      ICC_all=c(ICC_all,ICC)
    }
    #jpeg(paste0(outfolder,'/',a1,'_',a2,'_rplot.jpg'), width = 350, height = 350)
    #hist(ICC_all)
    #dev.off()
   print(ICC_all)

write.table(ICC_all, sub("Data_ICC","ICC",filein), append = FALSE, sep = ",",row.names = FALSE, col.names = FALSE)