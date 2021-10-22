

library(ICC)
library(gplots)
library(gridGraphics)
library(grid)
library(lme4)
library(R.matlab)
library(mgc)
library(doParallel)  
source('/Users/xinhui.li/Documents/reproducibility/LA/Reproducibility_Analysis/trace_only_unba.R')

# a new differentt I2C2
#source("https://neuroconductor.org/neurocLite.R")
#neuro_install('I2C2')
#library(I2C2)

## calculatew ICC

getICC <- function (i,subn,xcp_data,cpac_data){
  #print(i)
  if (i %% 100 == 0){
    print(100*i/num_edge)
  }
  iccdata=data.frame(matrix(, nrow = subn*2, ncol = 4))
  colnames(iccdata)=c('Subject','Session','data','FCMean')
  iccdata$Subject[1:subn]=1:subn 
  iccdata$Session[1:subn]=1
  iccdata$data[1:subn]=xcp_data[,i]
  iccdata$FCMean[1:subn]=rowMeans(xcp_data,na.rm = TRUE)
  
  iccdata$Subject[(subn+1):(subn*2)]=1:subn
  iccdata$Session[(subn+1):(subn*2)]=2
  iccdata$data[(subn+1):(subn*2)]=cpac_data[,i] 
  iccdata$FCMean[(subn+1):(subn*2)]=rowMeans(cpac_data,na.rm = TRUE)
  
  # ICC
  if (fc_handel != 'Scale' | fc_handel != 'Ranking'){ # regress out the FC mean if not using scaling and ranking.
    lm=tryCatch({summary(lmer(data ~ FCMean + (1 | Subject),data=iccdata))}, error=function(e) {return('NA')})
  }else{
    lm=tryCatch({summary(lmer(data ~  FCMean + (1 | Subject),data=iccdata))}, error=function(e) {return('NA')})
    
  }
  
  if (typeof(lm) != 'list'){
    ICC=0
  }else{
    Var_between=as.numeric(attributes(lm$varcor$Subject)$stddev)^2
    Var_within=as.numeric(attributes(lm$varcor)$sc)^2
    ICC=(Var_between)/(Var_between+Var_within)
  }
  return(ICC)
}

# sym_matrix_vector
symMat2vec <- function(mat){
  mat[lower.tri(mat,diag = TRUE)] <- 99999
  temp1=as.vector(t(mat))
  temp1=temp1[temp1 !=99999]
  if (fc_handel == 'Scale'){
    return(scale(temp1))
  }else if(fc_handel == 'Ranking'){
    return(rank(temp1))
  }else{
    return(temp1)
  }
}

vec2symMat <- function(vect,n){
  mat=matrix(, nrow = n, ncol = n);
  pre=1
  for (i in 1:n){
    mat[i,i]=1
    if (i != n){
      mat[i,(i+1):n] = vect[pre:(pre+n-i-1)]
      mat[(i+1):n,i] = vect[pre:(pre+n-i-1)]
      pre=(pre+n-i)
    }
  }
  return(mat)
}

  

matchYeo <- function(data){
  ### yeo map
  # myindex = read.csv("cc_yeo7map_match.csv");
  # myindex = myindex[order(myindex[,2]),]
  # 
  # index_none = match('YeoMap1',myindex[,2]);
  # myindex = myindex[c(index_none:200,1:index_none-1),]
  # 
  # data = data[,myindex[,1]]
  return(data)
}


loaddata <- function(csv, name ){
  # load data for each packages. each pipelines are different
    df=read.csv(file=csv,sep = '\t',header = FALSE)
    idx=1
    if (dim(df)[1] != 295){
      idx=dim(df)[1]-294
    }
    df=df[idx:dim(df)[1],2:(num_roi+1)]
    df=matchYeo(df)
  return(df)
}


