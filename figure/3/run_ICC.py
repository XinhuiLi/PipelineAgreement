import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
from scipy import stats
from scipy.io import loadmat
from scipy.stats import rankdata
from scipy.stats import spearmanr
import random
import string
from itertools import combinations
from scipy.stats import gaussian_kde
from hyppo.discrim import DiscrimOneSample
from sklearn.preprocessing import minmax_scale

def kde_scipy(x, x_grid, bandwidth=0.2, **kwargs):
    #x_grid = np.linspace(-4.5, 3.5, 1000)
    """Kernel Density Estimation with Scipy"""
    # Note that scipy weights its bandwidth by the covariance of the
    # input data.  To make the results comparable to the other methods,
    # we divide the bandwidth by the sample standard deviation here.
    kde = gaussian_kde(x, bw_method=bandwidth / x.std(ddof=1), **kwargs)
    return kde.evaluate(x_grid)


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def mkdirs1(folder):
    if not os.path.isdir(folder):
        os.makedirs(folder)


def timeseries_bootstrap(tseries, block_size, random_state=None):
    """
    Generates a bootstrap sample derived from the input time-series.
    Utilizes Circular-block-bootstrap method described in [1]_.

    Parameters
    ----------
    tseries : array_like
        A matrix of shapes (`M`, `N`) with `M` timepoints and `N` variables
    block_size : integer
        Size of the bootstrapped blocks
    random_state : integer
        the random state to seed the bootstrap

    Returns
    -------
    bseries : array_like
        Bootstrap sample of the input timeseries


    References
    ----------
    .. [1] P. Bellec; G. Marrelec; H. Benali, A bootstrap test to investigate
       changes in brain connectivity for functional MRI. Statistica Sinica,
       special issue on Statistical Challenges and Advances in Brain Science,
       2008, 18: 1253-1268.

    Examples
    --------

    >>> x = np.arange(50).reshape((5, 10)).T
    >>> sample_bootstrap(x, 3)
    array([[ 7, 17, 27, 37, 47 ],
           [ 8, 18, 28, 38, 48 ],
           [ 9, 19, 29, 39, 49 ],
           [ 4, 14, 24, 34, 44 ],
           [ 5, 15, 25, 35, 45 ],
           [ 6, 16, 26, 36, 46 ],
           [ 0, 10, 20, 30, 40 ],
           [ 1, 11, 21, 31, 41 ],
           [ 2, 12, 22, 32, 42 ],
           [ 4, 14, 24, 34, 44 ]])

    """
    import numpy as np

    if not random_state:
        random_state = np.random.RandomState()

    # calculate number of blocks
    k = int(np.ceil(float(tseries.shape[0]) / block_size))

    # generate random indices of blocks
    r_ind = np.floor(random_state.rand(1, k) * tseries.shape[0])
    blocks = np.dot(np.arange(0, block_size)[:, np.newaxis], np.ones([1, k]))

    block_offsets = np.dot(np.ones([block_size, 1]), r_ind)
    block_mask = (blocks + block_offsets).flatten('F')[:tseries.shape[0]]
    block_mask = np.mod(block_mask, tseries.shape[0])

    return tseries[block_mask.astype('int'), :], block_mask.astype('int')


