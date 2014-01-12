
""" 
A reddit bot that will reply to links to chess games on a number 
of off-reddit sites, take the pgns from those sites, and respond
with a comment containing the pgn in [pgn] tags for the veiwer plugin.

"""

from config import config
import praw
import urllib2
import re
import datetime
import time

# define local variables
USERNAME = config['username']
PASSWORD = config['password']
USER_AGENT = config['user_agent']
REGEX_LIST = config['regex_list']
POST_TEXT = config['post_text']

already_done = []     


def go():
    log.write("Starting scan...\n")
    log.write(str(datetime.datetime.now())+"\n")
    subreddit = reddit.get_subreddit('chessbottesting')  
    for submission in subreddit.get_new(limit=10):
        # print "Checking " + submission.id
        log.write("Checking " + submission.id +"\n")
        commenters = []
        for x in submission.comments:
            commenters.append(x.author.name)
            print x.author.name + str(x.author.name == 'PGN-Bot')
        if "PGN-Bot" in commenters:
            log.write("%s is already done\n" % submission.id)
        else:
            if not submission.is_self:
                # print "identified as link post"
                log.write("identified as link post\n")
                processLinkPost(submission)
            else:
                # print "identified as self post"
                log.write("identified as self post\n")
                processSelfPost(submission)

    for submission in subreddit.get_hot(limit=25):
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        for comment in flat_comments:
            # print "found comment %s" % comment.id
            log.write("found comment %s \n" % comment.id)
            commenters = []
            for x in comment.replies:
                print x
                commenters.append(x)
            if "PGN-Bot" in commenters:
             
                log.write("%s is already done" % comment.id)
                break
            processComment(comment)
    # print "\nCompleted: "
    log.write("\nCompleted: \n")
    log.writelines(already_done)
    with open("completed_posts", 'w') as f:
        f.write('\n'.join(already_done))    

def processLinkPost(submission):
    op_link = submission.url.lower()
    pgn=linkToPgn(op_link)   
    
    if pgn:
        # print "found game at %s" %  submission.url
        # print "created pgn link: %s" % pgn[0]
        log.write("found game at %s\n" %  submission.url)
        log.write( "created pgn link: %s\n" % pgn[0])
        postPgn(submission, pgn, submission.add_comment)
    else:
        # print "no chess game at %s" % submission.url
        log.write("no chess game at %s\n" % submission.url)
    already_done.append(submission.id)

def processSelfPost(submission):
    op_text = submission.selftext.lower()
    link_list = []
    link_list = linkToPgn(op_text)
    for i in link_list:
        # print "Game found in  selftext %s: " % submission.id + i 
        log.write( "Game found in  selftext %s: " % submission.id + i +"\n") 
    
    if link_list:
        postPgn(submission, link_list, submission.add_comment)
    else:
        # print "No games in %s" % submission.id 
        log.write("No games in %s\n" % submission.id)
    already_done.append(submission.id)

def processComment(comment):
    comment_text = comment.body.lower()
    link_list = []
    link_list = linksFromText(comment_text)
    for i in link_list:
        # print "Game found in comment %s: " % comment.id + i
        log.write( "Game found in comment %s: \n" % comment.id + i)
    
    if link_list:
        postPgn(comment, link_list, comment.reply)
    else:
        # print "No games in %s" % comment.id
        log.write( "No games in %s \n" % comment.id)

    
    already_done.append(comment.id)

def linksFromText(post):
    link_text = []
    if linkToPgn(post):
        link_text = linkToPgn(post)
    return link_text

def linkToPgn(post):
    linksCreated = []
    for n in REGEX_LIST:
        # print n[0] + " 1"
        linksFound = re.findall(n[0], post)
        # print linksFound
        for link in linksFound:
            # print link 
            linksCreated.append(re.sub(n[1], n[2], link))
    return linksCreated

def getPgn(target):
    response = urllib2.urlopen(target)
    html = response.read()
    return html

def postPgn(parent, links, methodtorun):
    pgn = [] 
    
    for link in links:
        pgn.append(getPgn(link))
    singlePgn = '\n'.join(pgn)

    post = "[pgn]\n" + singlePgn + "\n[/pgn]"
    while True:
        try:
            methodtorun(post + POST_TEXT)       
            break
        except praw.errors.RateLimitExceeded as error:
            print "Waiting %d seconds to be allowed to post" % (error.sleep_time/2)
            time.sleep(error.sleep_time/2)

print "Opening logfile"
log = open('logfile' , 'a')
log.write("\n\n Starting up...\n\n")




print "logging in to reddit"
log.write("Logging in to reddit...\n")
reddit = praw.Reddit(user_agent = USER_AGENT)
reddit.login(username = USERNAME, password = PASSWORD)

 
print 'preparing to go'
go()

