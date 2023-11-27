import json
import re
from typing import Iterable

import scrapy

from urllib.parse import urlencode

from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor


"""
All info in Indeed could be found in script section (hidden json data):

<script id="mosaic-data" type="text/javascript">
    ...
    window.mosaic.providerData["mosaic-provider-jobcards"]={"metaData":
     ....
     "taxonomyAttributes":[{"attributes":[{"label":"Part-time","suid":"75GKK"}};"
    ...
</script>

"""


class IndeedSpider(scrapy.Spider):
    name = 'indeed'
    start_urls = ['https://www.indeed.com/q-python-developer-jobs.html']
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")

    def get_indeed_search_url(self, keyword, location, offset=0):
        params = {
            'q': keyword,
            'l': location,  # may be empty
            'filter': 0,
            'start': offset,
        }
        return 'https://www.indeed.com/jobs?' + urlencode(params)

    def start_requests(self) -> Iterable[Request]:
        keyword_list = ['python']
        location_list = ['']

        for keyword in keyword_list:
            for location in location_list:
                indeed_jobs_url = self.get_indeed_search_url(keyword, location)
                yield scrapy.Request(
                        url=indeed_jobs_url,
                        callback=self.parse_search_results,
                        meta={
                            'keyword': keyword,
                            'location': location,
                            'offset': 0
                        }
                )

    def parse_search_results(self, response):
        location = response.meta['location']
        keyword = response.meta['keyword']
        offset = response.meta['offset']
        script_tag = re.findall(
                r'window.mosaic.providerData\["mosaic-provider-jobcards"]=(\{.+?\});',
                response.text
        )
        if script_tag is not None:
            json_all = json.loads(script_tag[0])

            # paginate through pages
            if offset == 0:
                meta_data = json_all['metaData']['mosaicProviderJobCardsModel']['tierSummaries']
                number_of_results = sum(category['jobCount'] for category in meta_data)

                if number_of_results > 1000:
                    number_of_results = 50

                for offset in range(10, number_of_results + 10, 10):
                    url = self.get_indeed_search_url(keyword, location, offset)
                    yield scrapy.Request(
                            url=url,
                            callback=self.parse_search_results,
                            meta={
                                'keyword': keyword,
                                'location': location,
                                'offset': offset
                            }
                    )

            # extract jobs from search page
            job_lst = json_all['metaData']['mosaicProviderJobCardsModel']['results']
            for idx, job in enumerate(job_lst):
                if job.get('jobkey') is not None:
                    job_url = 'https://www.indeed.com/m/basecamp/viewjob?viewtype=embedded&jk=' + job.get('jobkey')
                    yield scrapy.Request(
                            url=job_url,
                            callback=self.parse_job,
                            meta={
                                'keyword': keyword,
                                'location': location,
                                'page': round(offset / 10) + 1 if offset > 0 else 1,
                                'position': idx,
                                'jobKey': job.get('jobkey'),
                            }
                    )

    def parse_job(self, response):
        location = response.meta['location']
        keyword = response.meta['keyword']
        page = response.meta['page']
        position = response.meta['position']
        script_tag = re.findall(r"_initialData=(\{.+?\});", response.text)

        if script_tag is not None:
            json_blob = json.loads(script_tag[0])
            job = json_blob["jobInfoWrapperModel"]["jobInfoModel"]
            yield {
                'keyword': keyword,
                'location': location,
                'page': page,
                'position': position,
                'company': job.get('companyName'),
                'jobkey': response.meta['jobKey'],
                'jobTitle': job.get('jobTitle'),
                'jobDescription': job.get('sanitizedJobDescription').get('content') if job.get(
                    'sanitizedJobDescription'
                    ) is not None else '',
            }


    # def parse(self, response):
    #     # Extract the JavaScript object from the page
    #     script_text = response.xpath("//script[contains(., 'results')]/text()").get()
    #     json_data = re.search(r'"results": (\[.*?\])\s*,\s*"pagination', script_text, re.S)
    #     install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    #
    #     if json_data:
    #         # Load the data as a JSON object
    #         job_listings = json.load(json_data.group(1))
    #
    #         # Iterate through the job listings
    #         for job in job_listings:
    #             salary_info = job.get('extractedSalary')
    #             if salary_info:
    #                 salary = f"{salary_info['min']} - {salary_info['max']} {salary_info['type']}"
    #                 job_description_link = job.get('link')
    #
    #                 # Follow the job description link
    #                 if job_description_link:
    #                     yield response.follow(job_description_link, self.parse_job_description, meta={'salary': salary})
    #
    # def parse_job_description(self, response):
    #     # Extract job description
    #     description = response.xpath('//div[@id="jobDescriptionText"]//text()').getall()
    #     description = ' '.join(description).strip()
    #
    #     yield {
    #         'estimated_salary': response.meta['salary'],
    #         'description': description
    #     }


# # Run the spider
# process = CrawlerProcess(settings={
#     'FEED_FORMAT': 'json',
#     'FEED_URI': 'jobs.json'
# })
#
# process.crawl(IndeedSpider)
# process.start()
