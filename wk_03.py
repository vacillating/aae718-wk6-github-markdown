import pandas as pd
import numpy as np

# Problem 1

def methane(file_path):

    cols_to_keep = [
            'region', 
            'country', 
            'emissions', 
            'type', 
            'segment',
            'reason', 
            'baseYear', 
            'notes'
            ]
    
    
    df = pd.read_csv(file_path, usecols = cols_to_keep)

    return df

# Problem 2

def methane_aggregation(file_path):  
    df = methane(file_path)
    not_world = df.query("region != 'World' and type != 'Agriculture'")["emissions"].sum()
    world = df.query("region == 'World' and type != 'Agriculture'")["emissions"].sum()
    return not_world - world


# Problem 3

def problem_03(file_path):
    df = methane(file_path)
    return df.query("region != 'World' and type != 'Agriculture'")["segment"].unique()


# Problem 4
"""
I am using method to make Pandas data manipulation look better (more like R, 
which data really well). The idea is wrap your code in (...) and put each operation
on a new line. 
"""
def region_mean(df):
    return (df.
            groupby("region").
            agg(
                {"emissions": np.mean}
            )
    )

# Problem 5
"""
Using the above method it was very easy to add a query to my dataframe. Typically
you will be doing this in a notebook, not as functions. The above code would just 
become the bottom code. 
"""
def region_total_mean(df):
    return (df.
            query("segment == 'Total'").
            groupby("region").
            agg(
                {"emissions": np.mean}
            )
    )




# Problem 6
#
# I'll make one function for each graph. 
#
# In your real life, this would be an iterative process where you were exploring 
# some data. Slowly building the graph that shows the information you want. 

def problem_06_1(df, file_path = "plot1.png"):
    (df.
        boxplot("emissions", by = "region", figsize = (10, 5)).
        get_figure().
        savefig(file_path)
    )

def problem_06_2(df, file_path = "plot2.png"):
    (df.
    query("region != 'World'").
    boxplot("emissions", by = "region", figsize = (10, 5)).
    get_figure().
    savefig(file_path)
)


def problem_06_3(df, file_path = "plot3.png"):
    (df.
        query("region != 'World' and segment == 'Total'").
        boxplot("emissions", by = "region", figsize = (10, 5)).
        get_figure().
        savefig(file_path)
    )

def problem_06_4(df, file_path = "plot4.png"):
    (df.
        query("region != 'World' and segment != 'Total'").
        boxplot("emissions", by = "region", figsize = (10, 5)).
        get_figure().
        savefig(file_path)
    )


# I did something different here. The boxplot command was getting long, so I 
# broke it over several lines. Each argument is on its own line and they are 
# indented to show they are part of the same command. Also, notice the last 
# argument ends with a comma (vert=False,). This way if I add a new argument
# I don't forget to add a comma. This is a total lie, of course. I almost never
# put the comma until I get an error. In fact it happened when I was writing this
# very function, I added the vert=False argument, forgot the comma, and got an
# error. 

def problem_06_5(df, file_path = "plot5.png"):
    (df.
        query("region != 'World' and segment != 'Total'").
        boxplot(
            "emissions", 
            by = "segment", 
            figsize = (10, 5),
            vert=False,
            ).
        get_figure().
        savefig(file_path)
    )


# problem 7

def animal_crossing(file_path):
    return pd.read_csv(file_path, usecols = ["Name","Buy","Sell"])


# problem 8
def sell_price(df):
    return df[df["Sell"] == df["Sell"].max()]

# problem 9

# The below function is bad because it changes the input dataframe, df. This is 
# not necessarily a problem, however the goal of this function is to return a 
# computation based on df. It's hard to trust the computation if it changes the 
# input. 
#
# For example, say the check engine light comes on in your car. You take it to the
# mechanic so he run a code check. When you get your car back you notice the door
# is very obviously different, like it's a whole new door. Would you trust that
# mechanic?

def bad_smallest_diff(df):
    df["Buy"] = pd.to_numeric(df["Buy"], errors="coerce")
    df["diff"] = df["Buy"] - df["Sell"]
    return df[df["diff"] == df["diff"].min()]["Name"].unique()


def smallest_diff(df):
    X = pd.to_numeric(df["Buy"], errors="coerce")
    Y = X - df["Sell"]
    return df[Y == Y.min()]["Name"].unique()
    

if __name__ == "__main__":

    methane_path = "Worksheets/wk_03-Pandas/data/Climate/Methane_final.csv"

    df = methane(methane_path)

    problem_06_1(df)
    problem_06_2(df)
    problem_06_3(df)
    problem_06_4(df)
    problem_06_5(df)

