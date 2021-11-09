# Pipeline Harmonization

Resources for pipeline harmonization paper

### Data Running

The `config` folder contains all pipeline configuration files

- minimal: pipeline configuration files for minimal preprocessing

- fig4: pipeline configuration files for Fig. 4

- figs3: pipeline configuration file for Fig. S3

### Visualization

#### Figure 1

- Update extract_ROI.sh to create soft links for functional timeseries and run 3dROIstats

- Update and run run_ICC_part1.sh

- Run run_ICC_part2.sh
    - Results will be saved in the folder All_new_ICC_Schaefer200/600/1000_aggreg

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

- Plot Fig. 1 using plot_fig1.py

#### Figure 2

- Plot Fig. 2 using plot_fig2.py

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

- Plot Fig. 3A using plot_fig3_time.py and plot_fig3_time.py

- Plot Fig. 3B using plot_fig3_time.py and plot_fig3_gsr.py

#### Figure 4

- Run extract_ROI.py

- Run corr.py and corr_harm.py to generate Pearson correlation

- Plot Fig. 4 using plot_fig4.ipynb

Notes: The `post-processing` folder for extra processing for several runs

#### Figure 5

- Plot Fig. 5 using plot_fig5.py

Notes: The `post-processing` folder for extra processing for several runs

#### Supplementary Figure 1

- Run ccs_postproc.sh and fmriprep_postproc.sh to generate intermediate files for comparison

- Run abcd.py/ccs.py/fmriprep.py to generate correlation

- Plot Fig. S1 using plot_figs1.ipynb

#### Supplementary Figure 2

- Run corr_fd.py to calculate FD correlation

- Plot Fig. S2 using plot_figs2.ipynb

#### Supplementary Figure 3

- Plot Fig. S3 using plot_figs3.py

#### Supplementary Figure 4

- Plot Fig. S4 using plot_figs4.py


Contributors: Xinhui Li, Lei Ai