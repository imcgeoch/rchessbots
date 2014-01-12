config = {

    'username' : 'PGN-Bot',
    'password' : '' ,
    'user_agent' : 'PGN-Bot is a bot to reply to links in /r/chess with text-based versions of the games',

# Three regular expressions are needed:
# 1. One that matches a link to a game, without group names, for searching
# 2. One that matches a link to a game, with group names, for subbing
# 3 One that matches a .pgn download link, with flags, for subbing
    'regex_list' : [( 'http://www\.chess\.com/l*i*v*echess/game\?id=[0-9]{8,9}','http://www\.chess\.com/(?P<gmtype>l*)i*v*echess/game\?id=(?P<id>[0-9]{8,9})', 'http://www.chess.com/echess/download_pgn?\g<gmtype>id=\g<id>'),( 'http://www\.chessgames\.com/perl/chessgame\?gid=[0-9]{7}', 'http://www\.chessgames\.com/perl/chessgame\?gid=(?P<id>[0-9]{7})', 'http://www.chessgames.com/perl/nph-chesspgn?text=1&gid=\g<id>'),('http://[a-z]{2}\.lichess\.org/[a-z0-9]{8}','http://(?P<lang>[a-z]{2})\.lichess\.org/(?P<id>[a-z0-9]{8})','http://\g<lang>.lichess.org/\g<id>/pgn')],

    'post_text' : "\nHi, I'm a bot that posts games you link to formatted for the [pgn viewer](http://www.reddit.com/r/chess/comments/1s8j14/inline_pgn_viewer_faq/). The pgn viewer is a plugin for [Firefox](https://addons.mozilla.org/en-US/firefox/addon/rchess-pgn-viewer/) and [Chrome](https://chrome.google.com/webstore/detail/hplecpnihkigeaiobbmfnfblepiadjdh) that allows you to view games inside reddit. "

}
