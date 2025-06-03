import pandas as pd



# Did you check your output? The value column has non-values in it. You want
# that column to be numeric. 
#
# You want the years to be integers, not strings. Think about making a graph but
# only using the years after 2020. Hard with strings.
#
# You don't have any 111CA (framing) commodities. This is really bad as it's 
# (perhaps) the most important commodity in the US economy. That's why it's first.
#
# I recommend dropping any totals. They are useful to ensure you've loaded the data
# correctly (even though they don't always add up  perfectly), but they'll skew
# the data in any graphs you make.
#
# Your code structure is very good. Should be easy to debug.
#
# Your naics codes are just the commodities (and value added). You also want the 
# sectors, which include final demand (the far right of the table). 



# Process a single year's sheet into long format
def load_single_sheet(sheet, year):
    df_raw = sheet.iloc[7:, 1:]
    df_raw.columns = sheet.iloc[6, 1:]
    df_raw.index = sheet.iloc[7:, 0]

    df_long = df_raw.reset_index().melt(id_vars=df_raw.index.name, var_name="industry", value_name="value")
    df_long.columns = ["commodity", "industry", "value"]
    df_long["year"] = year
    df_long["value"] = df_long["value"].fillna(0)

    return df_long


# Extract NAICS code and descriptions from first sheet
def extract_naics_descriptions(sheet):
    naics_codes = sheet.iloc[7:, 0]
    descriptions = sheet.iloc[7:, 1]
    df_naics = pd.DataFrame({
        "naics code": naics_codes,
        "description": descriptions
    })
    df_naics = df_naics.dropna().drop_duplicates()
    df_naics["naics code"] = df_naics["naics code"].astype(str).str.strip()
    return df_naics


# Read and process all years from the Excel file
def process_all_sheets(file_path):
    xl = pd.ExcelFile(file_path)
    all_data = []
    for year in xl.sheet_names:
        sheet = xl.parse(sheet_name=year)
        df = load_single_sheet(sheet, year)
        all_data.append(df)
    df_all = pd.concat(all_data, ignore_index=True)
    df_naics = extract_naics_descriptions(xl.parse(xl.sheet_names[0]))
    return df_all, df_naics


# Run the script
if __name__ == "__main__":
    file_path = "/Users/wenshi/Library/Mobile Documents/com~apple~CloudDocs/Study/UW Madison/AAE 718/Use_Tables_Supply-Use_Framework_1997-2023_Summary.xlsx"
    df_main, df_naics = process_all_sheets(file_path)

    # Preview output
    print(df_main.head())
    print(df_naics.head())

    # Optionally save results (comment out if not needed)
    df_main.to_csv("use_table_long.csv", index=False)
    df_naics.to_csv("naics_descriptions.csv", index=False)
