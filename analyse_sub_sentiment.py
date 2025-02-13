import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import sys
#not very good at its job sadly
#try to use some sort of LLM solution as they will most likely be more accurate
def analyse_comments_sentiment(comment):
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(comment[2])['compound']
    if sentiment_dict >= 0.05 :
        return "Positive"
    elif sentiment_dict <= -0.05 :
        return "Negative"
    else :
        return "Neutral"

def sentiment_analysis_inital(data):

    #each data_instance has a different timestamp
    for data_instance_i,data_instance in enumerate(data):
        end_time = datetime.fromtimestamp(data_instance[0])
        for user_i,user in enumerate(data_instance[2]):
            #avoid duplicate data points
            print(f"analysing: {user["username"]}")
            account_comment_list = user["comment-data-list"]
            
            for comment_i,comment in enumerate(account_comment_list):
                comment_sentiment = analyse_comments_sentiment(comment)
                data[data_instance_i][2][user_i]["comment-data-list"][comment_i].append(comment_sentiment)
            print(f"finished analysing user {user["username"]}")
    return data

if __name__ == "__main__":
    if len(sys.argv) == 2:
        start_time = datetime.now()
        print("starting program")
        file_data = None
        print(sys.argv[1])
        with open(sys.argv[1],"r") as file:
            file_data = json.load(file)
        new_data = sentiment_analysis_inital(file_data)
        with open(sys.argv[1],'w') as file:
            json.dump(new_data, file, indent=4)  
        print(f"process finished in: {datetime.now()-start_time}")