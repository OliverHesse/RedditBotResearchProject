this project was started after i got interesed in how many bots there actualy are on reddit.
inorder to do this i will pull data of the top posts in 
r/uknews
r/europe
r/politics

i will then go through each post and pull data from all users that commented on the post.
the important data i want to get on users is.
age of their account. what subreddits they follow. what subreddits they comment in. the frequency at which they comment and what sort of things they mention in their comments

and interesting statistic i would like to see is the frequency that phrases like
immigration,open borders,the left failed men occur.
and then compare that too the age of accounts.

i will expand upon the data gatherd and how it is analysed in the future


there are sadly some limits too how much data i can pull. i cannot specify a time limit and can only gather 1000 posts from each of new and top for each sub
this limits me significantly especialy since there will be an overlap between top and new.
to counteract this i will expand the number of subreddits i will research
luckily even with this limit i can still get a lot of users
the way the user_data file is formated is like such
{
    {
        crawled_time_stamp
        subreddit_name
        user_data{
            non unique list of users that commented in this subreddit
        }
    }
}

this will generate duplicate data e.g 1 user might have commented in both europe and uknews. so their user data is in both.
when however i do multi subreddit data analysis these users are not treated as 2 but one


here is an example:
total unique users from 5 posts: 269
that is from the top 5 posts on r/uknews and included We’re looking for mods… and Positive news weekend mega thread! which have few comments

graphs:
pie chart for age ranges and what subreddits they posted in
box plot for stuff like post frequency of accounts in an age range

python main.py uknews bot1 BotResearchProjectBot(by-/u/TiredAndExtraTired)
python main.py uknews bot2 CommentBehavior(by-/u/noWinner)