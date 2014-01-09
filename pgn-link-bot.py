
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

NESTED_LIST = config['nested_list']

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

    for submission in subreddit.get_hot(limit=25):
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        for comment in flat_comments:
            print "found comment %s" % comment.id
            processComment(comment)
    print "Completed"
    for p in already_done: print p

def processLinkPost(submission):
    op_link = submission.url.lower()
    for site in NESTED_LIST:
        if site[0] in op_link and not submission.id in already_done:
            print "found link: %s " % submission.url
            already_done.append(submission.id)
            break
    else:
        print "no chess game at %s" % submission.url

def processSelfPost(submission):
    op_text = submission.selftext.lower()
    link_list = []
    link_list = linksFromText(op_text)



    already_done.append(submission.id)

def processComment(comment):
    comment_text = comment.body.lower()
    link_list = []
    link_list = linksFromText(comment_text)

    already_done.append(comment.id)

def linksFromText(post):
    links_found = []
    link_text = []

    # try this for every site:
    for n in NESTED_LIST:
        linkURL=n[0]
        pgnURL=n[1]
        urlLength = len(linkURL)
        # iterate through text
        for i in range(0, len(post)-urlLength):
            # generate vars from NESED_LIST and iterator
            token =  post[i:i+urlLength]
            idStart=i+urlLength
            idEnd=idStart+n[2]
            gameid = post[idStart:idEnd]
            pgnCreated = '' 

            if token == linkURL:
                print "found link %s" % linkURL + gameid
                pgnCreated = pgnURL + gameid + n[3]
                print "created pgn: %s" % pgnCreated
    # print links
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

