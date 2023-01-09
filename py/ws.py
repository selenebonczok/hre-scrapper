import wscrapper
import scrapconf
import pandas as pd
import misc
import requests 
import bs4

#df = wscrapper.main(scrapconf.MainAI, scrapconf.OutputAI)
#df.to_csv("ai_full.csv", escapechar = "\\")

# Page 872 has a bad gateway

uk = scrapconf.MainUKEnglish
uko = scrapconf.OutputUKEnglish
# uk.url_head = "https://www.amnesty.org/en/search/page/"
uk.url_head = "https://www.amnesty.org.uk/search/%20a?type=article&sort_by=search_api_relevance&page="

df = wscrapper.create_data_by_pages(1, 2, uk, uko)
