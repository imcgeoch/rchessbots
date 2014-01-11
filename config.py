config = {

    'username' : 'PGN-Bot',
    'password' : '' ,
    'user_agent' : 'PGN-Bot is a bot to reply to links in /r/chess with text-based versions of the games',
# nested_list is used for comparing and generating links. 
# for each site to process links from, provide 5 variables
# 
# [0] the beginning of a url, common to all games on that site
# [1] the beginning of a url, common to all pgn files of games on that site
# [2] the length of the unique id
# [3] the common url following the unique id of all pgns, if any
    'nested_list' : [('http://www.chess.com/livechess/game?id=', 'http://www.chess.com/livechess/download_pgn?id=', 9 , ''),('http://www.chess.com/echess/game?id=', 'http://www.chess.com/echess/download_pgn?id=', 9, ''),('http://www.chessgames.com/perl/chessgame?gid=', 'http://www.chessgames.com/perl/nph-chesspgn?text=1&gid=', 8, ''),('en.lichess.org/', 'http://en.lichess.org/', 8, '/pgn' )],
    'regex_list' : [( 'http://www\.chess\.com/l*i*v*echess/game\?id=[0-9]{8,9}','http://www\.chess\.com/(?P<gmtype>l*)i*v*echess/game\?id=(?P<id>[0-9]{8,9})', 'http://www.chess.com/echess/download_pgn?\g<gmtype>id=\g<id>'),( 'http://www\.chessgames\.com/perl/chessgame\?gid=[0-9]{7}', 'http://www\.chessgames\.com/perl/chessgame\?gid=(?P<id>[0-9]{7})', 'http://www.chessgames.com/perl/nph-chesspgn?text=1&gid=\g<id>'),('http://[a-z]{2}\.lichess\.org/[a-z0-9]{8}','http://(?P<lang>[a-z]{2})\.lichess\.org/(?P<id>[a-z0-9]{8})','http://\g<lang>.lichess.org/\g<id>/pgn')]


}
