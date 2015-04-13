#! /usr/bin/python
''' 
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
'''

from config import config
from credentials import credentials
import praw
import re
import datetime
import requests

# define variables
USERNAME = credentials['username']
PASSWORD = credentials['password']
USER_AGENT = credentials['user_agent']
SUBREDDIT_LIST = config['subreddit_list']
REGEX_LIST = config['regex_list']
POST_TEXT = config['post_text']


# define methods
def go():
    print 'Starting scan...'
    print str(datetime.datetime.now())
    for s in SUBREDDIT_LIST:
        subreddit = reddit.get_subreddit(s)  
        print 'Reading posts and comments in /r/%s' % subreddit
        doPosts(subreddit)   
        doComments(subreddit)

def doPosts(subreddit):
    for submission in subreddit.get_new(limit=10):
        print 'Checking ' + submission.id 
        comment_found = False
        for x in submission.comments:
            if re.search('\[pgn\].*\[/pgn\]', x.body, re.DOTALL):
                comment_found = True
        if comment_found :
            print '%s is already done' % submission.id
        else:
            if not submission.is_self:
                print 'identified as link post'
                processLinkPost(submission)
            else:
                print 'identified as self post'
                processSelfPost(submission)

def doComments(subreddit):
    flat_comments = subreddit.get_comments()
    for comment in flat_comments:
        print 'found comment %s ' % comment.id
        comment_found = False
        for x in comment.replies:
            if re.search('\[pgn\].*\[/pgn\]', x.body, re.DOTALL):
                comment_found = True
        if comment_found:
            print '%s is already done' % comment.id
            break
        processComment(comment)

def processLinkPost(submission):
    op_link = submission.url
    pgn=getGoodLinks(op_link)   
    
    if pgn:
        print 'found game at %s' %  submission.url
        postPgn(pgn, submission.add_comment)
    else:
        print 'no chess game at %s' % submission.url

def processSelfPost(submission):
    op_text = submission.selftext
    link_list = getGoodLinks(op_text)
    if re.search('\[pgn\].*\[/pgn\]', op_text, re.DOTALL):
		print 'comment already contains game'
    for i in link_list:
        print  'Game found in selftext %s: ' % submission.id + i 
    if link_list:
        postPgn(link_list, submission.add_comment)
    else:
        print 'No games in %s' % submission.id

def processComment(comment):
    comment_text = comment.body
    link_list = getGoodLinks(comment_text)
    if re.search('\[pgn\].*\[/pgn\]', comment_text, re.DOTALL):
		print 'comment already contains game'
		return

    for i in link_list:
        print  'Game found in comment %s: ' % comment.id + i
    
    if link_list:
        postPgn(link_list, comment.reply)
    else:
        print  'No games in %s ' % comment.id

def linksFromText(post):
    link_text = []
    if getGoodLinks(post):
        link_text = getGoodLinks(post)
    return link_text

def getGoodLinks(post):
    linksCreated = []
    for n in REGEX_LIST:
        linksFound = re.findall(n[0], post)
        for link in linksFound:
            newLink = re.sub(n[1], n[2], link)
            print 'Created link to %s' % newLink
            linksCreated.append(newLink)
    return linksCreated

def getPgn(target):
    print target
    r = requests.get(str(target))
    print r.text.replace('\n', '\n    ').encode('utf-8')
    return '    ' + r.text.replace('\n', '\n    ')

def postPgn(links, postmethod):
    singlePgn = ''
    toLong = False
    for link in links:
        nextPgn = getPgn(link)
        if len(singlePgn+nextPgn) <= 9700:
            singlePgn = singlePgn + nextPgn + '\n'
        else:
            toLong = True
            break
    post = '[pgn]\n\n' + singlePgn + '\n\n[/pgn]'
    if toLong:
        post = post + 'Post is too long, one or more games not included.\n\n'
    while True:
        try:
            newPost = postmethod(post + POST_TEXT)
            print 'Successfully posted: %s' % newPost.id       
            break
        except praw.errors.RateLimitExceeded as error:
            print  'Waiting %d seconds to be allowed to post' % min(error.sleep_time, 270)
            time.sleep(min(error.sleep_time, 270))
	except praw.errors.APIException as error:
	    print 'API Exception: ', error
            break

# Begin Script

print 'Logging in to reddit...'
reddit = praw.Reddit(user_agent = USER_AGENT)
reddit.login(username = USERNAME, password = PASSWORD)
 
print 'preparing to go'
go()
print 'done!'
