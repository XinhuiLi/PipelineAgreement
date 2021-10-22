import os
import numpy as np

def upper_tri_indexing(A):
    m = A.shape[0]
    r,c = np.triu_indices(m,1)
    return A[r,c]

def get_corr(pathname, subid):
    filename = os.path.join(pathname, 'sub-00254'+str(subid)+'a.1D')
    data = np.genfromtxt(filename)
    data = data.transpose()
    data_corr = np.corrcoef(data)
    corr_tri = upper_tri_indexing(data_corr)
    return corr_tri

run_list = ['from_abcd_to_default', 'from_abcd_to_fmriprep', 'from_abcd_to_ccs', 'from_ccs_to_default', 'from_ccs_to_fmriprep', 'from_ccs_to_abcd', 'from_default_to_abcd', 'from_default_to_ccs', 'from_default_to_fmriprep', 'from_fmriprep_to_default', 'from_fmriprep_to_abcd', 'from_fmriprep_to_ccs']

for run in run_list:
    from_run = run.split('_')[1]
    to_run = run.split('_')[3]

    if from_run == 'default':
        path1 = '/data3/cnl/fmriprep/Lei_working/Finalizing/Minimal/ROI/ROI_Schaefer200/cpac_default_v1.8'
    elif from_run == 'fmriprep':
        path1 = '/data3/cnl/fmriprep/Lei_working/Finalizing/Minimal/ROI/ROI_Schaefer200/cpac_fmriprep_v1.8'
    elif from_run == 'abcd':
        path1 = '/data3/cnl/fmriprep/Lei_working/Finalizing/Minimal/ROI/ROI_Schaefer200/cpac_abcd_v1.8'
    elif from_run == 'ccs':
        path1 = '/data3/cnl/fmriprep/Lei_working/Finalizing/Minimal/ROI/ROI_Schaefer200/cpac_ccs_v1.8'

    if to_run == 'default':
        path2 = '/data3/cnl/fmriprep/Lei_working/Finalizing/Minimal/ROI/ROI_Schaefer200/cpac_default_v1.8'
    elif to_run == 'fmriprep':
        path2 = '/data3/cnl/fmriprep/Lei_working/Finalizing/Minimal/ROI/ROI_Schaefer200/cpac_fmriprep_v1.8'
    elif to_run == 'abcd':
        path2 = '/data3/cnl/fmriprep/Lei_working/Finalizing/Minimal/ROI/ROI_Schaefer200/cpac_abcd_v1.8'
    elif to_run == 'ccs':
        path2 = '/data3/cnl/fmriprep/Lei_working/Finalizing/Minimal/ROI/ROI_Schaefer200/cpac_ccs_v1.8'

    path_new = os.path.join('/data3/cnl/xli/reproducibility/analysis/ROI200', run)
    path_out = '/data3/cnl/xli/reproducibility/analysis/PearsonCorr'

    sc = []
    for sub in range(27, 57):
        if sub == 30:
            continue
        corr1 = get_corr(path2, sub)
        corr2 = get_corr(path1, sub)
        x = np.isnan(corr1) | np.isnan(corr2)
        corr1_new = corr1[~x]
        corr2_new = corr2[~x]
        sc.append(np.corrcoef(corr1_new,corr2_new)[0,1])
    np.save(os.path.join(path_out, run+'.npy'), sc)

    var_list = os.listdir(path_new)
    for var in var_list:
        print(run, var)
        path1 = os.path.join(path_new, var)
        sc = []
        for sub in range(27, 57):
            if sub == 30:
                continue
            if sub == 48 and 'from_abcd' in run and var == 'func_mask':
                continue
            corr1 = get_corr(path2, sub)
            corr2 = get_corr(path1, sub)
            x = np.isnan(corr1) | np.isnan(corr2)
            corr1_new = corr1[~x]
            corr2_new = corr2[~x]
            sc.append(np.corrcoef(corr1_new,corr2_new)[0,1])
        np.save(os.path.join(path_out, run+'-'+var+'.npy'), sc)