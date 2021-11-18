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

def cal_corr(path1, path2, run):
    print(run)
    sc = []
    for sub in range(27, 57):
        if sub == 30:
            continue
        corr1 = get_corr(path1, sub)
        corr2 = get_corr(path2, sub)
        x = np.isnan(corr1) | np.isnan(corr2)
        corr1_new = corr1[~x]
        corr2_new = corr2[~x]
        sc.append(np.corrcoef(corr1_new,corr2_new)[0,1])
    np.save(os.path.join(out_path, run+'.npy'), sc)

root_path = f'{os.environ.get("BASEFOLDER")}/ROI/ROI_Schaefer200'
out_path = f'{os.environ.get("LOCAL_ROOT")}/figure/4/PearsonCorr'

# ABCD
path1 = root_path + 'ABCD'
path2 = root_path + 'cpac_abcd_v1.8'
cal_corr(path1, path2, 'baseline_abcd-cpac_abcd')

# CCS
path1 = root_path + 'ccs'
path2 = root_path + 'cpac_ccs_v1.8'
cal_corr(path1, path2, 'baseline_ccs-cpac_ccs')

# fMRIPrep
path1 = root_path + 'fmriprep_default'
path2 = root_path + 'cpac_fmriprep_v1.8'
cal_corr(path1, path2, 'baseline_fmriprep-cpac_fmriprep')