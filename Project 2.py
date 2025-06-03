import pandas as pd

# ———————— 配置 ————————
file_path = "Supply_Tables_1997-2023_Summary.xlsx"

# BEA Supply 表格里真正表示“Total/汇总”的 NAICS code，需要删除
totals_to_remove = [
    'T001', 'T002', 'T003', 'T004', 'T005', 'T006',
    'T007', 'T008', 'T009', 'T010', 'T011',
    'T012', 'T013', 'T014', 'T015', 'T016', 'T017'
]

# 用于检测 “Total/SUM/All industries” 的关键词（不包含 special 列名）
summary_keywords = ['total', 'sum', 'all industries']

# ———————— 开始清洗 ————————
excel_obj = pd.ExcelFile(file_path)
sheet_names = excel_obj.sheet_names

main_data = []
naics_data = []

for sheet in sheet_names:
    year = int(sheet)
    df = pd.read_excel(file_path, sheet_name=sheet, skiprows=5)

    # 第一列为 commodity，第二列为 description
    df.rename(columns={df.columns[0]: 'commodity', df.columns[1]: 'description'}, inplace=True)
    # 删除用于二次表头的行（如 IOCode）
    df = df[df['commodity'] != 'IOCode']

    # 保存 naics code + description
    naics_subset = df[['commodity', 'description']].dropna().drop_duplicates()
    naics_data.append(naics_subset)

    # ———— 删除真正意义上的 “Total/SUM” 行（commodity 端） ————
    # 1) 删除 NAICS code 属于 totals_to_remove 的行
    df = df[~df['commodity'].isin(totals_to_remove)]
    # 2) 删除 commodity 或 description 中含 “total”/“sum”/“all industries” 的行
    df = df[~df['commodity'].str.contains(r'(?i)total|sum|all industries', na=False)]
    df = df[~df['description'].str.contains(r'(?i)total|sum|all industries', na=False)]

    # ———— 删除真正意义上的 “Total/SUM” 列（industry 端） ————
    # 先找出要 Drop 掉的列名（从第三列开始才是 industry）
    cols_to_drop = []
    for col in df.columns[2:]:
        lower_col = str(col).lower()
        if any(keyword in lower_col for keyword in summary_keywords):
            cols_to_drop.append(col)
        # 同时，如果列名刚好是某个 totals_to_remove，也删掉
        if str(col) in totals_to_remove:
            cols_to_drop.append(col)
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)

    # ———— 处理占位符与空值 ————
    df.replace(["...", "....", "-"], pd.NA, inplace=True)
    # 删除从第三列开始如果全是空值的行
    df = df.dropna(how='all', subset=df.columns[2:])

    # ———— 将宽表转换成长表 ————
    df_long = df.melt(
        id_vars=['commodity', 'description'],
        var_name='industry',
        value_name='value'
    )
    df_long['value'] = pd.to_numeric(df_long['value'], errors='coerce')
    df_long['year'] = year

    # ———— 删除 Long 表里 industry 端的 Total/汇总 NAICS code ———
    df_long = df_long[~df_long['industry'].isin(totals_to_remove)]
    # 再次删除 industry 中含 “total”/“sum”/“all industries” 的行
    df_long = df_long[~df_long['industry'].str.contains(r'(?i)total|sum|all industries', na=False)]

    main_data.append(df_long)

# 合并所有年份的数据
data_cleaned = pd.concat(main_data, ignore_index=True)

# 合并并去重所有 naics code + description
naics_cleaned = pd.concat(naics_data, ignore_index=True)
naics_cleaned = naics_cleaned.dropna().drop_duplicates().reset_index(drop=True)

# 保存成 CSV
data_cleaned.to_csv("supply_data_cleaned.csv", index=False)
naics_cleaned.to_csv("supply_naics_cleaned.csv", index=False)



# Part 2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 一定先读入清洗后的数据
df = pd.read_csv("supply_data_cleaned.csv", dtype={'commodity': str, 'industry': str})

# — 1. Special Indicators Over Time —
special_cols = ['MCIF', 'MADJ', 'Trade', 'Trans', 'MDTY', 'TOP', 'SUB']
df_spec = df[df['industry'].isin(special_cols)]
trend_spec = df_spec.groupby(['year', 'industry'])['value'].sum().unstack('industry').fillna(0)

plt.figure(figsize=(10, 5))
for col in special_cols:
    if col in trend_spec.columns:
        plt.plot(
            trend_spec.index,
            trend_spec[col] / 1_000_000,   # 换算成 Million USD
            marker='o',
            label=col
        )
plt.title("Special Economic Indicators Over Time")
plt.xlabel("Year")
plt.ylabel("Total Value (Millions USD)")
plt.legend(title="Indicator", bbox_to_anchor=(1.02, 1), loc='upper left')
plt.grid(linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("Special_Indicators_Over_Time.png")
plt.show()


# — 2. Top 5 Commodities Over Time —
df_comm_trend = df.groupby(['year', 'commodity'])['value'].sum().unstack('commodity').fillna(0)
commodity_totals = df_comm_trend.sum(axis=0).sort_values(ascending=False)
top5_coms = commodity_totals.index[:5].tolist()

plt.figure(figsize=(10, 5))
for com in top5_coms:
    plt.plot(
        df_comm_trend.index,
        df_comm_trend[com] / 1_000_000,
        marker='o',
        label=com
    )
plt.title("Top 5 Commodities Over Time")
plt.xlabel("Year")
plt.ylabel("Total Value (Millions USD)")
plt.legend(title="Commodity", bbox_to_anchor=(1.02, 1), loc='upper left')
plt.grid(linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("Top5_Commodities_Over_Time.png")
plt.show()


# — 3. Top 5 Industries Over Time —
df_ind_trend = df.groupby(['year', 'industry'])['value'].sum().unstack('industry').fillna(0)
industry_totals = df_ind_trend.sum(axis=0).sort_values(ascending=False)
top5_inds = industry_totals.index[:5].tolist()

plt.figure(figsize=(10, 5))
for ind in top5_inds:
    plt.plot(
        df_ind_trend.index,
        df_ind_trend[ind] / 1_000_000,
        marker='o',
        label=ind
    )
plt.title("Top 5 Industries Over Time")
plt.xlabel("Year")
plt.ylabel("Total Value (Millions USD)")
plt.legend(title="Industry", bbox_to_anchor=(1.02, 1), loc='upper left')
plt.grid(linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("Top5_Industries_Over_Time.png")
plt.show()


# — 4. Total Supply Value Over Time —
total_trend = df.groupby('year')['value'].sum()
plt.figure(figsize=(10, 5))
plt.plot(
    total_trend.index,
    total_trend.values / 1_000_000,
    marker='o',
    color='tab:blue'
)
plt.title("Total Supply Value Over Time")
plt.xlabel("Year")
plt.ylabel("Total Value (Millions USD)")
plt.grid(linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("Total_Supply_Value_Over_Time.png")
plt.show()
