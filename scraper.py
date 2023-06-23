from requests_html import HTMLSession
from latest_user_agents import get_random_user_agent
import json
from time import sleep

class ShopifyReviews:
    def __init__(self, app, rating):
        self.app = app
        self.rating = rating
        self.session = HTMLSession()
        self.headers = {'User-Agent': get_random_user_agent()}
        self.url = f'https://apps.shopify.com/{self.app}/reviews?rating={self.rating}&page='

    def pagination(self, page):
        r = self.session.get(self.url + str(page))
        if not r.html.find('.tw-py-lg'):
            return False
        else:
            return r.html.find('.tw-py-lg')
        
    def parse(self, reviews):
        total = []
        for review in reviews:
            title = review.find('.tw-break-words', first=True).text.replace('\n', '').strip()
            date = review.find('.tw-text-body-xs.tw-text-fg-tertiary', first=True).text
            rating = self.rating

            data = {
                'Title': title,
                'Rating': rating,
                'Date': date
            }
            total.append(data)
        return total
    
    def save(self, results):
        with open(f'{self.app}_reviews.json', 'w') as f:
            json.dump(results, f)
    

if __name__ == '__main__':
    review_scraper = ShopifyReviews('tiktok', 4)
    results = []
    for x in range(1, 27):
        print(f'Getting page', x)
        sleep(0.3)
        reviews = review_scraper.pagination(x)
        if reviews is not False:
            results.append(review_scraper.parse(reviews))
        else:
            print('No more pages')
            break
    
    review_scraper.save(results)



