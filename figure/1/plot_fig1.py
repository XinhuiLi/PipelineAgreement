from ..utils.utils import spatial_corr_ridgeplot
from ..utils.utils import ICC_ridgeplot

fc_handle=''
simpleplot=False
atlases=['200','600','1000']
base='/Users/xinhui.li/Documents/reproducibility/LA/Reproducibility_Analysis/ROI'

namechangedict={'cpac_default_v1.8':'CPAC:Default',
                'fmriprep_default':'fMRIPrep',
                'ABCD':'abcd',
                'ccs_rerun':'CCS',
                'dpabi':'DPARSF'}

pipelines=['ABCD','fmriprep_default','ccs_rerun','cpac_default_v1.8','dpabi']

nameorder=spatial_corr_ridgeplot(base,base.replace('ROI','figures'),pipelines,atlases,namechangedict,fc_handle,simpleplot,'pearson')
ICC_ridgeplot(base.replace('ROI','figures'),base.replace('ROI','figures'),pipelines,atlases,namechangedict,simpleplot,nameorder)