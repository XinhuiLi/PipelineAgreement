# Pipeline Harmonization

Resources for pipeline harmonization paper

### Data Running

The [`config`](config) folder contains C-PAC pipeline configuration files

- [`minimal`](config/minimal): pipeline configuration files for minimal preprocessing

- [`fig4`](config/fig4): pipeline configuration files for Fig. 4

- [`figs3`](config/figs3): pipeline configuration file for Fig. S3

To run C-PAC Docker container, use the command below:
```
docker run \
-v <local data directory>:/bids_dataset \
-v <local output directory>:/outputs \
-v /tmp:/scratch \
fcpindi/c-pac:release-v1.8.1 /bids_dataset /outputs participant \
--pipeline_file <pipeline configuration file> \
--save_working_dir
```

Replace `<local data directory>` and `<local output directory>` to your local directories, and replace `<pipeline configuration file>` to your pipeline configuration file path such as `/outputs/default_pipeline.yml`. For more details, please check C-PAC user documentation: https://fcp-indi.github.io/


### Visualization

The [`figure`](figure) folder contains code to plot figures in the paper

Before running:

1. Update [`.pipelineharmonizationrc`](.pipelineharmonizationrc) with the applicable paths for your data.

2. Run `source .pipelineharmonizationrc` before running any scripts.

3. Run scripts (and IDEs like RStudio or Jupyter) from a terminal in which you've sourced [`.pipelineharmonizationrc`](.pipelineharmonizationrc)

#### Figure 1

- Update [`extract_ROI.sh`](figure/1/extract_ROI.sh) to create soft links for functional timeseries and run 3dROIstats

- Run [`run_ICC.sh`](figure/1/run_ICC.sh)
    - Results will be saved in the folder `All_new_ICC_Schaefer200/600/1000_aggreg`

- Organize folders as below

```
/root
└── figures
    └── ICC_Schaefer200
        ├── pipeline1_pipeline2.csv
        └── ...
    └── ICC_Schaefer600
    └── ICC_Schaefer1000
└── ROI
    └── ROI_Schaefer200
        ├── pipeline1
        └── pipeline2
        └── ...
    └── ROI_Schaefer600
    └── ROI_Schaefer1000
```

- Plot Fig. 1 using [`plot_fig1.py`](figure/1/plot_fig1.py)

#### Figure 2

- Plot Fig. 2 using [`plot_fig2.py`](figure/2/plot_fig2.py)

#### Figure 3

- Extract ROI
```
bash figure/3/extract_ROI.sh
```

- Save the data for calculating ICC and I2C2
```
python3.8 figure/3/run_ICC.py 
```

Outputs will be saved in a folder called `Data_ICC_1000_All_pearson` (60x19k matrix)

```
bash figure/3/run_ICC_I2C2.sh
```

Outputs will be saved in a folder called `ICC_1000_All_pearson` (19k matrix)

- Plot Fig. 3A using [`plot_fig3_time.py`](figure/3/plot_fig3_time.py) and [`plot_fig3_gsr.py`](figure/3/plot_fig3_gsr.py)

- Plot Fig. 3B using [`plot_fig3_time.py`](figure/3/plot_fig3_time.py) and [`plot_fig3_gsr.py`](figure/3/plot_fig3_gsr.py)

#### Figure 4

- Run [`extract_ROI.py`](figure/4/extract_ROI.py)

- Run [`corr.py`](figure/4/corr.py) and [`corr_harm.py`](figure/4/corr_harm.py) to generate Pearson correlation

- Plot Fig. 4 using [`plot_fig4.ipynb`](figure/4/plot_fig4.ipynb)

Notes: The [`post-processing`](figure/4/post-processing) folder for extra processing for several runs

#### Figure 5

- Plot Fig. 5 using [`plot_fig5.py`](figure/5/plot_fig5.py)

#### Supplementary Figure 1

- Run [`ccs_postproc.sh`](figure/s1/ccs_postproc.sh) and [`fmriprep_postproc.sh`](figure/s1/fmriprep_postproc.sh) to generate intermediate files for comparison

- Run [`abcd.py`](figure/s1/abcd.py)/[`ccs.py`](figure/s1/ccs.py)/[`fmriprep.py`](figure/s1/fmriprep.py) to generate correlation

- Plot Fig. S1 using [`plot_figs1.ipynb`](figure/1/plot_figs1.ipynb)

#### Supplementary Figure 2

- Run [`corr_fd.py`](figure/s2/corr_fd.py) to calculate FD correlation

- Plot Fig. S2 using [`plot_figs2.ipynb`](figure/s2/plot_figs2.ipynb)

#### Supplementary Figure 3

- Plot Fig. S3 using [`plot_figs3.py`](figure/s3/plot_figs3.py)

#### Supplementary Figure 4

- Plot Fig. S4 using [`plot_figs4.py`](figure/s4/plot_figs4.py)

#### Supplementary Figure 5

- Run [`corr_vol_ts.py`](figure/s5/corr_vol_ts.py) to get voxel-wise timeseries correlation


Contributors: [Xinhui Li](https://github.com/XinhuiLi), [Lei Ai](https://github.com/hahaai)

Acknowledgment: Thank [Jon Clucas](https://github.com/shnizzedy) for code review and [Anibal Sólon](https://github.com/anibalsolon) for technical support.