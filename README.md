# Skills evaluator mini-app

## Introduction

### Problematics
When you find a job you try to get skills required and then stude and practice to get skills you need for the 
certain job. But which skill set will help you most to get job with the highest salary possible?
I tried to create simple scripts and research if it is possible.

### Purpose
The main purpose is to create predictions for salary depending on skills required. I wanted to create ML models which 
are supposed to use real prepared data from job aggregators.

### Tasks
- get vacancies data set
- get skills from job description using ChatGPT
- train model and predict salary for skills

### What is inside
Few modules to parse list of job sites then get skills and salary then predict which skills will be the best for the 
highest salary.
It has 2 main packets:
- [indeed_project](https://github.com/jBuly4/skills_evaluator/blob/5b33252bdb45144a128da25f3b7f9d6a9f0208c9/indeed_project/indeed_project) - here you can find code which parses indeed.com
- [parser](https://github.com/jBuly4/skills_evaluator/blob/5b33252bdb45144a128da25f3b7f9d6a9f0208c9/parser) - this main package for parsing data, cleaning it and run predictor

## Version 0.0

## Requirements
- python 3.10.11
- see this [file](https://github.com/jBuly4/skills_evaluator/blob/5b33252bdb45144a128da25f3b7f9d6a9f0208c9/requirements.txt) to install all libraries needed

## Instructions
1. Clone this repo
2. Install requirements using
```bash
pip install -r requirements.txt
```
3. Get proxy from [scrapeops](https://scrapeops.io/app/register/main) and paste it api_key 
[settings.py](https://github.com/jBuly4/skills_evaluator/blob/1b66f445afb549c66ea0ef1bd29f3e4250587dd0/indeed_project/indeed_project/settings.py). 
Look for line 27 - here is the setting you need.
4. Run job parser (**remember that** for now only indeed.com is parsed):
```bash
scrapy crawl indeed
```
5. Set up api key for ChatGPT and add it to line 35 at [csv_cleaner](https://github.com/jBuly4/skills_evaluator/blob/5b33252bdb45144a128da25f3b7f9d6a9f0208c9/parser/clean_csv/csv_cleaner.py)
6. Set up path to your crawled indeed data file (line 134 at [csv_cleaner](https://github.com/jBuly4/skills_evaluator/blob/5b33252bdb45144a128da25f3b7f9d6a9f0208c9/parser/clean_csv/csv_cleaner.py))
7. Run csv_cleaner using ```bash python ./parser/clean_csv/csv_cleaner.py```
8. Run ```bash python ./parser/predictor/predictor.py```
9. Enjoy generated dataset and plots.

## Current results
PCA plot
![PCA plot](https://github.com/jBuly4/skills_evaluator/blob/main/parser/predictor/plots/PCA_top_10_skill_clusters_with_legend.png)

![Raw clusters for top-10 skills](https://github.com/jBuly4/skills_evaluator/blob/main/parser/predictor/plots/top_10_skill_clusters.png)

**Notification**:
Unfortunately for now I didn't find any correlation between extracted skills and salaries. It seems that I have some 
mistakes during data parsing and its evaluation with ML models. I guess that I should have to research skillset 
againts salary not separated skills but on the other side it would be hard to get excactly skillset from my data.

## How to get ChatGPT api-key:
1. **Please notice**: you have to pay for using api
2. In short:
   - Get account
   - Pay for Plus subscription (2$ might be enough for 1000 requests through scrapeops proxy)
   - For more details see official [info](https://help.openai.com/en/articles/7039783-how-can-i-access-the-chatgpt-api)

## Troubleshooting
For troubleshooting you need to be familiar with Python. At least at level - read code, understand logic.
If you have any issues - feel free to create issues for this project.

### FAQ
- Do I need to use scrapeops proxy?
  - No you don't need, you can use whatever proxy you want, but for now I tried only their proxy and did not tested 
    others (I didn't any tests, I know I'm bad LOL=) ) 
- Indeed scraper doesn't work correctly
  - Check the site structure if you see errors connected with requests and response
  - Check the logic inside functions - may be there is uncaptured bug
- Something wrong with predictor
  - Yea, it seems that there are a lot of troubles. Need a time to understnd how to fix it (and to learn ML..)

## LICENSE
- [MIT](https://github.com/jBuly4/skills_evaluator/blob/0a9b97352012d929752ea644feae8482c53b91d9/LICENSE)

## Changelog
Nothing is changed yet.

## Acknowledgments
I used this links and guides while creating skills_evaluator.

- https://arc.dev/developer-blog/python-developer-job-boards/
- https://github.com/indeedlabs/indeed-python
- https://medium.com/@alberto_moura/build-a-jobs-database-using-indeeds-api-8f95316be842
- https://realpython.com/build-a-content-aggregator-python/#demo-what-youll-build
- https://towardsdatascience.com/automate-your-job-search-with-python-and-github-actions-1dc818844c0
- https://scrapeops.io/python-scrapy-playbook/python-scrapy-indeed-scraper/
- https://scrapfly.io/blog/how-to-scrape-indeedcom/
- https://scrapeops.io/python-scrapy-playbook/python-scrapy-linkedin-jobs-scraper/
- https://scrapeops.io/web-scraping-playbook/
- https://www.scraperapi.com/blog/how-to-scrape-glassdoor/
- https://chat.openai.com/

### Useful links in one file
[Links](https://github.com/jBuly4/skills_evaluator/blob/main/some_sites.txt)
