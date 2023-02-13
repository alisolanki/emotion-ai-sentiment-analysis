from django.shortcuts import render
# from main import checker
import tweepy

# Create your views here.
def index(request):
    query = ""
    lang = "en"
    min_retweets = 0
    min_faves = 0
    min_replies = 0
    max_tweets = 100
    filter_replies = False
    
    context = {
        'query': query.capitalize(),
        'lang': lang,
        'min_retweets': min_retweets,
        'min_faves': min_faves,
        'min_replies': min_replies,
        'max_tweets': max_tweets,
        'filter_replies': filter_replies,
        'polarity': 0.5,
        'subjectivity': 0.5,
    }
    resultModel = {
        'positivePerc': 0.0,
        'negativePerc': 0.0,
        'neutralPerc': 0.0,
        'positiveTweets': [],
        'negativeTweets': [],
        'neutralTweets': [],
    }
    if request.method == 'POST':
        context['query'] = request.POST.get('query').capitalize() if request.POST.get('query').capitalize() != None else " "
        context['lang'] = request.POST.get('lang') if request.POST.get('lang') != None else "en"
        context['min_retweets'] = int(request.POST.get('min_retweets')) if int(request.POST.get('min_retweets')) > 0 else 0
        context['min_faves'] = int(request.POST.get('min_faves')) if int(request.POST.get('min_faves')) > 0 else 0
        context['min_replies'] = int(request.POST.get('min_replies')) if int(request.POST.get('min_replies')) > 0 else 0

        context['max_tweets'] = int(request.POST.get('max_tweets')) if int(request.POST.get('max_tweets')) > 1 else 1
        if int(request.POST.get('max_tweets')) > 5000:
            context['max_tweets'] = 5000

        context['polarity'] = float(request.POST.get('polarity'))
        if float(request.POST.get('polarity')) > 1:
            context['polarity'] = 1
        elif float(request.POST.get('polarity')) < 0:
            context['polarity'] = 0

        context['subjectivity'] = float(request.POST.get('subjectivity')) if float(request.POST.get('subjectivity')) != None else 0
        if float(request.POST.get('subjectivity')) > 1:
            context['subjectivity'] = 1
        elif float(request.POST.get('subjectivity')) < 0:
            context['subjectivity'] = 0

        if request.POST.get('filter_replies') == 'on':
            context['filter_replies'] = True
        
        print(context)
        
        resultModel = checker(context)
        #resultModel = {"positivePerc", "negativePerc", "neutralPerc",
        #   "positiveTweets", "negativeTweets", "neutralTweets"}
    print("resultModel: ", resultModel)
    return render(request, 'home.html', {'context': context,'resultModel': resultModel})