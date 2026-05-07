# Ontario Large Buildings Energy & Water Validation Report
**Author:** Eric Workman
**Purpose:** To create a script to find discrepancies in utilities data from my province.

# Clean.py
The data I downloaded from the ontario.ca website came in an excel file with a mixture of numeric and string values in some of columns. The null values were also represented with strings "Not Available". This script formats the data and exports it to a clean data file.

# Validate.py
A series of checks on logical contradictions that could warrant investigation or connote logging or miscalculation errors in the data.

# How to Run
1. place the excel file into the same folder as the scripts
2. run clean.py first to format the data
3. run validate.py to generate a printed summary, a csv file output of the summary and also csv files of all flagged rows

# Headers

## ID columns
EWRB_ID — unique ID for each building in the registry

City, Postal_Code — location

PrimPropTypCalc, PrimPropTypSelf, Largest_PropTyp, All_Prop_Types — what kind of building it is, from different sources. Calc is calculated, Self is self-reported

## Certification

Thrd_Party_Cert — whether a third party engineer certified the data

Ener_Star_Score — Energy Star rating 1-100, higher is more efficient

Ener_Star_Certs — whether the building has an Energy Star certificate

## Electricity (Int = Intensity, meaning per square metre)

WN_Sit_Elc_Int1 — electricity intensity in metric units (kWh/m^2)

WN_Sit_Elc_Int2 — same but in imperial units (kBtu/ft^2)

## Gas

WN_Sit_Gas_Int1/2/3 — natural gas intensity in different units

## Water

All_Water_Int1/2 — total site water intensity

Ind_Water_Int1/2 — individual unit water intensity, requires sub-metering

## Energy Use Intensity (EUI) — measures overall energy efficiency

Site_EUI1/2 — total energy used at the site per square metre/foot
Source_EUI1/2 — accounts for energy lost in generation and transmission, more complete picture
WN_Site_EUI1/2 — weather normalized version, adjusts for how cold or hot that year was
WN_Source_EUI1/2 — weather normalized source EUI

## Greenhouse Gas

GHG_Emiss_Int1/2 — carbon emissions per square metre/foot

## Data quality

Data_Qual_Check — Yes/No whether the record passed a quality check
Data_Qual_Date — when that check happened

# Findings Summary

VALIDATION REPORT — Ontario Large Buildings Energy & Water

Total records checked: 6739

CHECK: Missing primary energy data (Site_EUI1)
Severity: High
Records failed: 360
Note: Buildings with no Site_EUI1 value are missing their core energy metric.

CHECK: Zero or negative Site_EUI1 value
Severity: High
Records failed: 5
Note: A building reporting zero or negative energy use warrants investigation.

CHECK: Energy Star Score outside valid range (1-100)
Severity: Medium
Records failed: 43
Note: Energy Star scores must be between 1 and 100.

CHECK: Site_EUI1 and Site_EUI2 null mismatch
Severity: Medium
Records failed: 0
Note: These columns are the same measurement in metric and imperial. Nulls should match.

CHECK: Data quality check passed but no date recorded
Severity: Low
Records failed: 0
Note: A record marked as quality checked should always have a corresponding date.

CHECK: Energy data present but GHG emissions missing
Severity: Medium
Records failed: 0
Note: Buildings with energy data should also have greenhouse gas emissions calculated.

CHECK: source usage lower than site usage
Severity: Medium
Records failed: 0
Note: Buildings with source energy data lower than site data is almost definitely an error


# Data Source
https://data.ontario.ca/dataset/energy-and-water-usage-of-large-buildings-in-ontario/resource/aeb34aef-5029-4b65-8093-c86ad682b037

