############################################################################################################################################################################
## load spatial correlaiotn and plot 
import os
import random
import numpy as np
import pandas as pd
import scipy.stats as st
import seaborn as sns
import matplotlib.pyplot as plt

axis_tick_size=17
lw_value=2
to_sum = False#True

for corr_type in ['pearson']:

    def plot_mean_and_CI(mean, lb, ub, color_mean=None, color_shading=None):
        # plot the shaded range of the confidence intervals
        plt.fill_between(range(len(mean)), ub, lb,
                         color=color_shading, alpha=.5)
        # plot the mean on top
        plt.plot(mean, color_mean)
        plt.show()

    def kde_scipy(x, x_grid, bandwidth=0.2, **kwargs):
        #x_grid = np.linspace(-4.5, 3.5, 1000)
        """Kernel Density Estimation with Scipy"""
        # Note that scipy weights its bandwidth by the covariance of the
        # input data.  To make the results comparable to the other methods,
        # we divide the bandwidth by the sample standard deviation here.
        kde = gaussian_kde(x, bw_method=bandwidth / x.std(ddof=1), **kwargs)
        return kde.evaluate(x_grid)

    # datain='/data3/cnl/fmriprep/Lei_working/testing/ICC_Scan_duration/All_sessions/figures/ICC_1000_All_' + corr_type
    datain='/Users/xinhui.li/Documents/reproducibility/XL/figure/3/ICC_1000_All_pearson_rank_eps'
    # datain='/Users/xinhui.li/Documents/reproducibility/XL/figure/3/ICC_1000_All_pearson_no_rank_eps'

    def re_sample(x,y,x_grid):
        y_out=np.linspace(0, 0, len(x_grid))

        stop=0
        for jj in range((len(x)-1)):
            for ii in range(len(x_grid)):
                grid=x_grid[ii]
                if grid >= x[jj] and grid <= x[jj+1]:
                    y_out[ii]=y[jj]
                if x[jj]== x[jj+1] and x[jj]==1 and stop == 0:
                    if grid >= x[jj]:
                        y_out[ii]=y[jj]  
                        stop=1
        return y_out
    
    num_pair=72
    num_rand_times=10
    
    binnum=2000
    # x_grid=np.linspace(0, 1.1, binnum) # TODO ask Lei: why?
    x_grid=np.linspace(0, 1, binnum)

    # combine different random runs together first.
    if to_sum:
        for pl in range(0,num_pair):
            print(pl)
            for ses in range(1,4):
                if os.path.isfile(datain+'/Random_All_Pipeline-'+str(pl)+'_Ses_'+str(ses)+'.txt'):
                    continue
                print('ses is ' + str(ses))
                print('Sum')
                # each is a single plot
                dataall = np.empty((num_rand_times,binnum))     

                for random_num in range(0,num_rand_times):
                    file=datain+'/Random-'+str(random_num)+'_Pipeline-'+str(pl)+'_Ses_'+str(ses)+'.txt'
                    if os.path.isfile(file):
                        data=np.loadtxt(file)
                        data=data[data>np.finfo(np.float32).eps]
                        # plt.cla()
                        pdf_tmp=sns.kdeplot(data,gridsize=200).get_lines()[0].get_data()
                        pdf=re_sample(pdf_tmp[0],pdf_tmp[1],x_grid)
                        #pdf=kde_scipy(data,x_grid,bandwidth=0.2)
                        dataall[random_num,:]=pdf

                np.savetxt(datain+'/Random_All_Pipeline-'+str(pl)+'_Ses_'+str(ses)+'.txt',dataall)

    ### same pipeline ###
    nrow = 2
    plt.cla()
    fig, axs = plt.subplots(nrow,3,figsize=(15, 3*nrow),sharex=True,sharey='row',dpi=600)

    same_pipe_same_scan_start_index = 0
    diff_pipe_same_scan_start_index = 12
    same_pipe_diff_scan_start_index = 36
    diff_pipe_diff_scan_start_index = 48

    same_pipe_lg = 12 # length
    same_pipe_itv = 3 # interval

    diff_pipe_lg = 24
    diff_pipe_itv = 4

    for row in range(nrow):
        '''
        # same session
        # no GSR vs no GSR
        if row == 0:
            pipelist = np.arange(same_pipe_same_scan_start_index, same_pipe_same_scan_start_index+same_pipe_lg, same_pipe_itv) # no GSR vs no GSR, same scan, same pipe, [0, 3, 6, 9]
        elif row == 1:
            pipelist = np.arange(diff_pipe_same_scan_start_index, diff_pipe_same_scan_start_index+diff_pipe_lg, diff_pipe_itv) # no GSR vs no GSR, same scan, diff pipe, [12, 16, 20, 24, 28, 32]
        '''
        # different session
        # no GSR vs no GSR
        if row == 0:
            pipelist = np.arange(same_pipe_diff_scan_start_index, same_pipe_diff_scan_start_index+same_pipe_lg, same_pipe_itv) # no GSR vs no GSR, diff scan, same pipe, [36, 39, 42, 45]
        elif row == 1:
            pipelist = np.arange(diff_pipe_diff_scan_start_index, diff_pipe_diff_scan_start_index+diff_pipe_lg, diff_pipe_itv) # no GSR vs no GSR, diff scan, diff pipe, [48, 52, 56, 60, 64, 68]
        
        for ses in range(1,4):
            for i in [0.6,0.8,0.9]:
                axs[row, (ses-1)].axvline(x=i, lw=lw_value, clip_on=False, color='lightgray')

        for num, pl in enumerate(pipelist):
            # set color
            if row in [0,2,4]:
                if num == 0:
                    color_plot=sns.color_palette("tab20c")[5] # abcd, orange
                if num == 1:
                    color_plot=sns.color_palette("tab20c")[9] # ccs, green
                if num == 2:
                    color_plot=sns.color_palette("tab20c")[1] # default, blue
                if num == 3:
                    color_plot=sns.color_palette("tab20c")[13] # fmriprep, purple
            else:
                if num == 0:
                    color_plot=sns.color_palette("Set3")[11] # abcd vs ccs, yellow
                if num == 1:
                    color_plot=sns.color_palette("tab20")[3] # abcd vs default, orange
                if num == 2:
                    color_plot=sns.color_palette("tab20")[7] # abcd vs fmriprep, red
                if num == 3:
                    color_plot=sns.color_palette("tab20")[5] # ccs vs default, green
                if num == 4:
                    color_plot=sns.color_palette("tab20")[1] # ccs vs fmriprep, blue
                if num == 5:
                    color_plot=sns.color_palette("tab20")[9] # default vs fmriprep, purple

            for ses in range(1,4):
                print('ses is ' + str(ses))
                dataall=np.loadtxt(datain+'/Random_All_Pipeline-'+str(pl)+'_Ses_'+str(ses)+'.txt')
                datamean=[]
                data_lb=[]
                data_up=[]
                for ii in range(0,dataall.shape[1]):
                    pdf=dataall[:,ii]
                    a,b=st.t.interval(0.95, len(pdf)-1, loc=np.mean(pdf), scale=st.sem(pdf))
                    if np.isnan(a):
                        a=0
                    if np.isnan(b):
                        b=0
                    data_lb.append(a)
                    data_up.append(b)
                    datamean.append(np.mean(pdf))

                axs[row, (ses-1)].fill_between(x_grid, data_lb, data_up, color=color_plot, alpha=0.8)
                axs[row, (ses-1)].plot(x_grid, datamean, linewidth=0.5, color='black')
                axs[row, (ses-1)].tick_params(axis='both', which='major', labelsize=axis_tick_size)

                axs[row, (ses-1)].set_ylim([-0.1,6]) # 5.2 for rank, 6 for no rank

                # add x ticks at last row
                if row == nrow-1:
                    axs[row, (ses-1)].set_xticks([x_grid[0], x_grid[int(0.6*binnum)], x_grid[int(0.8*binnum)], x_grid[int(0.9*binnum)]])
                    axs[row, (ses-1)].set_xticklabels(['0', '0.6', '0.8', '0.9'])

    plt.tight_layout()
    # plt.savefig('./Figure3_same_ses_time_nogsr-nogsr.png')
    plt.savefig('./Figure3_diff_ses_time_nogsr-nogsr.png')