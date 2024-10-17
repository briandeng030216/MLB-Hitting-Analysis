# import used packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import DBSCAN

# Function 1
def txt_to_csv(file_name):
    """
    Parameters:
        file_name: string

    Change the given file_name txt file into a dataframe and save as a csv file.
    """

    data = []
    player_data = []
    path = "data/" + file_name + ".txt"

    # put txt file data into dataframe
    with open(path, "r") as file:
        lines = file.readlines()
    
    for line in lines:
        line = line.strip()
        if line == "Graphs":
            data.append(player_data)
            player_data = []
        else:
            player_data.append(line)
    
    df = pd.DataFrame(data)
    df = df.drop(df.columns[0: 2], axis = 1)

    # set column name
    col_names = ["player", "pitches", "total", "pitches%", "PA", "AB", "BIP", "H", "1B", "2B", "3B", "HR", "SO",
     "K%", "BB", "BB%", "Whiffs", "Swings", "BA", "xBA", "OBP", "xOBP", "SLG", "xSLG", "wOBA", "xwOBA", "Barrels", "PV", "EV", "LA"]
    df.columns = col_names

    # change name to first, last name form
    player_names = df["player"]
    new_names = []
    for name in player_names:
        name = name.split(", ")
        new_name = name[1] + " " + name[0]
        new_names.append(new_name)
    df["player"] = new_names

    # replace all -- with 0
    df = df.replace("--", 0)

    # save the file
    df.to_csv("data/" + file_name + ".csv", index =False)

# Function 2
def search(data, players = "all", type = "fastball", features = "all"):
    """
    Parameters:
        data: a dictionary with all stats
        players: a list of player names
        type: a string
        features: a list of features
    
    Return a dataframe with given players, type, and features.
    """

    if players == "all":
        players = list(data.keys())
    new_data = {player: data[player] for player in players}

    if features == "all":
        col_names = ["player", "pitches", "total", "pitches%", "PA", "AB", "BIP", "H", "1B", "2B", "3B", "HR", "SO",
            "K%", "BB", "BB%", "Whiffs", "Swings", "BA", "xBA", "OBP", "xOBP", "SLG", "xSLG", "wOBA", "xwOBA", "Barrels", "PV", "EV", "LA"]
    else:
        col_names = ["player"] + features
    df = pd.DataFrame(columns = col_names)

    for player in new_data:
        row = [player]
        if features == "all":
            lst = list(new_data[player][type].values())
        else:
            lst = list(new_data[player][type][feature] for feature in features)
        
        row = row + lst
        df.loc[len(df)] = row

    return df

# Function 3
def get_top(df, feature, num = None, type = "fastball", ascending = False):
    """
    Parameters:
        df: a dataframe with all stat
        feature: a string representing feature
        num: an int
        type: a string
    
    Plot a scatter plot and return a dictionary with player name 
    as key and feature stat as value
    """

    # sort df with given feature
    if num == None:
        num = len(df)
    df[feature] = round(df[feature], 3)
    df = df.sort_values(by = feature, ascending = ascending)
    df = df.head(num).reset_index(drop = True)
    d = dict(zip(df["player"], round(df[feature], 3)))

    # create scatter plot
    x_scatter_plot(df, feature, num, type)

    return d

# Function 4
def x_scatter_plot(df, feature, num, type):
    """
    Parameters:
        df: a dataframe with aii stat
        feature: a string
        num: an int
        type: a string
    
    Plot a scatter woth givern inputs
    """

    sns.set_theme()
    fig = plt.figure(figsize = (20, 8))
    x = get_last_name(df)
    y = df[feature]
    fig = sns.scatterplot(x = x, y = y, hue = df["player"])
    title = feature + " Top " + str(num) + type_title(type)
    fig.set(title = title)

    for i in range(len(df)):
        plt.text(i, y[i], df[feature][i])

# Function 5
def get_last_name(df):
    """
    Parameters: 
        df: a dataframe

    Return a list with all players last name
    """

    lst = []

    for player in df["player"]:
        name = player.split(" ")[1]
        lst.append(name)
    
    return lst

