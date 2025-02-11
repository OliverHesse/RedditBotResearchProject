import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
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
    return (oldest_comment-youngest_comment)/len(comment_list)
def generate_post_frequency_box_plot(data):
    frequency_bands = {
        "<1":[],
        "1-2":[],
        "2-3":[],
        "3-4":[],
        "4-5":[],
        "5<":[]
    } 
    total_suspended_acc = 0
    #each data_instance has a different timestamp
    for data_instance in data:
        end_time = datetime.fromtimestamp(data_instance[0])
        for user in data_instance[1]:
            account_creation_timestamp = user["creation-unix"]
            account_comment_list = user["comment-data-list"]
            if(user["is-suspended"] or account_creation_timestamp == 0):
                total_suspended_acc += 1
                continue
            account_age = end_time-datetime.fromtimestamp(account_creation_timestamp)
            comment_frequncy = calculate_comment_frequency(end_time,account_comment_list)
 
            if account_age.days < 364:
                frequency_bands["<1"].append(comment_frequncy)
            elif account_age.days < 728:
                frequency_bands["1-2"].append(comment_frequncy)
            elif account_age.days < 1092:
                frequency_bands["2-3"].append(comment_frequncy)
            elif account_age.days < 1456:
                frequency_bands["3-4"].append(comment_frequncy)
            elif account_age.days < 1820:
                frequency_bands["4-5"].append(comment_frequncy)
            else:
                frequency_bands["5<"].append(comment_frequncy)

    #plot data
    fig = go.Figure()
    # Use x instead of y argument for horizontal plot
    fig.add_trace(go.Box(x=frequency_bands["<1"],y="< 1 year"))
    fig.add_trace(go.Box(x=frequency_bands["1-2"],y="1 to 2 years"))
    fig.add_trace(go.Box(x=frequency_bands["2-3"],y="2 to 3 years"))
    fig.add_trace(go.Box(x=frequency_bands["3-4"],y="3 to 4 years"))
    fig.add_trace(go.Box(x=frequency_bands["4-5"],y="4 to 5 years"))
    fig.add_trace(go.Box(x=frequency_bands["5<"],y="more than 5 years"))

    fig.show()
    #figure = px.box( points="all")
    #figure.update_traces(orientation='h')

def generate_graphs(file_path):
    with open(file_path,"r") as file:
        data = json.load(file)
        generate_post_frequency_box_plot(data)   