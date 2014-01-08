
""" 
A reddit bot that will reply to links to chess games on a number 
of off-reddit sites, take the pgns from those sites, and respond
with a comment containing the pgn in [pgn] tags for the veiwer plugin.

Completed: define variables 
TODO: Everything
"""

from config import config
import praw
import urllib2

# define local variables
USERNAME = config['username']
PASSWORD = config['password']
USER_AGENT = config['user_agent']
SUBREDDIT_LIST = config['subreddit_list']

SITE_LIST = ['www.chess.com/livechess/game', 'www.chess.com/echess/game', 'www.chessgames.com/perl/chessgame', 'en.lichess.org/']

reddit = praw.Reddit(user_agent = USER_AGENT)
reddit.login(username = USERNAME, password = PASSWORD)
already_done = []     

print "logging in to reddit"


def go():
    subreddit = reddit.get_subreddit('chessbottesting')  
    for  submission in subreddit.get_new(limit=10):
        
        print "Checking " + submission.id
        if not submission.is_self:
            print "id'd as link post"
            processLinkPost(submission)
        else:
            print "id'd as self post"
            processSelfPost(submission)

def processLinkPost(submission):
    op_link = submission.url.lower()
    for site in SITE_LIST:
        if site in op_link and not submission.id in already_done:
            print "found link \n ========== "
            print submission.id + "\n\n"
            already_done.append(submission.id)
    
    for p in already_done: print "Completed: \n " + p

def processSelfPost(submission):
    op_text = submission.selftext.lower()
    link_list = []
    link_list = linksFromText(op_text)

def processComment():
    return 0

def linksFromText(post):
    links_found = []
    link_text = []

    """# Catalog all locations of links to games
    for site in SITE_LIST:
        if site in post:
            links_found.append(post.index(site))
    links_found.sort()
"""

    # See where each links and use it generate the url of the DL link
    #for i in links_found:
    for i in range(0, len(post)-15):
        token = post[i:i+15]
        if token == "www.chess.com/l":
            link_text.append("http://www.chess.com/livechess/download_pgn?id=" + post[i+32:i+40])
            print "found chess.com/e"
        elif token == "www.chess.com/e":
            link_text.append("http://www.chess.com/echess/download_pgn?id=" + post[i+29:i+37])
            print "found www.chess.com/e"
        elif token == "www.chessgames.":
            link_text.append("http://www.chessgames.com/perl/nph-chesspgn?text=1&gid=" + post[i+38:i+45])   
            print "found chessgames"
        elif token == "en.lichess.org/":
            link_text.append("http://en.lichess.org/" + post[i+15:i+23] + "/pgn")
            print "found lichess"
    for a in link_text:
        print a
 
    return link_text
        

def checkLink():
    return 0

def getPgn(target):
    response = urllib2.urlopen(target)
    html = response.read()
    return html

def postPgn(links):
    post = "[pgn] " + pgn + "[/pgn]"
       
 
print 'preparing to go'
go()


