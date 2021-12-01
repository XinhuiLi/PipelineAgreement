import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
from scipy import stats
from scipy.io import loadmat
from scipy.stats import rankdata
from scipy.stats import spearmanr

def spatial_corr_ridgeplot(base,outpath,pipelines,atlases,namechangedict,fc_handle,simpleplot,corr_type):

    '''
    Function to prepare and, optionally, run the C-PAC workflow
    Parameters
    ----------
    base : string
        the base direcotory, the ROI data will be in base +'/ROI_Schaefer' + atlas + '/' + pipelinename
    pipelines : list of strings
        list of the pipelines to do correlaitons
    atlases : list
        list of atlases to ues, for example ['200','600','1000']
    namechangedict : dictionary
        keys are the pipeline names, values are the name to change to
    fc_handle : string
        how to hand the spatial correlation, it can be '','Scale','Ranking'
    simpleplot : boolean
        flag to indicate the combination of pipelines, True only plot the correlation betwene the first pipeline and the rest.
    corr_type: string
        which correlation to do: concordance, spearman, or pearson
    Returns:
        None, but save figure out.
    -------
    workflow : 
    '''

    # the order of ccs subjects correspondign to cpac nad ndmg
    # cpac: 1-2,    3-14,   15-30
    # ccs : 1-2,    19-30,  3-18

    #\u221a/data2/Projects/Lei/ndmg/Resting_Preprocessing/hnu/ndmg_out/func/roi-timeseries/CPAC200_res-2x2x2/sub-0025427_task-rest_bold_CPAC200_res-2x2x2_variant-mean_timeseries.npz
    def upper_tri_masking(A):
        m = A.shape[0]
        r = np.arange(m)
        mask = r[:,None] < r
        return A[mask]

    def upper_tri_indexing(A):
        m = A.shape[0]
        r,c = np.triu_indices(m,1)
        return A[r,c]

    # concordance_correlation_coefficient from https://github.com/stylianos-kampakis/supervisedPCA-Python/blob/master/Untitled.py
    def concordance_correlation_coefficient(y_true, y_pred,
                           sample_weight=None,
                           multioutput='uniform_average'):
        """Concordance correlation coefficient.
        The concordance correlation coefficient is a measure of inter-rater agreement.
        It measures the deviation of the relationship between predicted and true values
        from the 45 degree angle.
        Read more: https://en.wikipedia.org/wiki/Concordance_correlation_coefficient
        Original paper: Lawrence, I., and Kuei Lin. "A concordance correlation coefficient to evaluate reproducibility." Biometrics (1989): 255-268.  
        Parameters
        ----------
        y_true : array-like of shape = (n_samples) or (n_samples, n_outputs)
            Ground truth (correct) target values.
        y_pred : array-like of shape = (n_samples) or (n_samples, n_outputs)
            Estimated target values.
        Returns
        -------
        loss : A float in the range [-1,1]. A value of 1 indicates perfect agreement
        between the true and the predicted values.
        Examples
        --------
        >>> from sklearn.metrics import concordance_correlation_coefficient
        >>> y_true = [3, -0.5, 2, 7]
        >>> y_pred = [2.5, 0.0, 2, 8]
        >>> concordance_correlation_coefficient(y_true, y_pred)
        0.97678916827853024
        """
        cor=np.corrcoef(y_true,y_pred)[0][1]
        
        mean_true=np.mean(y_true)
        mean_pred=np.mean(y_pred)
        
        var_true=np.var(y_true)
        var_pred=np.var(y_pred)
        
        sd_true=np.std(y_true)
        sd_pred=np.std(y_pred)
        
        numerator=2*cor*sd_true*sd_pred
        
        denominator=var_true+var_pred+(mean_true-mean_pred)**2

        return numerator/denominator


    def ridgeplot(df,atlases,outfile):
        
        show_label=False
        # Initialize the FacetGrid object
        x=[]
        for i in np.unique(df['g']):
            x.append(np.median(df[df['g']==i]['x']))
        roworder=np.unique(df['g'])[np.argsort(x)[::-1]]

        # for colour and row name match
        with sns.plotting_context(font_scale=5):
            g1 = sns.FacetGrid(df, row="g", hue="g", aspect=len(pipelines)*(len(pipelines)-1)/2, height=2)
        default_rowname=g1.row_names

        sortidx=[]
        for i in default_rowname:
            sortidx.append(list(roworder).index(i))

        pal = np.asarray(sns.cubehelix_palette(len(np.unique(df['g'])), start=.5, rot=-.75,light=0.7))

        pal=pal[::-1]
        pal=pal[sortidx]
        with sns.plotting_context(font_scale=5):
            g = sns.FacetGrid(df, sharey=False, row="g", hue="g", row_order=roworder, aspect=5, height=2, palette=pal)

        if len(atlases)==1:
            g.map(sns.kdeplot, "x",shade=True,color='red')
        if len(atlases)==2:
            g.map(sns.kdeplot, "x",shade=True,color='red')
            g.map(sns.kdeplot, "xx",shade=True,color='blue')
        if len(atlases)==3:
            g.map(sns.kdeplot, "x",shade=True,color='red')
            g.map(sns.kdeplot, "xx",shade=True,color='blue')
            g.map(sns.kdeplot, "xxx",shade=True,color='black')

        lw_value=3
        g.map(plt.axvline, x=1, lw=lw_value, clip_on=False,color=(134/256.0,250/256.0,167/256.0))
        g.map(plt.axvline, x=0.9, lw=lw_value, clip_on=False,color=(128/256.0,171/256.0,69/256.0))
        g.map(plt.axvline, x=0.8, lw=lw_value, clip_on=False,color=(128/256.0,126/256.0,38/256.0))
        g.map(plt.axvline, x=0.7, lw=lw_value, clip_on=False,color=(246/256.0,192/256.0,66/256.0))
        g.map(plt.axvline, x=0.6, lw=lw_value, clip_on=False,color=(192/256.0,98/256.0,43/256.0))

        g.map(plt.axhline, y=0, lw=2, clip_on=False)

        # Define and use a simple function to label the plot in  axis coordinates
        def label(x, color, label):
            ax = plt.gca()
            ax.text(0, .2, label, fontweight="bold", color='black',fontsize=35,
                    ha="left", va="center", transform=ax.transAxes)

        if show_label==True:
            g.map(label, "x")
        # Set the subplots to overlap

        # change the x axis label size
        ax = plt.gca()
        ax.tick_params(axis = 'both', which = 'major', labelsize = 35)

         
        g.set(xlim=(0, 1))
        g.set_titles("")
        g.set(xlabel='')
        g.set(yticks=[])
        g.despine(bottom=True, left=True)

        if len(os.path.basename(outfile))>140:
            outfile=os.path.dirname(outfile)+ '/' + os.path.basename(outfile)[0:130]+'.png'

        g.savefig(outfile)
        return [x for _,x in sorted(zip(sortidx,default_rowname))]

    # define matrix for mean and median
    value_median=pd.DataFrame(np.zeros(((len(pipelines)*(len(pipelines)-1))//2,4)), columns=['Pipelines','Atlas200','Atlas600','Atlas1000'])
    value_std=pd.DataFrame(np.zeros(((len(pipelines)*(len(pipelines)-1))//2,4)), columns=['Pipelines','Atlas200','Atlas600','Atlas1000'])
    value_quartile=pd.DataFrame(np.zeros(((len(pipelines)*(len(pipelines)-1))//2,13)), columns=['Pipelines','25_Atlas200','50_Atlas200','75_Atlas200','100_Atlas200','25_Atlas600','50_Atlas600','75_Atlas600','100_Atlas600','25_Atlas1000','50_Atlas1000','75_Atlas1000','100_Atlas1000'])

    atlas_idx=0
    for atlas in atlases:

        num_idx=(len(pipelines)*(len(pipelines)-1))//2
        color_palette = sns.color_palette("Paired",num_idx)
        for i in range(0,len(pipelines)):
            for j in range(i+1,len(pipelines)):
                p1=pipelines[i]
                p2=pipelines[j]
                pp='sc_' + p1 + '_' + p2
                locals()[pp]=[]

        # basesub=25426
        sub_list=os.listdir(base +'/ROI_Schaefer' + atlas + '/v181-HBN-default')
        for sub in sub_list:
            stop=0
            for xxx in pipelines:
                foldercontent=os.listdir(base +'/ROI_Schaefer' + atlas + '/' + xxx)
                if sub not in str(foldercontent):
                    print(xxx + 'not in')
                    print(sub)
                    stop=1
            if stop==1:
                continue

            # put them all together, load each pipeline file and calcuate calrelaiton and give it a different name.
            for pl in pipelines:
                datafolder = base +'/ROI_Schaefer' + atlas + '/' + pl
                #${PH_SERVER_WORKING_ROOT}/CPAC_XCP/CPAC_aggre_output/sub-0025427a_ses-1_bandpassed_demeaned_filtered_antswarp_cc200.1D
                cpacfile=datafolder + '/' + sub
                data=np.genfromtxt(cpacfile)
                data=data.transpose()
                data_corr=np.corrcoef(data)
                tmp_corr_tri=upper_tri_indexing(data_corr)
                locals()[pl+'_corr_tri']=tmp_corr_tri

            def spatial_correlation(corr_a,corr_b,sc,corr_type):
                if fc_handle=='Scale':
                    print('here')
                    corr_a[np.isnan(corr_a)]=0
                    corr_b[np.isnan(corr_b)]=0
                    corr_a= (corr_a - corr_a.mean())/corr_a.std(ddof=0)
                    corr_b= (corr_b - corr_b.mean())/corr_b.std(ddof=0)
                if fc_handle == 'Ranking':
                    corr_a = rankdata(corr_a)
                    corr_b = rankdata(corr_b)
                x=np.isnan(corr_a) | np.isnan(corr_b)
                corr_a_new=corr_a[~x]
                corr_b_new=corr_b[~x]
                if corr_type == "spearman":
                    sc.append(spearmanr(corr_a_new,corr_b_new)[0])
                elif corr_type == "concordance":
                    sc.append(concordance_correlation_coefficient(corr_a_new,corr_b_new))
                else:
                    sc.append(np.corrcoef(corr_a_new,corr_b_new)[0,1])
                return sc

            ### do correlaiton between pipelines
            num_idx=(len(pipelines)*(len(pipelines)-1))//2
            color_palette = sns.color_palette("Paired",num_idx)
            for i in range(0,len(pipelines)):
                for j in range(i+1,len(pipelines)):
                    p1=pipelines[i]
                    corr1= locals()[p1 + '_corr_tri']
                    p2=pipelines[j]
                    corr2= locals()[p2 + '_corr_tri']
                    pp='sc_' + p1 + '_' + p2
                    locals()[pp] = spatial_correlation(corr1,corr2,locals()[pp],corr_type)

        idx=0
        num_idx=(len(pipelines)*(len(pipelines)-1))//2
        color_palette = sns.color_palette("Paired",num_idx)
        
        df_all=pd.DataFrame(columns = ['x','g'])
        if simpleplot == True:
            plotrange=1
        else:
            plotrange=len(pipelines)
        for i in range(0,plotrange):
            for j in range(i+1,len(pipelines)):
                print(idx)
                p1=pipelines[i]
                p2=pipelines[j]
                pp1='sc_' + p1 + '_' + p2
                pp2='sc_' + p2 + '_' + p1
                if pp1 in locals():
                    pp = locals()[pp1]
                    print(pp1)
                elif pp2 in locals():
                    pp = locals()[pp2]
                    print(pp2)
                pn1=p1
                pn2=p2
                for key in namechangedict:
                    pn1=pn1.replace(key,namechangedict[key])
                for key in namechangedict:
                    pn2=pn2.replace(key,namechangedict[key])

                # get median and std
                print(pp1+str(np.median(pp))+str(np.std(pp)))
                value_median['Pipelines'][idx] = pp1
                value_median['Atlas'+atlas][idx] = np.median(pp)

                value_std['Pipelines'][idx] = pp1
                value_std['Atlas'+atlas][idx] = np.std(pp)

                value_quartile['Pipelines'][idx] = pp1
                for pct_val in [25,50,75,100]:
                    value_quartile[str(pct_val)+'_Atlas'+atlas][idx] = np.percentile(pp, pct_val, interpolation = 'midpoint') 

                tmp=pd.DataFrame(pp, columns=['x'])
                tmp['g']=pn1+' - '+pn2
                df_all=pd.concat([df_all,tmp])
                idx +=1

        # put multiple atlas in one ridge plot. 
        if atlas_idx==0:
            df_ridge =df_all
        elif atlas_idx==1:
            df_ridge['xx']=df_all['x']
        elif atlas_idx==2:
            df_ridge['xxx']=df_all['x']
        atlas_idx += 1

    print(value_median)
    value_median.to_csv(os.path.dirname(base) + '/figures/Ridgeplot_spatial_corr_'+corr_type+'_'+'-'.join(pipelines)[0:90]+'_Median.csv')
    value_std.to_csv(os.path.dirname(base) + '/figures/Ridgeplot_spatial_corr_'+corr_type+'_'+'-'.join(pipelines)[0:90]+'_std.csv')

    value_quartile.to_csv(os.path.dirname(base) + '/figures/Ridgeplot_spatial_corr_'+corr_type+'_'+'-'.join(pipelines)[0:90]+'_quartile.csv')


    plotnameorder=ridgeplot(df_ridge,atlases,os.path.dirname(base) + '/figures/Ridgeplot_spatial_corr_'+corr_type+'_'+'-'.join(pipelines)[0:90]+'_'+atlas+'.png')

    return plotnameorder

def ICC_ridgeplot(base,outpath,pipelines,atlases,namechangedict,simpleplot,plotnameorder):

    def ridgeplot(df,atlases,outfile,plotnameorder):
        show_label=False
        # Initialize the FacetGrid object
        x=[]
        for i in np.unique(df['g']):
            x.append(np.median(df[df['g']==i]['x']))
        roworder=np.unique(df['g'])[np.argsort(x)[::-1]]

        # for colour and row name match
        with sns.plotting_context(font_scale=5):
            g1 = sns.FacetGrid(df, row="g", hue="g", aspect=len(pipelines)*(len(pipelines)-1)/2, height=2)
        default_rowname=g1.row_names

        if plotnameorder:
            default_rowname=plotnameorder
        sortidx=[]
        for i in default_rowname:
            sortidx.append(list(roworder).index(i))

        pal = np.asarray(sns.cubehelix_palette(len(np.unique(df['g'])), start=.5, rot=-.75,light=0.7))

        pal=pal[::-1]
        pal=pal[sortidx]
        with sns.plotting_context(font_scale=5):
            g = sns.FacetGrid(df, sharey=False, row="g", hue="atlas", row_order=roworder, aspect=5, height=2, palette=['red','blue','black'])

        g.map(sns.kdeplot, "x", shade=True)

        lw_value=3
        g.map(plt.axvline, x=1, lw=lw_value, clip_on=False,color=(134/256.0,250/256.0,167/256.0))
        g.map(plt.axvline, x=0.9, lw=lw_value, clip_on=False,color=(128/256.0,171/256.0,69/256.0))
        g.map(plt.axvline, x=0.8, lw=lw_value, clip_on=False,color=(128/256.0,126/256.0,38/256.0))
        g.map(plt.axvline, x=0.7, lw=lw_value, clip_on=False,color=(246/256.0,192/256.0,66/256.0))
        g.map(plt.axvline, x=0.6, lw=lw_value, clip_on=False,color=(192/256.0,98/256.0,43/256.0))

        g.map(plt.axhline, y=0, lw=2, clip_on=False)

        # Define and use a simple function to label the plot in  axis coordinates
        def label(x, color, label):
            ax = plt.gca()
            ax.text(0, .2, label, fontweight="bold", color='black',fontsize=35,
                    ha="left", va="center", transform=ax.transAxes)
        if show_label==True:
            g.map(label, "x")
        # Set the subplots to overlap

        # change the x axis label size
        ax = plt.gca()
        ax.tick_params(axis = 'both', which = 'major', labelsize = 35)

         
        g.set(xlim=(0, 1))
        g.set_titles("")
        g.set(xlabel='')
        g.set(yticks=[])
        g.despine(bottom=True, left=True)

        if len(os.path.basename(outfile))>140:
            outfile=os.path.dirname(outfile)+ '/' + os.path.basename(outfile)[0:130]+'.png'


        g.savefig(outfile)


    value_median=pd.DataFrame(np.zeros(((len(pipelines)*(len(pipelines)-1))//2,4)), columns=['Pipelines','Atlas200','Atlas600','Atlas1000'])
    value_std=pd.DataFrame(np.zeros(((len(pipelines)*(len(pipelines)-1))//2,4)), columns=['Pipelines','Atlas200','Atlas600','Atlas1000'])
    value_quartile=pd.DataFrame(np.zeros(((len(pipelines)*(len(pipelines)-1))//2,13)), columns=['Pipelines','25_Atlas200','50_Atlas200','75_Atlas200','100_Atlas200','25_Atlas600','50_Atlas600','75_Atlas600','100_Atlas600','25_Atlas1000','50_Atlas1000','75_Atlas1000','100_Atlas1000'])


    atlas_idx=0
    for atlas in atlases:
        print(atlas)
        df_all=pd.DataFrame(columns = ['x','g'])
        idx=0
        if simpleplot == True:
            plotrange=1
        else:
            plotrange=len(pipelines)
        for i in range(0,plotrange):
            for j in range(i+1,len(pipelines)):
                p1=pipelines[i]
                p2=pipelines[j]
                p1=p1.replace('ABCD','abcd')
                p2=p2.replace('ABCD','abcd')
                pp1= base+ '/ICC_Schaefer' + atlas + '/' + p1 + '_' + p2 + '_ICC.csv'
                pp2= base+ '/ICC_Schaefer' + atlas + '/' + p2 + '_' + p1 + '_ICC.csv'
                print(pp1)
                print(pp2)
                if os.path.isfile(pp1):
                    tmp=pd.read_csv(pp1,header=None,names=['x'])
                    tmp=tmp['x'][np.where(tmp>np.finfo(np.float32).eps)[0]].to_frame()
                elif os.path.isfile(pp2):
                    tmp=pd.read_csv(pp2,header=None,names=['x'])
                    tmp=tmp['x'][np.where(tmp>np.finfo(np.float32).eps)[0]].to_frame()
                
                pn1=p1
                pn2=p2
                for key in namechangedict:
                    pn1=pn1.replace(key,namechangedict[key])
                for key in namechangedict:
                    pn2=pn2.replace(key,namechangedict[key])

                # get median and std
                print(pp1+str(np.median(tmp))+str(np.std(tmp)))
                value_median['Pipelines'][idx] = p1+'_'+p2
                value_median['Atlas'+atlas][idx] = np.median(tmp)

                value_std['Pipelines'][idx] = p1+'_'+p2
                value_std['Atlas'+atlas][idx] = np.std(tmp)

                value_quartile['Pipelines'][idx] = p1+'_'+p2
                for pct_val in [25,50,75,100]:
                    value_quartile[str(pct_val)+'_Atlas'+atlas][idx] = np.percentile(tmp, pct_val, interpolation = 'midpoint') 

                tmp['g']=pn1+' - '+pn2
                df_all=pd.concat([df_all,tmp])
                print(df_all.head(3))
                idx += 1
        # put multiple atlas in one plot
        if atlas=='200':
            df_ridge_1=df_all
            df_ridge_1['atlas']='200'
        elif atlas=='600':
            df_ridge_2=df_all
            df_ridge_2['atlas']='600'
        elif atlas=='1000':
            df_ridge_3=df_all
            df_ridge_3['atlas']='1000'

    if len(atlases)==1:
        df=pd.concat([df_ridge_1])
    if len(atlases)==2:
        df=pd.concat([df_ridge_1])
        df=pd.concat([df_ridge_1,df_ridge_2])
    if len(atlases)==3:
        df=pd.concat([df_ridge_1])
        df=pd.concat([df_ridge_1,df_ridge_2])
        df=pd.concat([df_ridge_1,df_ridge_2,df_ridge_3])
    df = df[df['x'] != 0]

    print(value_median)

    value_median.to_csv(os.path.dirname(base) + '/figures/Ridgeplot_ICC_'+'_'+'-'.join(pipelines)[0:90]+'_Median.csv')
    value_std.to_csv(os.path.dirname(base) + '/figures/Ridgeplot_ICC_'+'_'+'-'.join(pipelines)[0:90]+'_std.csv')
    value_quartile.to_csv(os.path.dirname(base) + '/figures/Ridgeplot_ICC_'+'_'+'-'.join(pipelines)[0:90]+'_quartile.csv')

    ridgeplot(df,atlases,outpath + '/Ridgeplot_ICC_'+'_'+'-'.join(pipelines)[0:90]+'_'+atlas+'.png',plotnameorder)


if __name__=='__main__':
    fc_handle=''
    simpleplot=False
    atlases=['200','600','1000']

    wd_path=os.environ.get("BASEFOLDER")
    base=wd_path+'/ROI'

    namechangedict={'v181-HBN-default':'CPAC:Default',
                    'v181-HBN-fmriprep-opts':'fMRIPrep',
                    'v181-HBN-DCAN':'abcd',
                    'v181-HBN-CCS':'CCS'}

    pipelines=['v181-HBN-CCS', 'v181-HBN-DCAN', 'v181-HBN-default', 'v181-HBN-fmriprep-opts']

    nameorder=spatial_corr_ridgeplot(base,base.replace('ROI','figures'),pipelines,atlases,namechangedict,fc_handle,simpleplot,'pearson')
    ICC_ridgeplot(base.replace('ROI','figures'),base.replace('ROI','figures'),pipelines,atlases,namechangedict,simpleplot,nameorder)