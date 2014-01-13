rchessbots
==========

Reddit bot to post formatted pgns for easier viewing


As of January 12, 2014, this reddit bot reads through 
selected subreddits and finds links to chess games in
submissions and comments. When it finds a link to a 
supported site, it grabs the pgn file from that game and
posts it as a comment posted for the chess.com pgn viewer.

The [pgn viewer](http://www.reddit.com/r/chess/comments/1s8j14/inline_pgn_viewer_faq/) is a plugin for [Firefox](https://addons.mozilla.org/en-US/firefox/addon/rchess-pgn-viewer/) and [Chrome](https://chrome.google.com/webstore/detail/hplecpnihkigeaiobbmfnfblepiadjdh) that allows you to view games inside reddit.
It was created by somebody else and has no affiliation
with this bot.

As of now, this bot does not have other functionality
that some discussed on r/chess, such as finding and
fixing posts of pgns, or aggregating posts for a weekly digest.
It could integrate such features if they were written.

Logs are kept so that the operator can check on what the 
program was doing in case of bugs etc.

A configuration file, config.py, allows the operator to 
choose the username, password, API agent, and subreddits
to operate on. The text that included in each post and
supported sites can also be changed. Every supported site 
needs three regular expressions:
1. One that matches a link to a game, without group names, for searching
2. One that matches a link to a game, with group names, for subbing
3. One that matches a .pgn download link, with group, for subbing

All the sites supported use unique game ids for each game
in standard link formats. This passes the id from a
game link to a pgn link. 
