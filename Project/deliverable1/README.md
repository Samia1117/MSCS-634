# MSCS 634 - Project Deliverable 1: Data Collection, Cleaning, and Exploration

## Dataset Summary

**Dataset:** [Telco Customer Churn](https://github.com/IBM/telco-customer-churn-on-icp4d) (IBM sample dataset)

7,043 customer records, 21 columns, covering a telecom company's customer demographics,
subscribed services (phone, internet, streaming, security add-ons), account/billing info
(contract type, payment method, monthly/total charges, tenure), and whether the customer churned.

This dataset was chosen because it mixes numeric and categorical attributes and naturally
supports all four project deliverables on the same data:
- **Regression (Deliverable 2):** predict `MonthlyCharges` from customer/service attributes.
- **Classification (Deliverable 3):** predict `Churn` (Yes/No).
- **Clustering (Deliverable 3):** segment customers by usage and billing behavior.
- **Association rule mining (Deliverable 3):** find frequent service/contract combinations
  associated with churn.

I was also personally interested in this dataset as I work as a software engineern in the 
wireless & semiconductor industry and am curious what the customer profile looks like for 
such industries. 

## Key Insights from Analysis

- **Churn is moderately imbalanced:** ~26.5% of customers churned vs. 73.5% retained. Future
  classification work will need F1/ROC-AUC rather than raw accuracy.
- **Tenure is bimodal:** lots of brand-new customers and lots of long-tenured (70+ month)
  customers, fewer in between.
- **`TotalCharges` is highly correlated with `tenure` (r ~ 0.83)**, since it's effectively a
  function of tenure and monthly charges. `MonthlyCharges` is the more independent, more useful
  regression target for Deliverable 2.
- **Churn is concentrated among month-to-month contracts, fiber optic internet customers, and
  electronic check payers.** These look like strong predictors for classification and good
  candidates for association rule mining.
- **No meaningful outliers** were found in `tenure`, `MonthlyCharges`, or `TotalCharges` via
  boxplot/IQR inspection.

## Data Cleaning Steps

1. **Missing values:** `TotalCharges` was loaded as text and had 11 blank entries. All 11 belong
   to customers with `tenure == 0` (brand-new customers who haven't been billed a full cycle yet).
   Converted the column to numeric and filled those 11 rows with `0`, rather than dropping them or
   imputing a mean, since a mean would misrepresent new customers as average ones.
2. **Duplicates:** checked for both fully duplicated rows and duplicated `customerID` values -
   none found.
3. **Noisy/inconsistent data:**
   - Dropped `customerID` (a unique identifier, not a predictive feature).
   - Recoded `SeniorCitizen` from `0`/`1` to `No`/`Yes` for consistency with the rest of the
     binary categorical fields.
   - Kept `"No internet service"` / `"No phone service"` as their own categories (rather than
     collapsing into `"No"`) since they carry real information about what the customer has
     subscribed to.
   - Sanity-checked numeric ranges for `tenure`, `MonthlyCharges`, `TotalCharges` - no negative or
     out-of-range values found.

## Exploratory Data Analysis

Performed with Seaborn/Matplotlib: churn class distribution, histograms of the three numeric
features, boxplots for outlier detection, churn rate by contract/internet service/payment method,
a correlation heatmap of numeric features, and a tenure-vs-monthly-charges scatter plot colored by
churn. See `Deliverable1.ipynb` for the full code, plots, and written interpretation under each
visualization.

## Challenges Encountered

- **Hidden missing data:** `TotalCharges` didn't show up as `NaN` in a basic `.isna()` check
  because the missing values were stored as blank strings inside an object/string column rather
  than true `NaN`s. This was caught by noticing the column's dtype was `object` instead of
  numeric, then coercing it and inspecting which rows failed to convert.
- **Deciding how to fill the missing `TotalCharges` values:** since all 11 missing rows had
  `tenure == 0`, a generic imputation strategy (mean/median) would have been misleading. Using
  domain reasoning (new customer -> $0 total charges so far) gave a more defensible fill value
  than a purely statistical one.
- **Deciding whether to collapse `"No internet service"` / `"No phone service"` into `"No"`:**
  chose to keep them distinct since later deliverables (classification, association rule mining)
  benefit from knowing *why* a service is "off" (no add-on chosen vs. no base service to add it to).

## Files

- `Deliverable1.ipynb` - full notebook (load, inspect, clean, EDA, insights).
- `data/Telco-Customer-Churn.csv` - the raw dataset.
- `README.md` - this file.
