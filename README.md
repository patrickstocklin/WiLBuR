# WiLBuR
WiLBuR is a reddit-bot which, upon being called (responds to account name: /u/WritingLevelBot), replies to the caller with their parent-comment's Flesch-Kincaid Writing Level and Readability Ease Score. For language processing, WiLBuR uses python's Natural Language Toolkit (NLTK) as a lexical resource for tokenizing sentences into usable words. WiLBuR utilizes the PRAW module for interacting with reddit's API. Once calculated, WiLBuR replies to its caller with the fetched results.

Helpful Links:
  Flesch-Kincaid Reading Ease on Wikipedia: https://en.wikipedia.org/wiki/Flesch–Kincaid_readability_tests
  NLKT: http://www.nltk.org
  PRAW: https://praw.readthedocs.org/en/v3.1.0/
  
WiLBuR may be modified to work with any reddit account which is interested in finding comments or interest given a submission-object. One only needs NLTK's punkt data package, which can be found on their website above, a reddit account, and PRAW installed on their machine.

#Important Notes:
PRAW will be modifying their authentication protocol for user accounts as of 08/03/15, please take note as this will affect the current version of WiLBuR.

WiLBuR has accrued sufficient comment-karma so that it may exceed the initial comment Rate-Limit. An exception is thrown to sleep for 10 minutes otherwise.

Command to Run: python WiLBuR.py [password]. If a password is not given, PRAW will prompt the user with one.
