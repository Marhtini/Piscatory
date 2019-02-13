# PISCATORY!
# For Phishing Effectiveness!
# Note: TensorFlow support for Python 3.7 is bad. Use 3.6 if you want to use experimental features!
# @Marhtini

# TODO: Text Generation Tweaking (Epochs, Config Files, Temp)
# TODO: Ability to change threshold values
# TODO: Add Python Version Checking for TextGenRNN (Use 3.6 for now!)

print("Importing required modules... Please wait...")
import tweepy
from textblob import *
from pip._vendor.distlib.compat import raw_input
from urllib.request import *
from bs4 import BeautifulSoup as soup
import lxml
print("Loading Tensorflow backend... Please wait...")
import tensorflow
import textgenrnn
from newspaper import Article

def main():

    display_banner()
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


def display_banner():

    '''

    display_banner(): Well... it displays the banner.

    '''

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

    return 0


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

    url_dict = {}  # Dictonary with Numbered Key for Text Generation Selection
    url_dict_key = 0

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
            url_dict.update({url_dict_key:news_item.link.text})
            url_dict_key += 1
            #url_list.append(news_item.link.text) # Add to URL List
            print(news_item.pubDate.text)
            print(analyze.sentiment)
            print("\n")
        elif analyze.polarity < 0 and analyze.subjectivity < .5:
            print("Recommended! It's highly polarizing!")
            print(news_item.title.text)
            print(news_item.link.text)
            url_dict.update({url_dict_key: news_item.link.text})
            url_dict_key += 1
            #url_list.append(news_item.link.text)  # Add to URL List
            print(news_item.pubDate.text)
            print(analyze.sentiment)
            print("\n")
        elif analyze.subjectivity > .5 and analyze.polarity > 0:
            print("Recommended! It's highly subjective!")
            print(news_item.title.text)
            print(news_item.link.text)
            url_dict.update({url_dict_key: news_item.link.text})
            url_dict_key += 1
            #url_list.append(news_item.link.text)  # Add to URL List
            print(news_item.pubDate.text)
            print(analyze.sentiment)
            print("\n")

    text_generator_question = raw_input("Would you like to try to generate starter text? (EXPERIMENTAL) (y/n): ")
    if text_generator_question in ('y', 'n', 'ye', 'no', 'yes', 'Y', 'YE', 'YES', 'N', 'NO'):
        if text_generator_question in ('y', 'ye', 'yes', 'Y', 'YE', 'YES'):
            prepare_data(url_dict) # Pass the URL Dictionary
        elif text_generator_question in ('n', 'no', 'N', 'NO'):
            print("Continuing!")
        else:
            print("Invalid Input. Continuing!") # TODO: This is kind of lazy. Fix this with an actually while loop!

    main()


def prepare_data(url_dict):

    '''

    prepare_data(): Function to prepare data to be processed by the text_generator function. Note that in both this
    function as well as text_generator, there may be some heavier system load for model training. The function takes
    a dictionary of URLS to start with.

    '''

    valid_response = 0

    # IS the data already prepared? Is this a redundant step? AM I REDUNDANT?

    print("Here is the recommended URL listing:")
    for key in url_dict:
        print(str(key) + ": " + url_dict[key])

    # Deal with non-integers
    while True:
        user_url_choice = raw_input("\nWhich URL would you like to use? (Select Option 0 through " + str(len(url_dict) - 1) + "): ")
        try:
            int(user_url_choice)
            break
        except:
            print("Invalid Response! Please select a number between 0 and " + str(len(url_dict) - 1) + ".")

    while valid_response == 0:
        if int(user_url_choice) < 0 or int(user_url_choice) > len(url_dict):
            print("Invalid Response! Please select a number between 0 and " + str(len(url_dict) - 1) + ".")
        elif int(user_url_choice) >= 0 or int(user_url_choice) <= len(url_dict):
            # Logic to select item
            data_from_url = Article(str(url_dict[int(user_url_choice)]))
            data_from_url.download()
            data_from_url.parse()
            news_page_file = open("learnme.txt", "w")  # Get Ready to Write
            news_page_file.write(data_from_url.text)
            news_page_file.close()
            valid_response = 1
        else:
            print("Invalid Response! Please select a number between 0 and " + str(len(url_dict) - 1) + ".")

    text_generator()


def text_generator():

    '''

    text_generator() : Function to generate text from source data using TextGenRNN as starter text for phishing

    '''

    try:
        from textgenrnn import textgenrnn
    except ImportError:
        raise ImportError('[!] TextGenRNN import Error. Probably having to do with TensorFlow issues. Text Generation (EXPERIMENTAL) may not work!')

    # Generate the Text Now!
    generate_text = textgenrnn()
    generate_text.train_from_file('learnme.txt', num_epochs=30) # NOTE: TWEAK EPOCHS HERE
    generate_text.generate(20, temperature=0.2)  # NOTE: TWEAK MODEL SETTINGS HERE


if __name__ == "__main__":
    main()