run_icc <- function(a1,a2,outfolder){
  
  #### Note: ccs had different subject orders. no need
  # cpac: 1-2,	3-14,	15-30
  # ccs : 1-2,	19-30,	3-18
  #ccsOrder=c(1:2,19:30,3:18)
  
  ############# xcp
  xcpfolder=paste0(a1)
  file.names1 <- dir(xcpfolder, pattern =".1D") # thsi should be ordered by the subject ID from low to high
  
  ############# cpac with scp stype
  cpacfolder=paste0(a2)
  file.names2 <- dir(cpacfolder, pattern =".1D") # thsi should be ordered by the subject ID from low to high
  
  ### handle for incomplete data
  # loop through al lsubject
  
  #for (i in 25427:25456){
  for (i in c(25427:25429,25431:25456)){
      
    if (length(grep(i,file.names1))==1 & length(grep(i,file.names2))==0){
      file.names1=file.names1[-grep(i,file.names1)]
    }
    if (length(grep(i,file.names1))==0 & length(grep(i,file.names2))==1){
      file.names2=file.names2[-grep(i,file.names2)]
    }
    
  }
  subn=length(file.names1)
  
  xcp_data=matrix(, nrow = subn, ncol = num_edge);
  for(i in 1:subn){
    csv=paste0(xcpfolder,'/',file.names1[i])
    df=loaddata(csv,a1)
    df_corr=cor(df)
    xcp_data[i,]=symMat2vec(df_corr);
  }
  
  
  cpac_data=matrix(, nrow = subn, ncol = num_edge);

  for(i in 1:subn){
    csv=paste0(cpacfolder,'/',file.names2[i])
    df=loaddata(csv,a2)
    df_corr=cor(df)
    cpac_data[i,]=symMat2vec(df_corr);
  }
  
  if (runicc==1){
    # calculate ICC for each edge
    ICC_all=vector()
    for (i in 1:num_edge){
      if (i %% 100 == 0){
        print(100*i/num_edge)
      }
      iccdata=data.frame(matrix(, nrow = subn*2, ncol = 4))
      colnames(iccdata)=c('Subject','Session','data','FCMean')
      iccdata$Subject[1:subn]=1:subn
      iccdata$Session[1:subn]=1
      iccdata$data[1:subn]=xcp_data[,i]
      iccdata$FCMean[1:subn]=rowMeans(xcp_data,na.rm = TRUE)
      
      iccdata$Subject[(subn+1):(subn*2)]=1:subn
      iccdata$Session[(subn+1):(subn*2)]=2
      iccdata$data[(subn+1):(subn*2)]=cpac_data[,i] 
      iccdata$FCMean[(subn+1):(subn*2)]=rowMeans(cpac_data,na.rm = TRUE)
      
      # ICC
      if (fc_handel != 'Scale' | fc_handel != 'Ranking'){ # regress out the FC mean if not using scaling and ranking.
        lm=tryCatch({summary(lmer(data ~ FCMean + (1 | Subject),data=iccdata))}, error=function(e) {return('NA')})
      }else{
        lm=tryCatch({summary(lmer(data ~  FCMean + (1 | Subject),data=iccdata))}, error=function(e) {return('NA')})
        
      }
      
      if (typeof(lm) != 'list'){
        ICC=0
      }else{
        Var_between=as.numeric(attributes(lm$varcor$Subject)$stddev)^2
        Var_within=as.numeric(attributes(lm$varcor)$sc)^2
        ICC=(Var_between)/(Var_between+Var_within)
      }
      ICC_all=c(ICC_all,ICC)
    }

  }else{
    ICC_all='NA'
  }
  
  #### discriminability over subjects
  discr=discr.stat(as.matrix(rbind(xcp_data,cpac_data)),c(1:subn,1:subn))
  
  #### I2C2
  data_I2C2=as.matrix(rbind(xcp_data,cpac_data))
  data_I2C2=t(na.omit(t(data_I2C2)))
  I2C2_visit=c(rep(1,subn),rep(2,subn))
  I2C2_id=c(1:subn,1:subn)
  i2c2_num=I2C2(data_I2C2,I = subn,J = 2,visit = I2C2_visit, id =I2C2_id,demean = TRUE)
  
  return(list(ICC_all,discr$discr,i2c2_num$lambda))
}


