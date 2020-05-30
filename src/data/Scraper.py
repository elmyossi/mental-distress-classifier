import tldextract
from lxml import html
import requests
import os


class Scraper:
    def __init__(self, url):
        self.url = url
        self.domain = tldextract.extract(url).domain

    # TODO Yossi - should we use type str or unicode?
    def scrape(self):

        if self.domain == 'stips':
            return self.scrape_from_stips()

        elif self.domain in ['askp', 'askpeople']:
            return self.scrape_from_askp()

        elif self.domain == 'twitter':
            return self.scrape_from_twitter()

        else:
            raise NotImplementedError()

    def scrape_from_stips(self):
        page = requests.get(self.url, verify=False)
        tree = html.fromstring(page.content)
        title_elements = tree.xpath('//*[@id="item-title"]/h1')
        body_elements = tree.xpath('//*[@id="item-title"]/div[1]/text()')

        title = ""
        if len(title_elements) > 0:
            title = title_elements[0].text

        body = ""
        if len(body_elements) > 0:
            body = os.linesep.join([elem.encode('utf-8').strip() for elem in body_elements])

        return title + " : " + body

    def scrape_from_askp(self):
        page = requests.get(self.url)
        tree = html.fromstring(page.content)
        title_elements = tree.xpath('//*[@id="h1_question_title"]')
        body_elements = tree.xpath('//*[@id="div_question_content"]/div[1]/div[1]/p/text()')

        title = ""
        if len(title_elements) > 0:
            title = title_elements[0].text

        body = ""
        if len(body_elements) > 0:
            body = os.linesep.join([elem.encode('utf-8').strip() for elem in body_elements])

        return title + " : " + body

    def scrape_from_twitter(self):
        pass


def main():
    # scraper_stips = Scraper("https://stips.co.il/ask/5444151")
    # scraper_stips.scrape()

    scraper_askp = Scraper('https://www.askpeople.co.il/question/107279')
    scraper_askp.scrape()


if __name__ == "__main__":
    main()
