from ..utils import spatial_corr_ridgeplot
from ..utils import ICC_ridgeplot

fc_handle=''
simpleplot=False
atlases=['200','600','1000']

wd_path='/Users/xinhui.li/Documents/reproducibility/LA/Reproducibility_Analysis'
base=wd_path+'/ROI'

namechangedict={'fmriprep_mni2009_2mm':'fMRIPrep MNI2009 2mm',
                'fmriprep_default':'fMRIPrep MNI2009 3.4mm',
                'fmriprep_mni2004_2mm':'fMRIPrep MNI2004 2mm',
                'fmriprep_mni2004_native':'fMRIPrep MNI2004 3.4mm',
                'fmriprep_mni152_2mm':'fMRIPrep MNI2006 2mm',
                'fmriprep_mni152_native':'fMRIPrep MNI2006 3.4mm'}

pipelines=['fmriprep_mni2009_2mm', 'fmriprep_default', 'fmriprep_mni2004_2mm', 'fmriprep_mni2004_native', 'fmriprep_mni152_2mm', 'fmriprep_mni152_native']

nameorder=spatial_corr_ridgeplot(base,base.replace('ROI','figures'),pipelines,atlases,namechangedict,fc_handle,simpleplot,'pearson')
ICC_ridgeplot(base.replace('ROI','figures'),base.replace('ROI','figures'),pipelines,atlases,namechangedict,simpleplot,nameorder)