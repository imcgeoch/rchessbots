
""" 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    (1) Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer. 

    (2) Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.  
    
    (3)The name of the author may not be used to
    endorse or promote products derived from this software without
    specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

from config import config
import praw
import urllib2
import re
import datetime
import time

# define variables
USERNAME = config['username']
PASSWORD = config['password']
USER_AGENT = config['user_agent']
SUBREDDIT_LIST = config['subreddit_list']
REGEX_LIST = config['regex_list']
POST_TEXT = config['post_text']


# define methods
def go():
    log.write("Starting scan...\n")
    log.write(str(datetime.datetime.now())+"\n")
    for s in SUBREDDIT_LIST:
        subreddit = reddit.get_subreddit(s)  
        doPosts(subreddit)   
        doComments(subreddit)
    
    log.write("\nCompleted pass, sleeping for 5 minutes\n\n\n")
    print "Completed pass, sleeping for 5 minutes"
    time.sleep(300)

def doPosts(subreddit):
    for submission in subreddit.get_new(limit=10):
        log.write("Checking " + submission.id +"\n")
        commenters = []
        for x in submission.comments:
            commenters.append(x.author.name)
        if "PGN-Bot" in commenters:
            log.write("%s is already done\n" % submission.id)
        else:
            if not submission.is_self:
                log.write("identified as link post\n")
                processLinkPost(submission)
            else:
                log.write("identified as self post\n")
                processSelfPost(submission)

def doComments(subreddit):
    flat_comments = subreddit.get_comments()
    for comment in flat_comments:
        log.write("found comment %s \n" % comment.id)
        commenters = []
        for x in comment.replies:
            commenters.append(x.author.name)
        if "PGN-Bot" in commenters:
            
            log.write("%s is already done" % comment.id)
            break
        processComment(comment)

def processLinkPost(submission):
    op_link = submission.url.lower()
    pgn=linkToPgn(op_link)   
    
    if pgn:
        log.write("found game at %s\n" %  submission.url)
    #    log.write( "created pgn link: %s\n" % pgn[0])
        postPgn(pgn, submission.add_comment)
    else:
        log.write("no chess game at %s\n" % submission.url)

def processSelfPost(submission):
    op_text = submission.selftext.lower()
    link_list = []
    link_list = linkToPgn(op_text)
    for i in link_list:
        log.write( "Game found in selftext %s: " % submission.id + i +"\n") 
    if link_list:
        postPgn(link_list, submission.add_comment)
    else:
        log.write("No games in %s\n" % submission.id)

def processComment(comment):
    comment_text = comment.body.lower()
    link_list = []
    link_list = linksFromText(comment_text)
    for i in link_list:
        log.write( "Game found in comment %s: \n" % comment.id + i)
    
    if link_list:
        postPgn(link_list, comment.reply)
    else:
        log.write( "No games in %s \n" % comment.id)

def linksFromText(post):
    link_text = []
    if linkToPgn(post):
        link_text = linkToPgn(post)
    return link_text

def linkToPgn(post):
    linksCreated = []
    for n in REGEX_LIST:
        linksFound = re.findall(n[0], post)
        for link in linksFound:
            newLink = re.sub(n[1], n[2], link)
            log.write("Created link to %s\n" % newLink)
            linksCreated.append(newLink)
    return linksCreated

def getPgn(target):
    response = urllib2.urlopen(target)
    html = response.read()
    return html

def postPgn(links, postmethod):
    pgn = [] 
    for link in links:
        pgn.append(getPgn(link))
    singlePgn = '\n'.join(pgn)
    post = "[pgn]\n" + singlePgn + "\n[/pgn]"
    while True:
        try:
            newPost = postmethod(post + POST_TEXT)
            log.write("Successfully posted: %s\n" % newPost.id)       
            break
        except praw.errors.RateLimitExceeded as error:
            log.write( "Waiting %d seconds to be allowed to post\n" % min(error.sleep_time, 270))
            time.sleep(min(error.sleep_time, 270))

# Begin Script

print "Opening logfile"
log = open('logfile' , 'a')
log.write("\n\n Starting up...\n\n")

print "logging in to reddit"
log.write("Logging in to reddit...\n")
reddit = praw.Reddit(user_agent = USER_AGENT)
reddit.login(username = USERNAME, password = PASSWORD)
 
print 'preparing to go'
while True:
    go()

