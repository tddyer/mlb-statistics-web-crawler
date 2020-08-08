import scrapy


class CubsSpider(scrapy.Spider):
    name = "cubs"

    def start_requests(self):
        urls = [
            'https://www.mlb.com/stats/chicago-cubs/at-bats?playerPool=ALL'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = '%s.txt' % page
        names = response.css('span.full-3fV3c9pF::text').getall()
        i = 0
        with open(filename, 'w') as f:
            while i < len(names) - 1:
                f.write(names[i] + ' ' + names[i + 1] + '\n')
                i += 2
        self.log('Saved file %s' % filename)
