#theParser

*Note*: This is a completed homework assignment for MIT's 6.00x. I thought it was really cool though, so I decided to post it. Although I did well the course, this project is now deprecated. I'll be building other things, but welcome the pulls to spruce this up a bit.

Directions: Run theParser from the command line using this code:

    mkdir theParser
    cd theParser
    python theParser.py

To change the newsfeed, type

    edit triggers.txt

This newswire works by creating new 'triggers' which will fire articles to your newswire every 60 seconds. Customize your newswire using the following format in triggers.txt. A few examples have been provided already, but here are the specs:

[trigger name] [trigger type] [trigger]

  trigger name: an arbitrary name used to identify a particular trigger

  trigger type: one or combinations of the following types can be expressed to customize your newswire (SUBJECT, TITLE, SUMMARY, PHRASE, AND, OR, NOT). The first three types state where to look for your keyword, PHRASE types look for phrases and the last three logic types can be used in conjunction with trigger names to create complex triggers.

  trigger: a keyword, phrase or trigger name to be used in your new trigger.