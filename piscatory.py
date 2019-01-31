# PISCATORY!
# For Phishing Effectiveness!
# @Marhtini

# TODO: Add Text Generation
# TODO: Ability to change threshold values
# TODO: Remove need to re-enter API Key every time

import tweepy
from textblob import *
from pip._vendor.distlib.compat import raw_input
from urllib.request import *
from bs4 import BeautifulSoup as soup
#import lxml   MAKE SURE TO INSTALL THIS VIA PIP


def main():
    print('\n><(((0>  ___  _____  ___   _____         _______  _____   _____          <0)))><')
    print('><(((0> |   |   |   |     |         /\      |    |     | |     | \     / <0)))><')
    print('><(((0> |___|   |   |___  |        /  \     |    |     | |_____|  \___/  <0)))><')
    print('><(((0> |       |       | |       / -- \    |    |     | |    \     |    <0)))><')
    print('><(((0> |     __|__  ___| |_____ /      \   |    |_____| |     \    |    <0)))><')
    print("><(((0>                                                                  <0)))><\n")
    print("Sentiment Analysis for Phishing!")
    print("@Marhtini")
    print("Using Twitter, the news, and TextBlob (NLP) to analyze the sentiment and polarity of subjects to")
    print("determine the potential effectiveness of a phishing ruse!")
    print("Polarization Range: -1.0 (Very Polarizing) to 1.0 (Not Very Polarizing)")
    print("Subjectivity Range: 0.0 (Very Objective) to 1.0 (Very Subjective)")
    print("\n")

    check_again = 0
    user_option = '0'
    user_decision = 0

    print("Please select an option: \n1. Keyword Search\n2. Top News Analysis\n3. Exit" + "\n")
    user_option = raw_input("Enter your Selection: ")

    # ADD OPTIONS HERE
    if user_option in ('1', '2', '3'):
        if user_option == '1':
            keyword_analysis()
        elif user_option == '2':
            top_news_analysis()
        elif user_option == '3':
            print("Thanks for stopping by!")
            quit()
    else:
        print("Invalid Selection!")
        main()

    while check_again == 0:
        user_decision = raw_input("Would you like to search for another keyword? (y/n)\n")
        if user_decision in ('y', 'n', 'ye', 'no', 'yes', 'Y', 'YE', 'YES', 'N', 'NO'):
            if user_decision in ('y', 'ye', 'yes', 'Y', 'YE', 'YES'):
                keyword_analysis()
            elif user_decision in ('n','no', 'N', 'NO'):
                main()
                check_again = 1
            else:
                print("Invalid Input Detected!\n")


def api_configure():

    """

    api_configure(): Takes user input of Twitter Consumer API Key, Consumer API Secret, Access Token
    and Access Token Secret.

    NOTE TO END USERS: Place your API Key Here!!!

    """

    key = 'SET KEY HERE'
    secret = 'SET SECRET HERE'
    token = 'SET TOKEN HERE'
    token_secret = 'SET TOKEN_SECRET HERE'

    return key, secret, token, token_secret


def keyword_analysis():

    """

    keyword_analysis(): Accepts api_configure return values and connects to the Twitter API via
    the tweepy library and OAuth.

    The function then retrieves a list of tweets containing the keywords entered by the user, and runs
    a sentiment analysis against them using TextBlob.

    """

    key, secret, token, token_secret = api_configure()
    polarity_avg = 0
    subjectivity_avg = 0

    authenticate = tweepy.OAuthHandler(key, secret)
    authenticate.set_access_token(token, token_secret)
    api = tweepy.API(authenticate)

    search_term = raw_input("Enter your Search Term:\n")
    pub_tweet_list = api.search(search_term, count=100) # Change Count Here! Note, potential Rate Limit

    for tweet in pub_tweet_list:
        #print(tweet.text)  ENABLE TO SEE THE TWEEETS!
        analyze = TextBlob(tweet.text)
        #print(analyze.sentiment)  ENABLE TO SEE THE SENTIMENT VALUE PER TWEET
        polarity_avg += analyze.polarity
        subjectivity_avg += analyze.subjectivity

    if len(pub_tweet_list) <= 0:
        print("No tweets found.\n")
        return -1

    polarity_avg = polarity_avg / len(pub_tweet_list)
    subjectivity_avg = subjectivity_avg / len(pub_tweet_list)
    print("Total tweets in the list:")
    print(len(pub_tweet_list))
    print("Polarity Average: " + str(polarity_avg) + "\n")
    print("Subjectivity Average: " + str(subjectivity_avg) + "\n")

    if polarity_avg < 0 and subjectivity_avg > .5:
        print("Keyword: " + search_term + " is HIGHLY Recommended! It's highly polarizing and highly subjective!")
        print(analyze.sentiment)

    elif polarity_avg < 0 and subjectivity_avg < .5:
        print("Keyword: " + search_term + " is Recommended! It's highly polarizing!")
        print(analyze.sentiment)

    elif subjectivity_avg > .5 and polarity_avg > 0:
        print("Keyword: " + search_term + " is Recommended! It's highly subjective!")
        print(analyze.sentiment)


def top_news_analysis():

    """

    top_news_analysis(): Retrieves an RSS feed, either the default https://news.google.com/news/rss
    or a feed entered by the user, parses and extracts the Title, Link, and Publish Date, and runs
    a sentiment analysis against each item using TextBlob.

    """

    user_news_source_choice = raw_input("Would you like to use a custom RSS news source? (y/n): ")
    if user_news_source_choice in ('y', 'n', 'ye', 'no', 'yes', 'Y', 'YE', 'YES', 'N', 'NO'):
        if user_news_source_choice in ('y', 'ye', 'yes', 'Y', 'YE', 'YES'):
            news_source = raw_input("Enter RSS URL: ")
            print("Using " + news_source + " as the News Source RSS.")
        elif user_news_source_choice in ('n', 'no', 'N', 'NO'):
            print("Using Default News Source RSS.")
            news_source = "https://news.google.com/news/rss"
        else:
            print("Using Default News Source RSS.\n")
            news_source = "https://news.google.com/news/rss"

    # TRY/EXCEPT to capture incorrect or missing URLS
    try:
        get_news = urlopen(news_source)
    except:
        print("Unknown URL. Using Default News Source RSS.\n")
        news_source = "https://news.google.com/news/rss"
        get_news = urlopen(news_source)

    read_news = get_news.read()
    get_news.close()
    formatted_page = soup(read_news, "xml")
    news_page = formatted_page.findAll("item")

    for news_item in news_page:
        analyze = TextBlob(news_item.title.text)
        if analyze.polarity < 0 and analyze.subjectivity > .5:
            print("HIGHLY Recommended! It's highly polarizing and highly subjective!")
            print(news_item.title.text)
            print(news_item.link.text)
            print(news_item.pubDate.text)
            print(analyze.sentiment)
            print("\n")
        elif analyze.polarity < 0 and analyze.subjectivity < .5:
            print("Recommended! It's highly polarizing!")
            print(news_item.title.text)
            print(news_item.link.text)
            print(news_item.pubDate.text)
            print(analyze.sentiment)
            print("\n")
        elif analyze.subjectivity > .5 and analyze.polarity > 0:
            print("Recommended! It's highly subjective!")
            print(news_item.title.text)
            print(news_item.link.text)
            print(news_item.pubDate.text)
            print(analyze.sentiment)
            print("\n")

    main()


if __name__ == "__main__":
    main()
    
    
