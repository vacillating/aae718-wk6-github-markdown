# Worksheet 03 Solutions - Pandas
import pandas as pd
import matplotlib.pyplot as plt
# Problem 1
def methane(filepath):
    df = pd.read_csv(filepath)
    df = df.drop(columns=['Unnamed: 0'])
    return df

# Problem 2
def methane_aggregation(filepath):
    df = methane(filepath)
    subset = df[(df['region'] != 'World') & (df['type'] == 'Agriculture')]
    non_world_sum = subset['emissions'].sum()
    world_row = df[(df['region'] == 'World') & (df['type'] == 'Agriculture')]
    world_total = world_row['emissions'].sum()
    return world_total - non_world_sum

# Problem 3
def problem_03(filepath):
    df = methane(filepath)
    subset = df[(df['region'] != 'World') & (df['type'] == 'Agriculture')]
    unique_segments = subset['segment'].unique()
    return unique_segments

# Problem 4
def region_mean(filepath):
    df = methane(filepath)
    region_avg = df.groupby('region')['emissions'].mean().reset_index()
    return region_avg

# Problem 5
def region_total_mean(filepath):
    df = methane(filepath)
    filtered = df[df['segment'] != 'Total']
    region_avg = filtered.groupby('region')['emissions'].mean().reset_index()
    return region_avg

#print(region_total_mean('/Users/wenshi/Library/Mobile Documents/com~apple~CloudDocs/Study/UW Madison/AAE 718/AAE 718 - Pycharm/Methane_final.csv'))

#Problem 6

def methane_graphs(filepath):
    df = methane(filepath)

    plt.figure(figsize=(10, 6))
    df.boxplot(column='emissions', by='region', vert=False)
    plt.title('Boxplot 1: Emissions by Region (All Data)')
    plt.suptitle('')
    plt.xlabel('Emissions')
    plt.savefig('plot1.png')

    df2 = df[df['region'] != 'World']
    plt.figure(figsize=(10, 6))
    df2.boxplot(column='emissions', by='region', vert=False)
    plt.title('Boxplot 2: Emissions by Region (Excluding World)')
    plt.suptitle('')
    plt.xlabel('Emissions')
    plt.savefig('plot2.png')

    df3 = df2[df2['segment'] == 'Total']
    plt.figure(figsize=(10, 6))
    df3.boxplot(column='emissions', by='region', vert=False)
    plt.title('Boxplot 3: Emissions by Region (Total Only, Excl. World)')
    plt.suptitle('')
    plt.xlabel('Emissions')
    plt.savefig('plot3.png')

    df4 = df2[df2['segment'] != 'Total']
    plt.figure(figsize=(10, 6))
    df4.boxplot(column='emissions', by='segment', vert=False)
    plt.title('Boxplot 4: Emissions by Segment (Excl. World and Total)')
    plt.suptitle('')
    plt.xlabel('Emissions')
    plt.savefig('plot4.png')

    df5 = df[(df['segment'] == 'Onshore oil') & (df['region'] != 'World')]
    if not df5.empty:
        plt.figure(figsize=(10, 6))
        df5.boxplot(column='emissions', by='region', vert=False)
        plt.title('Boxplot 5: Onshore Oil Emissions by Region (Excl. World)')
        plt.suptitle('')
        plt.xlabel('Emissions')
        plt.savefig('plot5.png')
methane_graphs('/Users/wenshi/Library/Mobile Documents/com~apple~CloudDocs/Study/UW Madison/AAE 718/AAE 718 - Pycharm/Methane_final.csv')

# Problem 7
def animal_crossing(filepath):
    df = pd.read_csv(filepath)
    return df

# Problem 8
def sell_price(filepath):
    df = animal_crossing(filepath)
    max_price_row = df[df['Sell'] == df['Sell'].max()]
    return max_price_row['Name'].values[0]

# Problem 9
def smallest_diff(filepath):
    df = animal_crossing(filepath)
    df['Buy'] = pd.to_numeric(df['Buy'], errors='coerce')
    df['Sell'] = pd.to_numeric(df['Sell'], errors='coerce')
    df = df.dropna(subset=['Buy', 'Sell'])
    df['diff'] = abs(df['Buy'] - df['Sell'])
    min_diff_row = df[df['diff'] == df['diff'].min()]
    return min_diff_row['Name'].values[0]


#file_path = '/Users/wenshi/Library/Mobile Documents/com~apple~CloudDocs/Study/UW Madison/AAE 718/Animal_Crossing/accessories.csv'
#print("Highest sell price item:", sell_price(file_path))
#print("Smallest price difference item:", smallest_diff(file_path))
