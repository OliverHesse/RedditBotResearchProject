import praw
from praw.models import MoreComments,Comment
from datetime import datetime
import json
import sys
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
            self.comment_data_list = self.process_comment_list(redditor.comments.new(limit=1000))  
        except:
            self.comment_data_list = []
    
        

  
    def process_comment_list(self,comment_list):
        print("getting comments for user")
        comment_data_list = []
        for comment in comment_list:
            
            if isinstance(comment,MoreComments):
                print("found instance of MoreComment:")
                
                continue
                nested_comment_data_list = self.process_comment_list(comment.comments())
                comment_data_list += nested_comment_data_list
                continue   
            # in comments > text \n\n means the text is from another comment
            
           
            comment_data_list.append([comment.created_utc,comment.subreddit.display_name,comment.body,0])
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
def scrape_data(subreddit_list,ignore_accounts,MAX_POSTS,bot_name,agent_name):
    start_time = datetime.now()
    unique_user_set = set()
    user_list = []

    reddit = praw.Reddit(bot_name,user_agent=agent_name)
    file_json_data = []
    for subreddit_name in subreddit_list:
        sub = reddit.subreddit(subreddit_name)
        submissions = sub.hot(limit = MAX_POSTS)
        print("===== processing requests =====")
        subreddit_unique_user_set = set()
        subreddit_user_list = []
        for post in submissions:
            
            print("===== "+ post.title +"=====")
            comments = post.comments.list()
          
            post_user_list = process_comment_list(comments,subreddit_unique_user_set,ignore_accounts)
            
            print("post total users found: " +str(len(post_user_list)))
            subreddit_user_list += post_user_list
        data = []
        for user in subreddit_user_list:
            data.append(user.jsonify_user())
        
        file_json_data.append([datetime.now().timestamp(),subreddit_name,data])
        user_list += subreddit_user_list
        unique_user_set.update(subreddit_unique_user_set)
    
    print(f"program finished in: {datetime.now()-start_time}")
    print("unique accounts found: ")
    print(len(unique_user_set))
    print("User objects generated: ")
    print(len(user_list))
    return file_json_data
    with open("data/user_data.json","w") as file:
        json.dump(file_json_data, file, indent=4)   



if __name__ == "__main__":
    ignore_accounts = {"AutoModerator"}
    MAX_POSTS = 10

    if len(sys.argv) == 4:
        print(f"sub: {sys.argv[1]}")
        print(f"bot: {sys.argv[2]}")
        print(f"agent: {sys.argv[3]}")
        subreddit = sys.argv[1]
        bot = sys.argv[2]
        agent = sys.argv[3]
        data = scrape_data([subreddit],ignore_accounts,MAX_POSTS,bot,agent)
        print(data[0][1])
        with open(f"data/user_data/{subreddit}.json","w") as file:
            json.dump(data, file, indent=4)        


