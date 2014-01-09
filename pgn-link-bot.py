
""" 
A reddit bot that will reply to links to chess games on a number 
of off-reddit sites, take the pgns from those sites, and respond
with a comment containing the pgn in [pgn] tags for the veiwer plugin.

"""

from config import config
import praw
import urllib2

# define local variables
USERNAME = config['username']
PASSWORD = config['password']
USER_AGENT = config['user_agent']
#SITE_LIST = config['subreddit_list']

SITE_LIST = ['www.chess.com/livechess/game', 'www.chess.com/echess/game', 'www.chessgames.com/perl/chessgame', 'en.lichess.org/']

NESTED_LIST = config['nested_list']

# nest = [('www.chess.com/livechess/game', 'http://www.chess.com/livechess/download_pgn?id=', '9' , ''),('www.chess.com/echess/game', 'http://www.chess.com/echess/download_pgn?id=', '9', ''),('www.chessgames.com/perl/chessgame', 'http://www.chessgames.com/perl/nph-chesspgn?text=1&gid=', '8', ''),('en.lichess.org/', 'http://en.lichess.org/', '9', '/pgn' )]

reddit = praw.Reddit(user_agent = USER_AGENT)
reddit.login(username = USERNAME, password = PASSWORD)
already_done = []     

print "logging in to reddit"


def go():
    subreddit = reddit.get_subreddit('chessbottesting')  
    for  submission in subreddit.get_new(limit=10):
        
  #      print "Checking " + submission.id
        if not submission.is_self:
 #           print "id'd as link post"
            processLinkPost(submission)
        else:
            print "id'd as self post"
            processSelfPost(submission)

def processLinkPost(submission):
    op_link = submission.url.lower()
    for site in NESTED_LIST:
        if site[0] in op_link and not submission.id in already_done:
  #          print "found link \n ========== "
  #          print submission.id + "\n\n"
            already_done.append(submission.id)
    
  #  for p in already_done: print "Completed: \n " + p

def processSelfPost(submission):
    op_text = submission.selftext.lower()
    link_list = []
    link_list = linksFromText(op_text)

def processComment():
    return 0

def linksFromText(post):
    links_found = []
    link_text = []

    # iterate through text
    for i in range(0, len(post)-15):
        # compare 15- character segments 
        token =  post[i:i+15]
        for n in NESTED_LIST:
            # generate vars from NESED_LIST and iterator
            lURL=n[0]
            pURL=n[1]
            idStart=i+n[2]
            idEnd=idStart+n[3]
            gameid = post[idStart:idEnd]
            pgnCreated = '' 

            print n[2]
            print len(n[1])
            print

            if token == lURL:
                pgnCreated = pURL + gameid + n[4]
                print "found link: %s" % pgnCreated
                link_text.append(pgnCreated)                

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

# print " testing nesting"
nest = [('www.chess.com/livechess/game', 'http://www.chess.com/livechess/download_pgn?id=', '9' , ''),('www.chess.com/echess/game', 'http://www.chess.com/echess/download_pgn?id=', '9', ''),('www.chessgames.com/perl/chessgame', 'http://www.chessgames.com/perl/nph-chesspgn?text=1&gid=', '8', ''),('en.lichess.org/', 'http://en.lichess.org/', '9', '/pgn' )]
