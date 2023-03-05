# pip install -r requirements.txt
NEWS_PROJ_ENV=STAGE python3 data_sanity.py > logs/data_sanity.log 2>&1&
bash scripts/news_scraper_script.sh automobile
bash scripts/news_scraper_script.sh business
bash scripts/news_scraper_script.sh entertainment
bash scripts/news_scraper_script.sh national
bash scripts/news_scraper_script.sh science
bash scripts/news_scraper_script.sh politics
bash scripts/news_scraper_script.sh startup
bash scripts/news_scraper_script.sh technology
bash scripts/news_scraper_script.sh world
bash scripts/news_scraper_script.sh sports
bash scripts/news_scraper_script.sh hatke
bash scripts/news_scraper_script.sh miscellaneous
bash scripts/news_scraper_script.sh