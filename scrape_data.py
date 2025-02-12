import os
import subprocess
bots = [
    ["bot1","BotResearchProjectBot(by-/u/TiredAndExtraTired)"],
    ["bot2","CommentBehavior(by-/u/noWinner"]
]
sublist = [
    "europe",
    "uknews",
    #"politics"
]
if __name__ == "__main__":

    print("scraping subreddits")
    for i,sub in enumerate(sublist):
        subprocess.run(['start', 'cmd', '/k','python', 'data_scraper.py',sub,bots[i][0],bots[i][1]], shell=True)
   