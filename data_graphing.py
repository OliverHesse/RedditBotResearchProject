import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime
import os
import numpy

fig = px.scatter(x=range(10), y=range(10))
fig.write_html("data/graph_display.html")

def calculate_comment_frequency(end_date,comment_list):
    if len(comment_list) == 0:
        return 0
    youngest_comment,oldest_comment = float('inf'),0
    for comment in comment_list:
        comment_age = (end_date - datetime.fromtimestamp(comment[0])).days
        if comment_age > oldest_comment:
            oldest_comment = comment_age
        if comment_age < youngest_comment:
            youngest_comment = comment_age
    if oldest_comment-youngest_comment == 0:
        return 0
    return len(comment_list)/(oldest_comment-youngest_comment)




def generate_account_age_related_plots(data):
    unique_user_set = set()
    frequency_bands = {
        "<1":[],
        "1-2":[],
        "2-3":[],
        "3-4":[],
        "4-5":[],
        "5<":[]
    } 
    sentiment_bands ={
        "<1":{"Positive":0,"Negative":0,"Neutral":0},
        "1-2":{"Positive":0,"Negative":0,"Neutral":0},
        "2-3":{"Positive":0,"Negative":0,"Neutral":0},
        "3-4":{"Positive":0,"Negative":0,"Neutral":0},
        "4-5":{"Positive":0,"Negative":0,"Neutral":0},
        "5<":{"Positive":0,"Negative":0,"Neutral":0}
    }
    total_suspended_acc = 0
    #each data_instance has a different timestamp
    for data_instance in data:
        end_time = datetime.fromtimestamp(data_instance[0])
        for user in data_instance[2]:
            #avoid duplicate data points
            if user["username"] in unique_user_set:
                print("skipping user")
                continue
            unique_user_set.add(user["username"])

            account_creation_timestamp = user["creation-unix"]
            account_comment_list = user["comment-data-list"]
            if(user["is-suspended"] or account_creation_timestamp == 0):
                total_suspended_acc += 1
                continue
            account_age = end_time-datetime.fromtimestamp(account_creation_timestamp)
            comment_frequncy = calculate_comment_frequency(end_time,account_comment_list)
            
            comment_sentiment_list = []
            for comment in account_comment_list:
                comment_sentiment_list.append(comment[3])
            comment_dic = {p: comment_sentiment_list.count(p) for p in comment_sentiment_list}
            if account_age.days < 364:
                frequency_bands["<1"].append(comment_frequncy)
                sentiment_bands["<1"] = merge_dic(sentiment_bands["<1"],comment_dic)
            elif account_age.days < 728:
                frequency_bands["1-2"].append(comment_frequncy)
                sentiment_bands["1-2"] = merge_dic(sentiment_bands["1-2"],comment_dic)
            elif account_age.days < 1092:
                frequency_bands["2-3"].append(comment_frequncy)
                sentiment_bands["2-3"] = merge_dic(sentiment_bands["2-3"],comment_dic)
            elif account_age.days < 1456:
                frequency_bands["3-4"].append(comment_frequncy)
                sentiment_bands["3-4"] = merge_dic(sentiment_bands["3-4"],comment_dic)
            elif account_age.days < 1820:
                frequency_bands["4-5"].append(comment_frequncy)
                sentiment_bands["4-5"] = merge_dic(sentiment_bands["4-5"],comment_dic)
            else:
                frequency_bands["5<"].append(comment_frequncy)
                sentiment_bands["5<"] = merge_dic(sentiment_bands["5<"],comment_dic)

    #plot data
    fig = go.Figure()
    # Use x instead of y argument for horizontal plot
    fig.add_trace(go.Box(x=frequency_bands["<1"],name="< 1 year"))
    fig.add_trace(go.Box(x=frequency_bands["1-2"],name="1 to 2 years"))
    fig.add_trace(go.Box(x=frequency_bands["2-3"],name="2 to 3 years"))
    fig.add_trace(go.Box(x=frequency_bands["3-4"],name="3 to 4 years"))
    fig.add_trace(go.Box(x=frequency_bands["4-5"],name="4 to 5 years"))
    fig.add_trace(go.Box(x=frequency_bands["5<"],name="more than 5 years"))
    fig.update_traces(boxpoints='all', jitter=1)
    fig.show()
    for key in frequency_bands:
       
        frequency_bands[key] = numpy.mean(frequency_bands[key])
    print(frequency_bands)
    fig = px.bar(pd.Series(frequency_bands).to_frame())
    fig.show()

    labels = ["Positive","Negative","Neutral"]
    pie_chart_order = ["<1","1-2","2-3","3-4","4-5","5<"]
    specs = [[{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'},{'type':'domain'},{'type':'domain'}]]
    fig = make_subplots(rows=1, cols=6,specs=specs)
    for i,sentiment in enumerate(sentiment_bands):
        data = sentiment_bands[pie_chart_order[i]]
        fig.add_trace(go.Pie(labels=labels,values=[data["Positive"],data["Negative"],data["Neutral"]]),i,1)
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    fig.update_layout(
    title_text="Comment sentiment",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='<1', x=sum(fig.get_subplot(1, 1).x) / 2, y=0.5,
                      font_size=20, showarrow=False, xanchor="center"),
                 dict(text='1-2', x=sum(fig.get_subplot(1, 2).x) / 2, y=0.5,
                      font_size=20, showarrow=False, xanchor="center"),
                dict(text='2-3', x=sum(fig.get_subplot(1, 3).x) / 2, y=0.5,
                      font_size=20, showarrow=False, xanchor="center"),
                dict(text='3-4', x=sum(fig.get_subplot(1, 4).x) / 2, y=0.5,
                      font_size=20, showarrow=False, xanchor="center"),
                dict(text='4-5', x=sum(fig.get_subplot(1, 5).x) / 2, y=0.5,
                      font_size=20, showarrow=False, xanchor="center"),
                dict(text='5<', x=sum(fig.get_subplot(1, 6).x) / 2, y=0.5,
                      font_size=20, showarrow=False, xanchor="center"),])
    fig.show()
    print(f"total suspended acc: {total_suspended_acc}")





def merge_dic(dic1,dic2):
    keys = {"Positive","Negative","Neutral"}
    
    if "Positive" in dic2:
        dic1["Positive"] += dic2["Positive"]
    if "Negative" in dic2:
        dic1["Negative"] += dic2["Negative"]
    if "Neutral" in dic2:
        dic1["Neutral"] += dic2["Neutral"]
    return dic1
 
def generate_graphs(data_directory,generate_sentiment = False):
    data = []
    arr = os.listdir(data_directory)
    
    for file_path in arr:
        with open(data_directory+"/"+file_path,"r") as file:
            data += json.load(file)  
        
    print("generating graphs")
    generate_account_age_related_plots(data) 

if __name__ == "__main__":
    generate_graphs("data/user_data",True)