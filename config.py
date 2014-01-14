config = {

    'username' : 'PGN-Bot',
    'password' : '' ,
    'user_agent' : 'PGN-Bot is a bot to reply to links in /r/chess with text-based versions of the games',
    'subreddit_list' : ['chessbottesting', 'chess'],

# Three regular expressions are needed:
# 1. One that matches a link to a game, without group names, for searching
# 2. One that matches a link to a game, with group names, for subbing
# 3 One that matches a .pgn download link, with flags, for subbing
    'regex_list' : [( 'http://www\.chess\.com/l?i?v?echess/game\?id=[0-9]{8,9}','http://www\.chess\.com/(?P<gmtype>l?)i?v?echess/game\?id=(?P<id>[0-9]{8,9})', 'http://www.chess.com/echess/download_pgn?\g<gmtype>id=\g<id>'),( 'http://www\.chessgames\.com/perl/chessgame\?gid=[0-9]{7}', 'http://www\.chessgames\.com/perl/chessgame\?gid=(?P<id>[0-9]{7})', 'http://www.chessgames.com/perl/nph-chesspgn?text=1&gid=\g<id>'),('http://[a-z]{2}\.lichess\.org/[a-z0-9]{8}','http://(?P<lang>[a-z]{2})\.lichess\.org/(?P<id>[a-z0-9]{8})','http://\g<lang>.lichess.org/\g<id>/pgn')],

# This is the text that goes in every post after the games
    'post_text' : "\n\nHi, I'm a bot. When I find links to chess games, I reply with PGN formatted for viewing with the [reddit PGN viewer](http://www.reddit.com/r/chess/wiki/pgnviewer).\n\n---------- \n\n ([Source Code](https://github.com/rastalas/rchessbots) | [Report a Bug](http://www.reddit.com/message/compose/?to=Summervillain)) "

}
