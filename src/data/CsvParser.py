import csv
import tldextract
import validators


class CsvParser:

    def __init__(self, csv_file):
        self.csv_file = csv_file

    def get_valid_urls(self):
        with open(self.csv_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
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


def main():
    parser = CsvParser("archive.csv")
    urls_by_domain = parser.get_urls_by_domain_name()
    print(len(urls_by_domain.keys()))


if __name__ == "__main__":
    main()
