# Data notes

`new_data.csv` contains the historical daily return series used for asset-level analytics, portfolio construction and simulation inputs.

The available history differs by instrument. Asset correlations therefore use pairwise available observations, while portfolio analysis uses the data handling defined in the Python workflow.

The dataset is included to make the analysis and website exhibits reproducible. See `config_file.py` for the mapping between data columns and portfolio holdings.
