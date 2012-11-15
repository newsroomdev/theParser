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

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError    
    

class WordTrigger(Trigger):

    def __init__(self, word)
        self.word = word

    def isWordIn(text):
        """
        Returns True if word is within text
        False otherwise
        """
        text, word = text.lower, word.lower
        text.replace(string.punctuation, " ")
        if self.word in text:
            return True
        else:
            return False

class TitleTrigger(WordTrigger):

    def __init__(self,word):
        self.word = word
        

class SubjectTrigger(WordTrigger):

class SummaryTrigger(WordTrigger):
    