iccplot_old <- function(data,outfile){
  
  ########### some old plot scripts
  myindex = read.csv("cc_yeo7map_match.csv");
  myindex = myindex[order(myindex[,2]),]
  index_none = match('YeoMap1',myindex[,2]);
  myindex = myindex[c(index_none:200,1:index_none-1),]
  
  Yeomap = factor(myindex[,2])
  # make labels for heatmap
  Yeomaplab = matrix(,nrow = 200,ncol =1)
  
  Yeomaplab[19] = 'ICN 1';
  Yeomaplab[48] = 'ICN 2';
  Yeomaplab[69] = 'ICN 3';
  Yeomaplab[90] = 'ICN 4';
  Yeomaplab[108] = 'ICN 5';
  Yeomaplab[126] = 'ICN 6';
  Yeomaplab[158] = 'ICN 7';
  Yeomaplab[190] = 'ICN 8';
  
  myBreaks = c(seq(0,0.4,length=10),seq(0.41,0.6,length=10),seq(0.61,0.8,length=10),seq(0.81,1,length=10))
  my_palette <- colorRampPalette(c("blue","green","red","purple"))(n = 39)
  
  ifile <- outfile
  png(ifile,units="px", width=2000, height=2000, res=300)
  heatmap.2(data,
            dendrogram='none', Rowv=FALSE, Colv=FALSE,
            trace='none',
            breaks=myBreaks, 
            col = my_palette,
            rowsep = c(38,59,78,101,116,136,179),
            colsep = c(38,59,78,101,116,136,179),
            sepcolor="white",
            labRow = Yeomaplab,
            labCol  = Yeomaplab,
            adjCol = c(NA,0.4),
            cexRow = 0.7,
            cexCol = 0.7,
            offsetRow = -0.2,
            offsetCol = 0.5,
            margins = c(14, 14),
            density.info = 'none',
            srtCol=45,
            key = FALSE)
  dev.off()
  
}


iccplot <- function(data,outfile){
  
  myBreaks = c(seq(0,0.4,length=10),seq(0.41,0.6,length=10),seq(0.61,0.8,length=10),seq(0.81,1,length=10))
  my_palette <- colorRampPalette(c("blue","green","red","purple"))(n = 39)
  
  ifile <- outfile
  png(ifile,units="px", width=2000, height=2000, res=300)
  heatmap.2(data,
            dendrogram='none', Rowv=FALSE, Colv=FALSE,
            trace='none',
            breaks=myBreaks, 
            col = my_palette,
            sepcolor="white",
            labRow = '',
            labCol  = '',
            adjCol = c(NA,0.4),
            cexRow = 0.7,
            cexCol = 0.7,
            offsetRow = -0.2,
            offsetCol = 0.5,
            margins = c(14, 14),
            density.info = 'none',
            srtCol=45,
            key = FALSE)
  dev.off()
  
}

basefolder='/Users/xinhui.li/Documents/reproducibility/LA/Reproducibility_Analysis'

num_roi=1000
num_edge=num_roi*num_roi/2-num_roi/2

setwd(paste0(basefolder,'/ROI/ROI_Schaefer',num_roi))
outfolder=paste0(basefolder,'/figures/ICC_Schaefer',num_roi) # to calculate I2C2 and dis

runicc=0
fc_handel='Scale'
fc_handel='Ranking'
fc_handel='Regress_out_Mean'
fc_handel=''

#####################################################################
#Figure1. ICC and Discriminability

runs=c('ABCD','fmriprep_default','ccs','cpac_default_v1.8','dpabi')

dis=matrix(,nrow=length(runs),ncol=length(runs))
i2c2_all=matrix(,nrow=length(runs),ncol=length(runs))

idx=1
for (i in 1:(length(runs)-1)){
  for (j in (i+1):length(runs)){
    a1=runs[i]
    a2=runs[j]
    print(paste0(a1,'_',a2))
    tmp=run_icc(a1,a2,outfolder)
    icc_all=tmp[[1]]
    discriminability=tmp[[2]]
    i2c2_one=tmp[[3]]
    
    if (runicc==1){
      # plot icc
      iccplot(vec2symMat(icc_all,num_roi),paste0(outfolder,'/ICC_',fc_handel,'_',a1,'_',a2,'.png'))
      # save icc to csv
      outcsv=paste0(outfolder,'/',a1,'_',a2,'_ICC.csv')
      write.table(icc_all,outcsv,sep=",",  col.names=FALSE,row.names = FALSE)
    }

    dis[i,j]=discriminability
    print(discriminability)
    
    i2c2_all[i,j]=i2c2_one
    print('I2C2 is:')
    print(i2c2_one)
    idx=idx+1
      
  }
}

print(dis)
print(i2c2_all)
# save discriminability
outcsv=paste0(outfolder,'/',paste0(runs,collapse = '_'),'_discriminability.csv')
write.table(dis,outcsv,sep=",",  col.names=TRUE,row.names = TRUE)