import praw

""" 
A reddit bot that will reply to links to chess games on a number 
of off-reddit sites, take the pgns from those sites, and respond
with a comment containing the pgn in [pgn] tags for the veiwer plugin.

Completed: 
TODO: Everything
"""

# define local variables from config file
from config import config

USERNAME = config['username']
PASSWORD = config['password']
USER_AGENT = config['user_agent']
SUBREDDIT_LIST = config['subreddit_list']

reddit = praw.Reddit(user_agent = user_agent)
reddit.login(username = username. password = password)
     

def go():
          
def getPosts():

def getComments():

def processLinkPost():

def processSelfPost():

def processComment():

def linksFromText():

def checkLink():

def getPgn():

def postPgn():

