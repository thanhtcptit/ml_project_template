{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}

Project Organization
------------

The directory structure of your new project looks like this: 

```
├── configs                     <- Store experiment config files
│
├── data
│   ├── external                <- Data from third party sources
│   ├── interim                 <- Intermediate data that has been transformed
│   ├── processed               <- The final, canonical data sets for modeling
│   └── raw                     <- The original, immutable data dump
│   
├── train_logs                  <- Trained and serialized models, model predictions, or model summaries
│   
├── notebooks                   <- Jupyter notebooks. Naming convention is a number (for ordering),
│                                  the creator's initials, and a short `-` delimited description, e.g.
│                                  `1.0-jqp-initial-data-exploration`
│
├── references                  <- Data dictionaries, manuals, and all other explanatory materials
│   
├── reports                     <- Generated analysis as HTML, PDF, LaTeX, etc
│   └── figures                 <- Generated graphics and figures to be used in reporting
│
├── scripts                     <- Scripts like bash, shell, ...
│  
├── src                         <- Source code for use in this project.
│   ├── __init__.py
│   ├── evaluate.py
│   ├── train.py
│   │
│   ├── data                    <- Scripts to download or generate data
│   │
│   ├── features                <- Scripts to turn raw data into features for modeling
│   │
│   ├── models                  <- Scripts to define models
│   │   └── base.py
│   │
│   ├── utils                   <- Scripts to define helper function
│   │
│   └── visualization           <- Scripts to create exploratory and results oriented visualizations
│
├── LICENSE
│
├── README.md                   <- The top-level README for developers using this project
│
├── requirements.txt            <- The requirements file for reproducing the analysis environment, e.g.
│                                  generated with `pip freeze > requirements.txt`
└── run.py                      <- Script to run tasks
│   
├── setup.py                    <- Makes project pip installable (pip install -e .) so src can be imported
```
