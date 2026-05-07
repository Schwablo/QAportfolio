import pandas as pd

# Load the cleaned data
df = pd.read_csv("cleaned_data.csv")

findings = []

# CHECK 1 - Missing a core energy data value
# Site_EUI1 is the primary energy metric. Missing means the building has no valid energy record.

missing_eui = df[df["Site_EUI1"].isnull()] #look for every empty primary EUI
findings.append({
    "check": "Missing primary energy data (Site_EUI1)",
    "severity": "High",
    "count": len(missing_eui),
    "note": "Buildings with no Site_EUI1 value are missing their core energy metric."
})

# CHECK 2 - Zero or negative energy values
# A building cannot use zero or negative energy. These could be data entry errors or perhaps vacant properties?.
zero_or_negative = df[(df["Site_EUI1"].notnull()) & (df["Site_EUI1"] <= 0)]
findings.append({
    "check": "Zero or negative Site_EUI1 value",
    "severity": "High",
    "count": len(zero_or_negative),
    "note": "A building reporting zero or negative energy use warrants investigation."
})

# CHECK 3 - Energy Star Score out of valid range
# Valid scores are 1 to 100. Anything outside that range is invalid.
invalid_score = df[(df["Ener_Star_Score"].notnull()) & ((df["Ener_Star_Score"] < 1) | (df["Ener_Star_Score"] > 100))]
findings.append({
    "check": "Energy Star Score outside valid range (1-100)",
    "severity": "Medium",
    "count": len(invalid_score),
    "note": "Energy Star scores must be between 1 and 100."
})

# CHECK 4 - Metric and imperial columns mismatched
# Site_EUI1 and Site_EUI2 are the same measurement in Metric and Imperial respectively.
# If one is null the other should be too. A mismatch means something went wrong.
mismatched_eui = df[df["Site_EUI1"].isnull() != df["Site_EUI2"].isnull()]
findings.append({
    "check": "Site_EUI1 and Site_EUI2 null mismatch",
    "severity": "Medium",
    "count": len(mismatched_eui),
    "note": "These columns are the same measurement in metric and imperial. Nulls should match."
})

# CHECK 5 - Data quality passed but no date recorded
# If Data_Qual_Check is Yes, there should be a timestamp.
qual_no_date = df[(df["Data_Qual_Check"] == "Yes") & (df["Data_Qual_Date"].isnull())]
findings.append({
    "check": "Data quality check passed but no date recorded",
    "severity": "Low",
    "count": len(qual_no_date),
    "note": "A record marked as quality checked should always have a corresponding date."
})

# CHECK 6 - Energy data present but no GHG emissions
# If a building has energy data it should have emissions data too.
energy_no_ghg = df[(df["Site_EUI1"].notnull()) & (df["GHG_Emiss_Int1"].isnull())]
findings.append({
    "check": "Energy data present but GHG emissions missing",
    "severity": "Medium",
    "count": len(energy_no_ghg),
    "note": "Buildings with energy data should also have greenhouse gas emissions calculated."
})

# CHECK 7 - Source EUI lower than Site EUI
# source EUI is all energy including the site EUI, it shouldn't be lower in most all circumstances.
source_eui = df[(df["Source_EUI1"].notnull()) & (df["Site_EUI1"].notnull()) & (df["Source_EUI1"] < df["Site_EUI1"])]
findings.append({
    "check": "source usage lower than site usage",
    "severity": "Medium",
    "count": len(source_eui),
    "note": "Buildings with source energy data lower than site data is almost definitely an error."

})

# Print findings report
print("=" * 60)
print("VALIDATION REPORT — Ontario Large Buildings Energy & Water")
print("=" * 60)
print(f"Total records checked: {len(df)}\n")

for f in findings:
    print(f"CHECK: {f['check']}")
    print(f"Severity: {f['severity']}")
    print(f"Records failed: {f['count']}")
    print(f"Note: {f['note']}")
    print("-" * 60)

#export of the findings summary
findings_df = pd.DataFrame(findings)
findings_df.to_csv("findings_summary.csv", index=False)
print("\nFindings Summary exported to findings_summary.csv")

# CSV files showing the records that were found for eack check
verbose_logs = {
    "missing_eui": missing_eui,
    "zero_or_negative": zero_or_negative,
    "invalid_score": invalid_score,
    "mismatched_eui": mismatched_eui,
    "qual_no_date": qual_no_date,
    "energy_no_ghg": energy_no_ghg,
    "source_eui": source_eui
}

for name, data in verbose_logs.items():
    if len(data) > 0:
        data.to_csv(f"verbose_{name}.csv", index=False)
        print(f"Verbose log exported: verbose_{name}.csv ({len(data)} records)")
    else:
        print(f"No failures for: {name} - no log generated")