from django.http import HttpResponse, JsonResponse
import requests
import json
import os
from django.conf import settings

def get_guardian_data():
  base_url = settings.GUARDIAN_BASE_URL
  api_key = settings.GUARDIAN_API_KEY
  response = requests.get(f"https://{base_url}/search?tag=environment/energyefficiency&api-key={api_key}")

  if response.status_code == 200:
    data = response.json()
    articles = data.get('response').get('results')

    guardian_list = []
    if articles:
      for idx, article in enumerate(articles):
        guardian_list.append(f"{article.get('webTitle')}:{article.get('webUrl')};")
      return HttpResponse(guardian_list, content_type="text/plain")
    else:
      return HttpResponse("No Guardian articles found.")
  else:
    print(f"Failed to fetch articles. Status code: {response.status_code}")

def get_nyt_articles():
  base_url = settings.NYT_BASE_URL
  api_key = settings.NYT_API_KEY
  response = requests.get(f"https://{base_url}/svc/search/v2/articlesearch.json?fq=news_desk:climate&api-key={api_key}")

  if response.status_code == 200:
    article_json = response.json()
    articles = article_json.get('response').get('docs')

    nyt_list = []
    if articles:
      for idx, article in enumerate(articles):
        nyt_list.append(f"{article.get('headline').get('main')}:{article.get('web_url')};")
      return HttpResponse(nyt_list, content_type="text/plain")
    else:
      return HttpResponse("No NYT articles found.")
  else:
    print(f"Failed to fetch articles. Status code: {response.status_code}")

def index(request):
  guardian = get_guardian_data()
  nyt = get_nyt_articles()

  combined_articles = HttpResponse(guardian, content_type='text/plain')
  nyt_res = HttpResponse(nyt, content_type='text/plain')
  combined_articles.write(nyt_res.content)
  return combined_articles