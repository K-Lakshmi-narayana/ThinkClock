# NASA Battery Dataset Analysis

This project analyzes the NASA Battery Dataset, which includes charge/discharge and impedance measurements of Li-ion batteries over multiple cycles at various temperatures. The dataset provides insights into battery aging and internal parameters such as impedance, electrolyte resistance (`Re`), and charge transfer resistance (`Rct`). The analysis is done using `Plotly` to visualize the changes in these parameters over the battery cycles.

## Prerequisites

Before running this code, ensure you have the following installed:

- Python 3.x
- Pandas
- NumPy
- Plotly
- tqdm

You can install these dependencies using `pip`:

```bash
pip install pandas numpy plotly tqdm
```

## Dataset
The dataset can be downloaded from Kaggle - NASA Battery Dataset.

The dataset contains the following files:

metadata.csv: Contains metadata for each battery test, including file paths, battery IDs, and other essential information.
charge_discharge (CSV files): Contains charge/discharge cycle data for each test.
impedance (CSV files): Contains impedance measurement data, including complex impedance values at various frequencies (0.1 Hz to 5 kHz).

### Folder Structure
The dataset should be organized as follows:

```bash
think_clock.py        # Main Python script for data processing and visualization 
cleaned_dataset/          
├── data/                 # Folder containing charge/discharge and impedance CSV files
└── metadata.csv          # Metadata file describing the dataset
```

## How to Run
1. Place the cleaned_dataset folder (containing data and metadata.csv) in the thinkclock directory.
2. Run the think_clock.py file from the terminal:
   ```bash
   python think_clock.py
   ```
3. The script will generate interactive plots showing changes in battery parameters over cycles.

## Outputs

The following plots are generated:

1. Battery Impedance (Battery_impedance_real)
    -- How battery impedance evolves over cycles.
   
2. Electrolyte Resistance (Re)
    -- Visualizes changes in electrolyte resistance.
   
3. Charge Transfer Resistance (Rct)
    -- Shows how charge transfer resistance varies with battery aging.



