# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re

utc = pytz.utc
#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
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
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate



#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# PhraseTrigger

class PhraseTrigger(Trigger):
    def __init__(self, s):
        self.s = s.lower()

    def get_phrase(self):
        return self.s

    def is_phrase_in(self, text):
        s = PhraseTrigger.get_phrase(self)

        regex = re.compile(r'[ \!\"\#\$\%\&\\\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\\\]\^\_\`\{\|\}\~ ]')

        split_text = regex.split(text)
        text = re.sub(r'\s+', ' ' , ' '.join(split_text))

        if re.search(fr'{s}[\s\W]', text + ' '):
            return True




# Problem 3
# TitleTrigger

class TitleTrigger(PhraseTrigger):
    def __init__(self, s):
        PhraseTrigger.__init__(self, s)

    def evaluate(self, story):
        title = story.get_title().lower()
        return PhraseTrigger.is_phrase_in(self, title)



# Problem 4
# DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):
    def __init__(self, s):
        PhraseTrigger.__init__(self, s)

    def evaluate(self, story):
        desc = story.get_description().lower()
        return PhraseTrigger.is_phrase_in(self, desc)

# TIME TRIGGERS

# Problem 5
# TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, time):
        self.time = utc.localize(datetime.strptime(time, '%d %b %Y %H:%M:%S'))

    def get_time(self):
        return self.time

# Problem 6
# BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    def __init__(self, time):
        TimeTrigger.__init__(self, time)

    def evaluate(self, story):
        
        if TimeTrigger.get_time(self) > utc.localize(story.get_pubdate().replace(tzinfo=None)):
            return True
        else:
            return False

class AfterTrigger(TimeTrigger):
    def __init__(self, time):
        TimeTrigger.__init__(self, time)

    def evaluate(self, story):
        
        if TimeTrigger.get_time(self) < utc.localize(story.get_pubdate().replace(tzinfo=None)):
            return True
        else:
            return False


# COMPOSITE TRIGGERS

# Problem 7
# NotTrigger

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# Problem 8
# AndTrigger

class AndTrigger(Trigger):
    def __init__(self, T1, T2):
        self.T1 = T1
        self.T2 = T2

    def evaluate(self, story):
        return self.T1.evaluate(story) and self.T2.evaluate(story)

# Problem 9
# OrTrigger

class OrTrigger(Trigger):
    def __init__(self, T1, T2):
        self.T1 = T1
        self.T2 = T2

    def evaluate(self, story):
        return self.T1.evaluate(story) or self.T2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # Problem 10

    filtered_stories = []

    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)

    return filtered_stories




#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    trigger_placeholder = {}
    triggers_to_add = {}

    def find_trigger_type(line):
        '''
        line is a list containig trigger name and type ('Title, desc, time, etc')
        returns object instance to use
        '''

        if line[1] == 'TITLE':
            return TitleTrigger(line[2])   #string to match in title

        elif line[1] == 'DESCRIPTION':
            return DescriptionTrigger(line[2]) #string to match in description

        elif line[1] == 'BEFORE':
            return BeforeTrigger(line[2])  #Correctly formatted time string. '%d %b %Y %H:%M:%S'

        elif line[1] == 'AFTER':
            return AfterTrigger(line[2])   #Correctly formatted time string. '%d %b %Y %H:%M:%S'

        elif line[1] == 'OR':
            return OrTrigger(line[2], line[3])

        elif line[1] == 'AND':
            return AndTrigger(line[2], line[3])

        elif line[1] == 'NOT':
            return NotTrigger(line[2])




    for line in lines:
        line = line.split(',')

        if line[0] == 'ADD':
            for trigger in line[1:]:
                triggers_to_add[trigger] = trigger_placeholder[trigger]

        else:
            trigger_placeholder[line[0]] = find_trigger_type(line)


    trigger_list = [c for c in triggers_to_add.values()]


    return trigger_list



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("election")
        # t2 = DescriptionTrigger("Trump")
        # t3 = DescriptionTrigger("Biden")
        # t4 = OrTrigger(t2, t3)
        # triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
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
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

