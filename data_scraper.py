import praw
from praw.models import MoreComments,Comment
from datetime import datetime
import json
import pprint
class User:

    def __init__(self,redditor):
        print(vars(redditor))
        try:
            self.username = getattr(redditor,"name","(NA)")
        except:
            self.username = "(NA)"
        try:
            self.is_suspended = getattr(redditor,"is_suspended",False)
        except:
            self.is_suspended = False
        try:
            self.creation_date = getattr(redditor,"created_utc", getattr(redditor,"created",0))
        except:
            self.creation_date = 0
        try:
            self.comment_karma = getattr(redditor,"comment_karma",0)
        except:
            self.comment_karma = 0
        try:
            self.comment_data_list = self.process_comment_list(redditor.comments.hot(limit=4))  
        except:
            self.comment_data_list = []
        pprint.pprint(vars(redditor))
        

  
    def process_comment_list(self,comment_list):
        comment_data_list = []
        for comment in comment_list:
            if isinstance(comment,MoreComments):
                nested_comment_data_list = self.process_comment_list(comment.comments())
                comment_data_list += nested_comment_data_list
                continue   
            comment_data_list.append([comment.created_utc,comment.subreddit.display_name,comment.body])
        return comment_data_list
    def jsonify_user(self):
        return {"username":self.username,
                "comment-karma":self.comment_karma,
                "is-suspended":self.is_suspended,
                "creation-unix":self.creation_date,
                "comment-data-list":self.comment_data_list}
def process_comment_list(comment_list,unique_user_set,ignore_accounts):
    
    user_list = []
    for comment in comment_list:
       
        if isinstance(comment, MoreComments):
            nested_user_list= process_comment_list(comment.comments(),unique_user_set,ignore_accounts)
            user_list += nested_user_list
            
            continue

        
        author = comment.author
        if author == None:
            continue
        if author.name in unique_user_set or author.name in ignore_accounts:
            continue
        user_list.append(User(author))
        unique_user_set.add(author.name)
    return user_list
def run(subreddit_list,reddit_client_data,ignore_accounts,MAX_POSTS):
    start_time = datetime.now()
    unique_user_set = set()
    user_list = []
    reddit = praw.Reddit("bot1",user_agent="BotResearchProjectBot (by /u/TiredAndExtraTired )")
    file_json_data = []
    for subreddit_name in subreddit_list:
        sub = reddit.subreddit(subreddit_name)
        submissions = sub.hot(limit = MAX_POSTS)
        print("===== processing requests =====")
        subreddit_user_list = []
        for post in submissions:
            
            print("===== "+ post.title +"=====")
            comments = post.comments.list()
          
            post_user_list = process_comment_list(comments,unique_user_set,ignore_accounts)
            
            print("post total users found: " +str(len(post_user_list)))
            subreddit_user_list += post_user_list
        data = []
        for user in subreddit_user_list:
            data.append(user.jsonify_user())
        file_json_data.append([datetime.now().timestamp(),data])
        user_list += subreddit_user_list
    with open("data/user_data.json","w") as file:
        json.dump(file_json_data, file, indent=4)   
    print(f"program finished in: {datetime.now()-start_time}")
    print("unique accounts found: ")
    print(len(unique_user_set))
    print("User objects generated: ")
    print(len(user_list))


