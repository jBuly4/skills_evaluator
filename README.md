# Skills evaluator app
Few modules to parse list of job sites, get skills and salary then predict which skills will be the best for the 
highest salary.

Unfortunately for now I didn't find any correlation between extracted skills and salaries.

How to use:
1. Clone thi repo
2. Install requirements using
```bash
pip install -r requirements.txt
```
3. Get proxy from scrapeops and paste it to line 27 at ./indeed_project/indeed_project/settings.py
4. Run job parser (for now only indeed.com is parsed):
```bash
scrapy crawl indeed
```
5. Set up api key for ChatGPT and add it to line 35 at csv_cleaner (/parser/clean_csv)
6. Set up path to your crawled indeed data file (line 134 at csv_cleaner (/parser/clean_csv))
7. Run csv_cleaner using ```bash python ./parser/clean_csv/csv_cleaner.py```
8. Run ```bash python ./parser/predictor/predictor.py```
9. Enjoy generated dataset and plots.

## Current results
PCA plot
[PCA plot](![PCA_top_10_skill_clusters_with_legend.png](https://github.com/jBuly4/skills_evaluator/blob/main/parser/predictor/plots/PCA_top_10_skill_clusters_with_legend.png)

[Raw clusters for top-10 skills](![top_10_skill_clusters.png](https://github.com/jBuly4/skills_evaluator/blob/main/parser/predictor/plots/top_10_skill_clusters.png))

### Useful links and sites I used
[Links]([some_sites.txt](some_sites.txt))