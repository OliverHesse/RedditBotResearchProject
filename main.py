from data_scraper import scrape_data,User
from data_graphing import generate_graphs
from datetime import datetime
import sys
import json
research_subreddits = [
    "europe",
    "uknews",
    #"politics"
]
ignore_accounts = {"AutoModerator"}
ignore_post_containing ={"Megathread"}
NUMBER_OF_POSTS = 4
if __name__ == "__main__":
    start_time = datetime.now()
    print("program started running")
    print(sys.argv)
    if len(sys.argv) == 4:
        print(f"sub: {sys.argv[1]}")
        print(f"bot: {sys.argv[2]}")
        print(f"agent: {sys.argv[3]}")
        subreddit = sys.argv[1]
        bot = sys.argv[2]
        agent = sys.argv[3]
        data = scrape_data([subreddit],ignore_accounts,NUMBER_OF_POSTS,bot,agent)
        print(data[0][1])
        with open(f"data/user_data/{subreddit}.json","w") as file:
            json.dump(data, file, indent=4)   
    else:
        generate_graphs("data/user_data",True)
    print(f"programmed finished running and took: {datetime.now()-start_time}")