def spatial_corr_plot(base,outpath,pipelines_list,atlases,namechangedict,fc_handle,simpleplot,corr_type):

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

    def upper_tri_masking(A):
        m = A.shape[0]
        r = np.arange(m)
        mask = r[:,None] < r
        return A[mask]

    def upper_tri_indexing(A):
        m = A.shape[0]
        r,c = np.triu_indices(m,1)
        return A[r,c]

    def load_multple_sess_data(datafolder,sub,sessions):

        if 'sess_ave' in locals():
            del sess_ave

        if bootstrapping_ci == True: # not average boostrapping resamples, but use them to extract confident intervals and show them on plot.
            # first of all stack session data all together, ie, 1 session: 295*200, if there are threes sessions: 295*600
            # the stacked data will be bootstrapped to get 100 of 295*600, then it will breack down to 3 295:200
            # This will be ensure that alls sessions will be gone through the same resampling in each boostrapping.

            if 'dataall' in locals():
                del dataall 
            for ses in sessions1:
                cpacfile=datafolder1 + '/sub-00' + str(sub) + ses + '.1D'
                #print(cpacfile)
                data=np.genfromtxt(cpacfile)
                if data.shape[0] != 295:
                    idx= data.shape[0]-295
                    data=data[idx:,]
                if 'dataall' in locals():
                    dataall=np.concatenate((dataall,data),axis=1)
                else:
                    dataall=data

            for ses in sessions2:
                cpacfile=datafolder2 + '/sub-00' + str(sub) + ses + '.1D'
                #print(cpacfile)
                data=np.genfromtxt(cpacfile)
                if data.shape[0] != 295:
                    idx= data.shape[0]-295
                    data=data[idx:,]
                if 'dataall' in locals():
                    dataall=np.concatenate((dataall,data),axis=1)
                else:
                    dataall=data

            block_size=np.int(np.floor(np.sqrt(dataall.shape[0])))
            bs_size=100
            tmp_corr_tri_tmp_all1 = np.empty((((data.shape[1]*data.shape[1]-data.shape[1])/2),bs_size))     
            tmp_corr_tri_tmp_all2 = np.empty((((data.shape[1]*data.shape[1]-data.shape[1])/2),bs_size))                

            for bs_idx in range(0,bs_size):
                tmp_pipelins=timeseries_bootstrap(dataall,block_size)[0] # it returns time of point * all session parcels
                
                tmp=tmp_pipelins[:,0:tmp_pipelins.shape[1]/2]
                # break down to sessions and pipelines
                tmp_corr_tri_tmp=np.float64(np.repeat(0,(data.shape[1]*data.shape[1]-data.shape[1])/2))
                for jj in range(0,tmp.shape[1]/int(atlas)):
                    xx=tmp[:,jj*int(atlas):((jj+1)*int(atlas))]
                    xx=xx.transpose()
                    xx_corr=np.corrcoef(xx)
                    tmp_corr_tri_tmp += upper_tri_indexing(xx_corr)
                tmp_corr_tri_tmp=tmp_corr_tri_tmp/(jj+1) # average across sessions.
                tmp_corr_tri_tmp_all1[:,bs_idx]=tmp_corr_tri_tmp

                tmp=tmp_pipelins[:,tmp_pipelins.shape[1]/2:]
                # break down to sessions and pipelines
                tmp_corr_tri_tmp=np.float64(np.repeat(0,(data.shape[1]*data.shape[1]-data.shape[1])/2))
                for jj in range(0,tmp.shape[1]/int(atlas)):
                    xx=tmp[:,jj*int(atlas):((jj+1)*int(atlas))]
                    xx=xx.transpose()
                    xx_corr=np.corrcoef(xx)
                    tmp_corr_tri_tmp += upper_tri_indexing(xx_corr)
                tmp_corr_tri_tmp=tmp_corr_tri_tmp/(jj+1) # average across sessions.
                tmp_corr_tri_tmp_all2[:,bs_idx]=tmp_corr_tri_tmp

            return tmp_corr_tri_tmp_all1, tmp_corr_tri_tmp_all2

        else: #average boostrapping or not use boostrapping.
            if 'sess_ave' in locals():
                del sess_ave
            for ses in sessions:
                cpacfile=datafolder + '/sub-00' + str(sub) + ses + '.1D'
                #print(cpacfile)

                #data=np.genfromtxt(cpacfile)
                data=globals()[os.path.basename(datafolder)  + str(sub) + ses]

                if data.shape[0] != 295:
                    idx= data.shape[0]-295
                    data=data[idx:,]

                if bootstrapping_average == True: # if doing bootstrapping and average within subjects.
                    ### bootstrapping the time series and then get the correlaiton matrix for each bootstrapping timeseries, then average the correlaiton matrix over all the bootstraping.
                    block_size=np.int(np.floor(np.sqrt(data.shape[0])))
                    bs_size=100
                    if 'data_bs' in locals():
                        del data_bs
                    for bs_idx in range(0,bs_size):
                        tmp=timeseries_bootstrap(data,block_size)[0]
                        tmp=tmp.transpose()
                        tmp_corr=np.corrcoef(tmp)
                        tmp_corr_tri_tmp=upper_tri_indexing(tmp_corr)   
                        if 'data_bs' in locals():
                            data_bs=data_bs+tmp_corr_tri_tmp
                        else:
                            data_bs=tmp_corr_tri_tmp
                    tmp_corr_tri_tmp=data_bs/bs_size
                else: # not doing bootstrapping at all
                    data=data.transpose()
                    data_corr=np.corrcoef(data)

                    if fc_handle == 'Ranking':
                        data_corr_tmp = np.abs(data_corr)
                        data_corr_tmp = np.reshape(minmax_scale(rankdata(data_corr_tmp)), data_corr_tmp.shape)
                        data_corr = np.sign(data_corr) * data_corr_tmp

                    tmp_corr_tri_tmp=upper_tri_indexing(data_corr)

                if 'sess_ave' in locals():
                    sess_ave=sess_ave+tmp_corr_tri_tmp
                else:
                    sess_ave=tmp_corr_tri_tmp
            return sess_ave/len(sessions)

    def spatial_correlation(corr_a,corr_b,sc,corr_type):
        if bootstrapping_ci == True:
            for jj in range(0,corr_a.shape[1]):
                sc.append(np.corrcoef(corr_a[:,jj],corr_b[:,jj])[0,1])
            return sc
        else:
            if fc_handle=='Scale':
                corr_a[np.isnan(corr_a)]=0
                corr_b[np.isnan(corr_b)]=0
                corr_a= (corr_a - corr_a.mean())/corr_a.std(ddof=0)
                corr_b= (corr_b - corr_b.mean())/corr_b.std(ddof=0)
            # if fc_handle == 'Ranking':
                # corr_a = np.reshape(minmax_scale(rankdata(corr_a)), corr_a.shape)
                # corr_b = np.reshape(minmax_scale(rankdata(corr_b)), corr_b.shape)
            x=np.isnan(corr_a) | np.isnan(corr_b)
            corr_a_new=corr_a[~x]
            corr_b_new=corr_b[~x]
            if corr_type == "spearman":
                sc.append(spearmanr(corr_a_new,corr_b_new)[0])
            elif corr_type == "concordance":
                sc.append(concordance_correlation_coefficient(corr_a_new,corr_b_new))
            else:
                sc.append(np.corrcoef(corr_a_new,corr_b_new)[0,1])
                #print(np.corrcoef(corr_a_new,corr_b_new)[0,1])
            return sc


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


    num_pair=len(pipelines_list) # this is number of rows of the plot


    plt.cla()
    fig, axs = plt.subplots(num_pair,3,figsize=(15,12),sharex=True,dpi=600)
    plt.xlim(0, 1.1) 

    duration10=[['a'],['j']]
    duration30=[['a','b','c'],['h','i','j']]
    duration50=[['a','b','c','d','e'],['f','g','h','i','j']]
    
    # random select sessions
    All_sessions=['a','b','c','d','e','f','g','h','i','j']
    def list_difference(list1,list2):
        list_difference = []
        for item in list1:
            if item not in list2:
                list_difference.append(item)
        return list_difference

    ### random select sessions. and then plot all of them
    duration30_all=[]
    duration50_all=[]
    ses10_all=list(combinations(All_sessions, 2))

    aaaa=10 
    for ses_select in range (0,aaaa):
        print('Another random session:' + str(ses_select))
        # 10:
        duration10=[list(aaa) for aaa in list(ses10_all[ses_select])]
        print(duration10)

        # 30:
        tt=3
        tmp1=random.sample(All_sessions,tt)
        tmp2=random.sample(list_difference(All_sessions,tmp1),tt)
        duration30=[tmp1,tmp2]
        tmp=''.join(sum(duration30,[]))
        # duration30_all.append(tmp)
        while tmp in duration30_all or tmp[::-1] in duration30_all:
            tmp1=random.sample(All_sessions,tt)
            tmp2=random.sample(list_difference(All_sessions,tmp1),tt)
            duration30=[tmp1,tmp2]
            tmp=''.join(sum(duration30,[]))
        duration30_all.append(tmp)

       # 50:
        tt=5
        tmp1=random.sample(All_sessions,tt)
        tmp2=random.sample(list_difference(All_sessions,tmp1),tt)
        duration50=[tmp1,tmp2]
        tmp=''.join(sum(duration50,[]))
        while tmp in duration50_all or tmp[::-1] in duration50_all:
            tmp1=random.sample(All_sessions,tt)
            tmp2=random.sample(list_difference(All_sessions,tmp1),tt)
            duration50=[tmp1,tmp2]
            tmp=''.join(sum(duration50,[]))
        duration50_all.append(tmp)

        name_postfix=''.join(sum(duration10, [])) + '_' + ''.join(sum(duration30, [])) + '_' + ''.join(sum(duration50, []))

        for atlas in atlases:
            # loop through each row, pipelines pairs
            for p_idx in range(0,num_pair):
                print(p_idx)
                pipelines=pipelines_list[p_idx][0:2]
                pl_handle=pipelines_list[p_idx][2]
                print(pipelines)
                '''
                if p_idx <=1:
                    p_idx=p_idx+6
                else:
                    p_idx=p_idx+12     
                print(p_idx)
                '''
                # Loop through 10min, 30min, and 50min.
                col_indx=0
                for duration_col in [duration10,duration30,duration50]:
                #for duration_col in [duration10]:

                    col_indx += 1
                    print(duration_col)
                    if pl_handle == 'different':
                        session_idx=[0,1]
                    else:
                        session_idx=[0,0]
                
                    #### Get each figure done
                    sess_all=[] # get all session used first, will check if have them all.
                    for ii in session_idx:
                        for ses in duration_col[ii]:
                            sess_all.append(ses)

                    for i in range(0,len(pipelines)):
                        for j in range(i+1,len(pipelines)):
                            p1=pipelines[i]
                            p2=pipelines[j]
                            pp='sc_' + p1 + '_' + p2
                            locals()[pp]=[]
      
                    # discrimination dataset an R script will be called
                    if 'discm_data' in locals():
                        del discm_data
                    basesub=25426
                    for isub in range(1,31):
                        if basesub+isub == 25430:
                            continue
                        stop=0
                        for xxx in pipelines:
                            fodlercontent=os.listdir(base +'/ROI_Schaefer' + atlas + '/' + xxx)
                            for ses in sess_all:
                                if (str(isub+basesub) + ses) not in str(fodlercontent):
                                    print(isub+basesub)
                                    stop=1
                        if stop==1:
                            continue

                        # same session and different session will be different:
                        for pl, ii in zip(pipelines, session_idx):
                            datafolder = base +'/ROI_Schaefer' + atlas + '/' + pl

                            # load the data - need to average sessions.
                            tmp_corr_tri=load_multple_sess_data(datafolder,str(isub+basesub),duration_col[ii])

                            if pl+'_corr_tri' in locals():
                                locals()[pl+'_1_corr_tri']=tmp_corr_tri
                            else:
                                locals()[pl+'_corr_tri']=tmp_corr_tri

                            # discriminability
                            if 'discm_data' in locals():
                                discm_data = np.row_stack((discm_data,tmp_corr_tri))
                            else:
                                discm_data=tmp_corr_tri
                        
                        ### calculate correlaiton between pipelines
                        num_idx=(len(pipelines)*(len(pipelines)-1))/2

                        for i in range(0,len(pipelines)):
                            for j in range(i+1,len(pipelines)):
                                p1=pipelines[i]
                                p2=pipelines[j]

                                corr1= locals()[p1 + '_corr_tri']
                                if p1 == p2:
                                    corr2= locals()[p2 + '_1_corr_tri']
                                else:
                                    corr2= locals()[p2 + '_corr_tri']

                                pp='sc_' + p1 + '_' + p2
                                locals()[pp] = spatial_correlation(corr1,corr2,locals()[pp],corr_type)

                        for pl, ii in zip(pipelines, session_idx):
                            if pl+'_1_corr_tri' in locals():
                                del locals()[pl+'_1_corr_tri']
                            if pl+'_corr_tri' in locals():
                                del locals()[pl+'_corr_tri']

                    print(discm_data.shape)
                    fileout=outpath + '/Data_ICC_1000_All_'+corr_type+'/Random-'+ str(ses_select)+'_Pipeline-'+str(p_idx) + '_Ses_'+str(col_indx)+'.txt' 
                    mkdirs1(os.path.dirname(fileout))
                    np.savetxt(fileout,discm_data.transpose())
                    discm_data=discm_data[:, ~np.isnan(discm_data).any(axis=0)]
                    disc_num=DiscrimOneSample().test(discm_data,np.repeat(range(1,(int(discm_data.shape[0]/2)+1)),2))
                    fileout=outpath + '/disc_num_1000_All_'+corr_type+'/Random-'+ str(ses_select)+'_Pipeline-'+str(p_idx) + '_Ses_'+str(col_indx)+'.txt' 
                    mkdirs1(os.path.dirname(fileout))
                    np.savetxt(fileout,[disc_num])
                    print('discr number is' + str(disc_num))

                    if simpleplot == True:
                        plotrange=1
                    else:
                        plotrange=len(pipelines)
                    for i in range(0,plotrange):
                        for j in range(i+1,len(pipelines)):
                            p1=pipelines[i]
                            p2=pipelines[j]
                            pp1='sc_' + p1 + '_' + p2
                            pp2='sc_' + p2 + '_' + p1
                            if pp1 in locals():
                                pp = locals()[pp1]
                            elif pp2 in locals():
                                pp = locals()[pp2]
                            pn1=p1
                            pn2=p2
                            for key in namechangedict:
                                if pn1 == key:
                                    pn1 = namechangedict[key]

                            pn1=pn1.replace('cpac','CPAC:fmriprep')
                            for key in namechangedict:
                                if pn2 == key:
                                    pn2 = namechangedict[key]
                            if bootstrapping_ci == True: # this will plot the mean spatial correlation and plot the confident interval
                                pp_bs = np.empty((len(pp)/100,100))
                                for jj in range(0,len(pp)/100):
                                    pp_bs[jj,:]=pp[jj*100:(jj+1)*100]
                                print('The final spatial correlation')
                                g=sns.distplot(pp,color= 'black',hist=False,ax=axs[p_idx,col_indx-1],axlabel='')
                            else:
                                fileout=outpath + '/CI_files_1000_All_' + corr_type + '/Random-'+ str(ses_select)+'_Pipeline-'+str(p_idx) + '_Ses_'+str(col_indx)+'.txt' 
                                mkdirs1(os.path.dirname(fileout))
                                np.savetxt(fileout,pp)


