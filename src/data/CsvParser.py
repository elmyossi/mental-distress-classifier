import csv
import tldextract
import validators
from collections import Counter
from nltk import ngrams

class CsvParser:

    def __init__(self, csv_file):
        self.csv_file = csv_file

    def get_valid_urls(self):
        with open(self.csv_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader) # skip column names
            urls = [row[3] for row in csv_reader]
            valid_urls = [url for url in urls if validators.url(url)]
            return valid_urls

    def get_urls_by_domain_name(self):
        result = {}
        valid_urls = self.get_valid_urls()
        domains = [(tldextract.extract(url).domain, url) for url in valid_urls]
        for i in domains:
            result.setdefault(i[0], []).append(i[1])

        return result

    def get_domestic_family_posts(self):
        with open(self.csv_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)  # skip column names
            rows_with_domestic_violence = []
            for row in csv_reader:
                tags = row[8]
                if 'אלימות במשפחה' in set(tags.split(', ')):
                    rows_with_domestic_violence.append(row)

            return rows_with_domestic_violence

        return []

def main():
    parser = CsvParser("archive.csv")
    posts_of_domestic_violence = parser.get_domestic_family_posts()
    titles = [row[2] for row in posts_of_domestic_violence]
    words = [word for line in titles for word in line.split()]
    three_grams = list(ngrams(words, 3))
    four_grams = list(ngrams(words, 4))
    most_common_3_grams = Counter(three_grams).most_common(10)
    most_common_4_grams = Counter(four_grams).most_common(10)
    print('Total number of Domestic Violence Posts: {}'.format(len(posts_of_domestic_violence)))
    print('3 Grams:')
    for i in range(10):
        print('{}. "{}" - {} מופעים'.format(i+1, ' '.join(most_common_3_grams[i][0]), most_common_3_grams[i][1]))

    print('4 Grams:')
    for i in range(10):
        print('{}. "{}" - {} מופעים'.format(i+1, ' '.join(most_common_4_grams[i][0]), most_common_4_grams[i][1]))


if __name__ == "__main__":
    main()