# Function 6
def type_title(type):
    """
    Parameters:
        type: a string
    
    Return part of title with goven type.
    """

    if type == "fastball":
        title = " for All Fastball"
    if type == "4sf":
        title = " for 4-Seam Fastball"
    if type == "2sf":
        title = " for 2-Seam Fastball"
    if type == "cut":
        title == " for Cutter"
    if type == "92":
        title = " for Fastball < 92 mph"
    if type == "93-97":
        title = " for Fastball 93 - 97 mph"
    if type == "98":
        title = " for Fastball > 98 mph"
    
    return title

# Function 7
def x_y_scatter(df, x, y, type = "fastball"):
    """
    Parameters:
        df: a dataframe
        x, y: a string
    
    Create a scatter plot with x - y
    """

    # create plot
    fig = px.scatter(df, x = x, y = y, hover_name = "player", hover_data = {x: False, y: False})

    # plot league average
    avg_x = df[x].mean()
    avg_y = df[y].mean()
    min_x = min(df[x])
    min_y = min(df[y])
    max_x = max(df[x])
    max_y = max(df[y])
    fig.add_trace(go.Scatter(x = [min_x, max_x], y = [avg_y, avg_y], mode = "lines", line = dict(color = "red", width = 2), name = "league average " + y))
    fig.add_trace(go.Scatter(x = [avg_x, avg_x], y = [min_y, max_y], mode = "lines", line = dict(color = "orange", width = 2), name = "league average " + x))

    # plot 75th percentile
    x75 = np.percentile(df[x], 75)
    y75 = np.percentile(df[y], 75)
    fig.add_trace(go.Scatter(x = [min_x, max_x], y = [y75, y75], mode = "lines", line = dict(color = "brown", width = 2), name = "league 75th percentile " + y))
    fig.add_trace(go.Scatter(x = [x75, x75], y = [min_y, max_y], mode = "lines", line = dict(color = "pink", width = 2), name = "league 75th percentile " + x))

    # set figure layout
    title = x + " - " + y + " Graph" + type_title(type)
    fig.update_layout(
        width = 1200,
        height = 600,
        title = title,
        showlegend = True,
        legend = dict(x = 1, y = 1)
    )

    fig.show()

# Function 8
def dis_plot(df, feature):
    """
    Parameters:
        df: a dataframe
        feature: a string
    
    Plot a histogram graph with given feature from the given dataframe and basic info
    """

    sns.set_theme()
    fig = plt.figure(figsize = (12, 6))
    fig = sns.histplot(df, x = feature, color = "orange", bins = 25)
    title = feature + " distribution"
    fig.set(title = title)

    min_x = round(min(df[feature]), 3)
    max_x = round(max(df[feature]), 3)
    avg_x = round(df[feature].mean(), 3)
    std_x = round(np.std(df[feature]), 3)
    text = "min: " + str(min_x) + ", max: " + str(max_x) + ", mean: " + str(avg_x) + ", sd: " + str(std_x)
    print(text)

# Function 9.
def get_pos(df, player, feature, ascending = False):
    """
    Return the player ranking info in given feature and dataframe
    """

    df = df.sort_values(by = feature, ascending = ascending)
    df = df.reset_index(drop = True)
    rank = df[df["player"] == player].index[0]
    text = player + " ranks " + str(rank) + " out of " + str(len(df)) + " in " + feature

    return text

# Function 9
def cor_matrix(df, features):
    """
    Return a matrix with every two feature correlation from list features
    """

    df = df[features]
    cor = df.corr()

    return cor

# Function 10
def DBSCAN_alg(df, x, y, eps):
    """
    Perform DBSCAN algorithm with given dataframe, x, and y and plot
    a clustering graph.
    """

    df["x"] = df[x]
    df["y"] = df[y]
    X = df[["x", "y"]].values
    dbscan = DBSCAN(eps=eps, min_samples=3)
    df['cluster'] = dbscan.fit_predict(X)

    sns.set_theme()
    fig = plt.figure(figsize=(12, 6))
    unique_clusters = df['cluster'].unique()

    for cluster in unique_clusters:
        cluster_data = df[df['cluster'] == cluster]
        if cluster == -1:
            fig = sns.scatterplot(x = cluster_data['x'], y = cluster_data['y'], color='black', label='Noise', marker='x')
        else:
            fig = sns.scatterplot(x = cluster_data['x'], y = cluster_data['y'])

    plt.title('DBSCAN Clustering')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()