####################################
#Example to call the functions

pipelines_list=[
    ### same scans, same pipelines ###
    # ABCD
    ['cpac_abcd_all','cpac_abcd_all','same'], # no GSR vs no GSR
    ['cpac_abcd_all_gsr','cpac_abcd_all_gsr','same'], # GSR vs GSR
    ['cpac_abcd_all','cpac_abcd_all_gsr','same'], # no GSR vs GSR
    # CCS
    ['cpac_ccs_all','cpac_ccs_all','same'], # no GSR vs no GSR
    ['cpac_ccs_all_gsr','cpac_ccs_all_gsr','same'], # GSR vs GSR
    ['cpac_ccs_all','cpac_ccs_all_gsr','same'], # no GSR vs GSR
    # default
    ['cpac_default_all','cpac_default_all','same'], # no GSR vs no GSR
    ['cpac_default_all_gsr','cpac_default_all_gsr','same'], # GSR vs GSR
    ['cpac_default_all','cpac_default_all_gsr','same'], # no GSR vs GSR
    # fMRIPrep
    ['cpac_fmriprep_all','cpac_fmriprep_all','same'], # no GSR vs no GSR
    ['cpac_fmriprep_all_gsr','cpac_fmriprep_all_gsr','same'], # GSR vs GSR
    ['cpac_fmriprep_all','cpac_fmriprep_all_gsr','same'], # no GSR vs GSR
    ### same scans, different pipelines ###
    # ABCD vs CCS
    ['cpac_abcd_all','cpac_ccs_all','same'], # no GSR vs no GSR
    ['cpac_abcd_all_gsr','cpac_ccs_all_gsr','same'], # GSR vs GSR
    ['cpac_abcd_all','cpac_ccs_all_gsr','same'], # no GSR vs GSR
    ['cpac_abcd_all_gsr','cpac_ccs_all','same'], # GSR vs no GSR
    # ABCD vs default
    ['cpac_abcd_all','cpac_default_all','same'], # no GSR vs no GSR
    ['cpac_abcd_all_gsr','cpac_default_all_gsr','same'], # GSR vs GSR
    ['cpac_abcd_all','cpac_default_all_gsr','same'], # no GSR vs GSR
    ['cpac_abcd_all_gsr','cpac_default_all','same'], # GSR vs no GSR
    # ABCD vs fMRIPrep
    ['cpac_abcd_all','cpac_fmriprep_all','same'], # no GSR vs no GSR
    ['cpac_abcd_all_gsr','cpac_fmriprep_all_gsr','same'], # GSR vs GSR
    ['cpac_abcd_all','cpac_fmriprep_all_gsr','same'], # no GSR vs GSR
    ['cpac_abcd_all_gsr','cpac_fmriprep_all','same'], # GSR vs no GSR
    # CCS vs default
    ['cpac_ccs_all','cpac_default_all','same'], # no GSR vs no GSR
    ['cpac_ccs_all_gsr','cpac_default_all_gsr','same'], # GSR vs GSR
    ['cpac_ccs_all','cpac_default_all_gsr','same'], # no GSR vs GSR
    ['cpac_ccs_all_gsr','cpac_default_all','same'], # GSR vs no GSR
    # CCS vs fMRIPrep
    ['cpac_ccs_all','cpac_fmriprep_all','same'], # no GSR vs no GSR
    ['cpac_ccs_all_gsr','cpac_fmriprep_all_gsr','same'], # GSR vs GSR
    ['cpac_ccs_all','cpac_fmriprep_all_gsr','same'], # no GSR vs GSR
    ['cpac_ccs_all_gsr','cpac_fmriprep_all','same'], # GSR vs no GSR
    # default vs fMRIPrep
    ['cpac_default_all','cpac_fmriprep_all','same'], # no GSR vs no GSR
    ['cpac_default_all_gsr','cpac_fmriprep_all_gsr','same'], # GSR vs GSR
    ['cpac_default_all','cpac_fmriprep_all_gsr','same'], # no GSR vs GSR
    ['cpac_default_all_gsr','cpac_fmriprep_all','same'], # GSR vs no GSR
    ### different scans, same pipelines ###
    # ABCD
    ['cpac_abcd_all','cpac_abcd_all','different'], # no GSR vs no GSR
    ['cpac_abcd_all_gsr','cpac_abcd_all_gsr','different'], # GSR vs GSR
    ['cpac_abcd_all','cpac_abcd_all_gsr','different'], # no GSR vs GSR
    # CCS
    ['cpac_ccs_all','cpac_ccs_all','different'], # no GSR vs no GSR
    ['cpac_ccs_all_gsr','cpac_ccs_all_gsr','different'], # GSR vs GSR
    ['cpac_ccs_all','cpac_ccs_all_gsr','different'], # no GSR vs GSR
    # default
    ['cpac_default_all','cpac_default_all','different'], # no GSR vs no GSR
    ['cpac_default_all_gsr','cpac_default_all_gsr','different'], # GSR vs GSR
    ['cpac_default_all','cpac_default_all_gsr','different'], # no GSR vs GSR
    # fMRIPrep
    ['cpac_fmriprep_all','cpac_fmriprep_all','different'], # no GSR vs no GSR
    ['cpac_fmriprep_all_gsr','cpac_fmriprep_all_gsr','different'], # GSR vs GSR
    ['cpac_fmriprep_all','cpac_fmriprep_all_gsr','different'], # no GSR vs GSR
    ### different scans, different pipelines ###
    # ABCD vs CCS
    ['cpac_abcd_all','cpac_ccs_all','different'], # no GSR vs no GSR
    ['cpac_abcd_all_gsr','cpac_ccs_all_gsr','different'], # GSR vs GSR
    ['cpac_abcd_all','cpac_ccs_all_gsr','different'], # no GSR vs GSR
    ['cpac_abcd_all_gsr','cpac_ccs_all','different'], # GSR vs no GSR
    # ABCD vs default
    ['cpac_abcd_all','cpac_default_all','different'], # no GSR vs no GSR
    ['cpac_abcd_all_gsr','cpac_default_all_gsr','different'], # GSR vs GSR
    ['cpac_abcd_all','cpac_default_all_gsr','different'], # no GSR vs GSR
    ['cpac_abcd_all_gsr','cpac_default_all','different'], # GSR vs no GSR
    # ABCD vs fMRIPrep
    ['cpac_abcd_all','cpac_fmriprep_all','different'], # no GSR vs no GSR
    ['cpac_abcd_all_gsr','cpac_fmriprep_all_gsr','different'], # GSR vs GSR
    ['cpac_abcd_all','cpac_fmriprep_all_gsr','different'], # no GSR vs GSR
    ['cpac_abcd_all_gsr','cpac_fmriprep_all','different'], # GSR vs no GSR
    # CCS vs default
    ['cpac_ccs_all','cpac_default_all','different'], # no GSR vs no GSR
    ['cpac_ccs_all_gsr','cpac_default_all_gsr','different'], # GSR vs GSR
    ['cpac_ccs_all','cpac_default_all_gsr','different'], # no GSR vs GSR
    ['cpac_ccs_all_gsr','cpac_default_all','different'], # GSR vs no GSR
    # CCS vs fMRIPrep
    ['cpac_ccs_all','cpac_fmriprep_all','different'], # no GSR vs no GSR
    ['cpac_ccs_all_gsr','cpac_fmriprep_all_gsr','different'], # GSR vs GSR
    ['cpac_ccs_all','cpac_fmriprep_all_gsr','different'], # no GSR vs GSR
    ['cpac_ccs_all_gsr','cpac_fmriprep_all','different'], # GSR vs no GSR
    # default vs fMRIPrep
    ['cpac_default_all','cpac_fmriprep_all','different'], # no GSR vs no GSR
    ['cpac_default_all_gsr','cpac_fmriprep_all_gsr','different'], # GSR vs GSR
    ['cpac_default_all','cpac_fmriprep_all_gsr','different'], # no GSR vs GSR
    ['cpac_default_all_gsr','cpac_fmriprep_all','different'], # GSR vs no GSR
    ]

