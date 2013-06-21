'''
The following bit of hackery was a part of the final project for MIT's CS 6.00.
It was broken up into a number of excersises that forced you to build tests before
you could start building the RSS reader.
'''
# 6.00x Problem Set 6
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from Tkinter import *

#======================
# Code for retrieving and parsing RSS feeds
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret
#======================

#======================
# Part 1
# Data structure design
#======================

class NewsStory(object):

    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def getGuid(self):
        return self.guid
        
    def getTitle(self):
        return self.title
    
    def getSubject(self):
        return self.subject
    
    def getSummary(self):
        return self.summary
    
    def getLink(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

class WordTrigger(Trigger):   
    def __init__(self, word):
        Trigger.__init__(self)
        self.word = word

    def isWordIn(self, text):
        text = text.lower()
        for l in text:
            if l in string.punctuation:
                text = string.replace(text,l,' ')
        text = text.split(' ')
        for w in text:
            if w == self.word.lower():
                return True
        return False

class TitleTrigger(WordTrigger):
    def evaluate(self, story):
        title = story.getTitle()
        return self.isWordIn(title)
         
class SubjectTrigger(WordTrigger):
    def evaluate(self, story):
        subject = story.getSubject()
        return self.isWordIn(subject)

class SummaryTrigger(WordTrigger):
    def evaluate(self, story):
        summary = story.getSummary()
        return self.isWordIn(summary)

class NotTrigger(object):
    def __init__(self, t):
        self.t = t
        
    def evaluate(self, story):
        if self.t.evaluate(story) == True: return False
        else: return True

class AndTrigger(object):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2

    def evaluate(self, story):
        if self.t1.evaluate(story) == True and self.t2.evaluate(story) == True:
            return True
        elif self.t1.evaluate(story) == False or self.t2.evaluate(story) == False:
            return False

class OrTrigger(object):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2

    def evaluate(self, story):
        if self.t1.evaluate(story) == False and self.t2.evaluate(story) == False:
            return False
        elif self.t1.evaluate(story) == True or self.t2.evaluate(story) == True:
            return True

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):
        if self.phrase in story.getTitle() or self.phrase in story.getSubject() \
           or self.phrase in story.getSummary():
            return True
        else: return False
            
#======================
# Part 3
# Filtering
#======================

def filterStories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.
    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    filtr = []
    for s in stories:
        for t in triggerlist:
            if t.evaluate(s) == True:
                filtr.append(s)
    return filtr

#======================
# Part 4
# User-Specified Triggers
#======================

def makeTrigger(triggerMap, triggerType, params, name):
    """
    Takes in a map of names to trigger instance, the type of trigger to make,
    and the list of parameters to the constructor, and adds a new trigger
    to the trigger map dictionary.

    triggerMap: dictionary with names as keys (strings) and triggers as values
    triggerType: string indicating the type of trigger to make (ex: "TITLE")
    params: list of strings with the inputs to the trigger constructor (ex: ["world"])
    name: a string representing the name of the new trigger (ex: "t1")

    Modifies triggerMap, adding a new key-value pair for this trigger.

    Returns: triggerMap[name]

    print '**************************************************************\n'
    import pprint as pp
    pp.pprint(locals())
    """
    trigger = {
        "TITLE": TitleTrigger,
        "SUBJECT": SubjectTrigger,
        "SUMMARY": SummaryTrigger,
        }
    logic = {
        "AND": AndTrigger,
        "OR": OrTrigger,
        "NOT": NotTrigger
        }
    if triggerType in trigger.keys():
        params = params[0]
        triggerMap[name] = trigger[triggerType](params)
        return triggerMap[name]
    elif triggerType in logic.keys():
        triggerMap[name] = logic[triggerType](*[triggerMap[param] for param in params])
        return triggerMap[name]
    elif triggerType == "PHRASE":
        params = " ".join(params)
        triggerMap[name] = PhraseTrigger(params)
        return triggerMap[name]
    
def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)
    triggers = []
    triggerMap = {}
    for line in lines:
        linesplit = line.split(" ")
        # Making a new trigger
        if linesplit[0] != "ADD":
            trigger = makeTrigger(triggerMap, linesplit[1],
                                  linesplit[2:], linesplit[0])
        # Add the triggers to the list
        else:
            for name in linesplit[1:]:
                triggers.append(triggerMap[name])
    return triggers
    
import thread

SLEEPTIME = 60 #seconds -- how often we poll


def main_thread(master):
    try:
        # These will probably generate a few hits...
        t1 = TitleTrigger("Obama")
        t2 = SubjectTrigger("Romney")
        t3 = PhraseTrigger("Election")
        t4 = OrTrigger(t2, t3)
        triggerlist = [t1, t4]
        triggerlist = readTriggerConfig("triggers.txt")
        
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.getGuid() not in guidShown:
                cont.insert(END, newstory.getTitle()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.getSummary())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.getGuid())

        while True:

            print "Polling . . .",
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

            stories = filterStories(stories, triggerlist)

            map(get_cont, stories)
            scrollbar.config(command=cont.yview)


            print "Sleeping..."
            time.sleep(SLEEPTIME)

    except Exception as e:
        print e


if __name__ == '__main__':

    root = Tk()
    root.title("Some RSS parser")
    thread.start_new_thread(main_thread, (root,))
    root.mainloop()
