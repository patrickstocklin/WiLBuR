# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 09:27:39 2015

@author: Pat
"""

import praw
import time
import pprint
import sys
import nltk.data

    #Given a word, returns the number of syllables (sometimes inaccurate)
    #Solution taken from: http://stackoverflow.com/
                        #questions/14541303/count-the-number-of-syllables-in-a-word 
def countSyllables(word): 
    count = 0
    vowels = 'aeiouy'
    word = word.lower().strip(".:;?!,")
        #If first letter is a vowel
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
            #Handles compound-vowel syllables
        if word[index] in vowels and word[index-1] not in vowels:
            count += 1
        #handles words like 'scene'
    if word.endswith('e'):
        count -= 1
        #handles words like 'rustle'
    if word.endswith('le'):
        count += 1
        #every word we miss must make a sound
    if count == 0:
        count +=1
    return count

    #Given a excerpt of text, returns the writing level
    #Will implement more scores later
def calculateScore(writingText):
    #Flesch Grade Level:
    #Calculate the average number of words used per sentence
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        #Creates a list of sentences
    sample = tokenizer.tokenize(writingText.decode("utf8"), writingText)
    totalSentences = len(sample)
    totalWords = 0
    totalSyllables = 0
    
        #Probably an easier way to do this
    for i in range(0, totalSentences):
        sentence = sample[i].split()
        numOfWords = len(sentence)
        for j in range(0, numOfWords):
            totalSyllables = totalSyllables + countSyllables(sentence[j])
        totalWords = totalWords + numOfWords

    print "VALUES FROM CALCULATIONS!"
    print totalSentences, totalWords, totalSyllables    
    
    #Flesch Grade-Level
    FleschGL = 0.39*(float(totalWords) / float(totalSentences))
    FleschGL = FleschGL +11.8*(float(totalSyllables) / float(totalWords))
    FleschGL = FleschGL - 15.59
    
    #Flesch Reading Ease:
    FleschRE = 206.835 - 1.015*(float(totalWords) / float(totalSentences))
    FleschRE = FleschRE - 84.6*(float(totalSyllables) / float(totalWords))
    #90-100 - easily understood by 11y/o
    #60-70 - easily understood by 13 - 15 y/o
    #0-30 - best understood by university graduates
    return FleschGL, FleschRE

def get_Inbox(r):
    print "Checking WiLBuR's Inbox"
    botInbox = r.get_unread()
    return botInbox

def get_Unread_Message(message):
        print "Called by: ", message.author
        print "Called to thread: ", message.submission
        submissionID = message._submission.id
        timestamp = message.created_utc
        author = message.author
        return submissionID, author, timestamp
        
def format_Results(score, fscore, author):
    result = str(author) + "'s Flesch-Kincaid Grade/Score is: " + " %.2f" %score   
    result = result + "\n\n" + str(author) + "'s Flesch Reading Ease is: " + " %.2f" %fscore
    print result
    return result
    
def main():
    #If we do not provide a password, PRAW prompts the user for one
    password = sys.argv[1:]
     
    try:
        r = praw.Reddit("A Sarcastic Bot that determines a user's writing level "
                "by Pat Stocklin, v 1.0.")
        r.login('WritingLevelBot', password)
    except:
        print "Bad Login (System Exiting)"
        sys.exit()
    
    while True:
        botInbox = get_Inbox(r)
        for newMessage in botInbox:
                #Grab submissionID, author, timestamp
            submissionID, author, timestamp = get_Unread_Message(newMessage)
                #Grab the Submission Object
            submission = r.get_submission(submission_id = newMessage._submission.id)
            thread = praw.helpers.flatten_tree(submission.comments)
            commentOfInterest = None
            parentID = ""
            for comment in thread:
                if isinstance(comment, praw.objects.MoreComments):
                    for comm in comment.comments():
                        thread.append(comm)
                else:
                    for comm in comment.replies:
                        thread.append(comm)
                    if "/u/WritingLevelBot" in comment.body and comment.created_utc == timestamp:
                        print "Found Our Caller!"
                        commentOfInterest = comment
                        parentID = comment.parent_id[3:]
                        break
                #There is probably a better way of grabbing the parent's comment
            for comment in thread:
                try:
                    if parentID == submissionID:
                        userscore, fscore = calculateScore(submission.selftext.lower())
                        replyText = format_Results(userscore, fscore, comment.author)
                        commentOfInterest.reply(replyText)
                        print "Successfully gave score: ", str(userscore)
                        break
                    if parentID == comment.id:
                        stringtoread = comment.body.encode('utf8')
                        userscore, fscore = calculateScore(stringtoread)
                        replyText = format_Results(userscore, fscore, comment.author)
                        commentOfInterest.reply(replyText)
                        print "Successfully gave score: ", str(userscore)
                        break
                except praw.errors.RateLimitExceeded as e:
                    pprint.pprint(vars(e))
                    print "RateLimited for " + str(e.sleep_time) + " seconds at " + time.strftime("%H:%M:%S", time.gmtime())
                    time.sleep(600)
                    continue
                except praw.errors.HTTPException as e:
                    pprint.pprint(vars(e))                    
                    print "HTTPException occured"
                    time.sleep(600)                    
                    continue
            newMessage.mark_as_read()
        time.sleep(10)
            

if __name__ == "__main__":
    sys.exit(main())