# fc_handle='Ranking'
fc_handle=''
corr_type='pearson'
simpleplot=False
atlases=['200',]
bootstrapping_ci=False
bootstrapping_average=False
base='/ROI'

allpl=sum(pipelines_list, [])
allpl=list(dict.fromkeys(allpl))
allpl.remove('same')    
allpl.remove('different')

for ppp in allpl:
    for f in os.listdir(base + '/ROI_Schaefer200/' + ppp):
        file=base + '/ROI_Schaefer200/' + ppp + '/' + f
        print(file)
        print(ppp+''+f.replace('.1D','').replace('sub-00',''))
        locals()[ppp+''+f.replace('.1D','').replace('sub-00','')]=np.genfromtxt(file)

# this is the name change for the final plot.
namechangedict={'cpac_default_all':'CPAC:Default',
            'cpac_fmriprep_all':'CPAC:fMRIPrep',
            'cpac_abcd_all':'CPAC:ABCD',
            'cpac_ccs_all':'CPAC:CCS',
            'cpac_default_all_gsr':'CPAC:Default(GSR)',
            'cpac_fmriprep_all_gsr':'CPAC:fMRIPrep(GSR)',
            'cpac_abcd_all_gsr':'CPAC:ABCD(GSR)',
            'cpac_ccs_all_gsr':'CPAC:CCS(GSR)',
            }

spatial_corr_plot(base,base.replace('ROI','figures'),pipelines_list,atlases,namechangedict,fc_handle,simpleplot,'pearson')
spatial_corr_plot(base,base.replace('ROI','figures'),pipelines_list,atlases,namechangedict,fc_handle,simpleplot,'concordance')
spatial_corr_plot(base,base.replace('ROI','figures'),pipelines_list,atlases,namechangedict,fc_handle,simpleplot,'spearman')