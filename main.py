from data_scraper import run
from data_graphing import generate_graphs
from datetime import datetime
research_subreddits = [
    "europe",
    "uknews",
    #"politics"
]
ignore_accounts = {"AutoModerator"}
ignore_post_containing ={"Megathread"}
NUMBER_OF_POSTS = 2
if __name__ == "__main__":
    start_time = datetime.now()
    print("program started running")
    #run(research_subreddits,ignore_accounts,NUMBER_OF_POSTS)
    generate_graphs("data/user_data.json")
    print(f"programmed finished running and took: {datetime.now()-start_time}")