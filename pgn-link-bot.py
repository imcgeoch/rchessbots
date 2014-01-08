import praw

""" 
A reddit bot that will reply to links to chess games on a number 
of off-reddit sites, take the pgns from those sites, and respond
with a comment containing the pgn in [pgn] tags for the veiwer plugin.

Completed: define variables 
TODO: Everything
"""

# define local variables from config file
from config import config

USERNAME = config['username']
PASSWORD = config['password']
USER_AGENT = config['user_agent']
SUBREDDIT_LIST = config['subreddit_list']

SITE_LIST = ['www.chess.com/echess/game/', 'www.chessgames.com/perl/chessgame',]

reddit = praw.Reddit(user_agent = USER_AGENT)
reddit.login(username = USERNAME, password = PASSWORD)
already_done = []     

print "logging in to reddit"


def go():
    subreddit = reddit.get_subreddit('chessbottesting')  
    print 'got subreddit'
    for submission in subreddit.get_new(limit=10):
        op_link = submission.url.lower()
        print "pulled link %s" % op_link
        if SITE_LIST[1] in op_link:
            print "found link \n ========== \n\n\n\n\n\n"
            processLinkPost(op_link)


"""          
def getPosts():

def getComments():
"""
def processLinkPost(op_link):
    print op_link
"""
def processSelfPost():

def processComment():

def linksFromText():

def checkLink():

def getPgn():

def postPgn():
"""
while ('true'):
    print 'preparing to go'
    go()


