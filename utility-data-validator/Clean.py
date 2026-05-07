import pandas as pd

#loading my excel file
df = pd.read_excel("data.xlsx")

#list of all the columns that are numeric but came in mixed with strings
numeric_columns = [
    "WN_Sit_Elc_Int1", "WN_Sit_Elc_Int2",
    "WN_Sit_Gas_Int1", "WN_Sit_Gas_Int2", "WN_Sit_Gas_Int3",
    "All_Water_Int1", "All_Water_Int2",
    "Ind_Water_Int1", "Ind_Water_Int2",
    "Site_EUI1", "Site_EUI2",
    "Source_EUI1", "Source_EUI2",
    "WN_Site_EUI1", "WN_Site_EUI2",
    "WN_Source_EUI1", "WN_Source_EUI2",
    "Ener_Star_Score"
]

#loop the columns and convert the values to floats or otherwise null
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

#Replacing strings that indicate null to a real null
df = df.replace("Not Available", None)
df = df.replace("Not Available ", None)

#save the clean file
df.to_csv("cleaned_data.csv", index=False)

#printing results
print(df.isnull().sum().to_string())
print(f"Shape: {df.shape}")
print("\nNull counts after cleaning:")
print("clean complete")
