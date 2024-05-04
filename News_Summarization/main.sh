# pip install -r requirements.txt
# NEWS_PROJ_ENV=STAGE python3 data_sanity.py > logs/data_sanity.log 2>&1&
bash scripts/news_scraper_script.sh automobile
sleep 1m
bash scripts/news_scraper_script.sh business
sleep 1m
bash scripts/news_scraper_script.sh entertainment
sleep 1m
bash scripts/news_scraper_script.sh national
sleep 1m
bash scripts/news_scraper_script.sh science
sleep 1m
bash scripts/news_scraper_script.sh politics
sleep 1m
bash scripts/news_scraper_script.sh startup
sleep 1m
bash scripts/news_scraper_script.sh technology
sleep 1m
bash scripts/news_scraper_script.sh world
sleep 1m
bash scripts/news_scraper_script.sh sports
sleep 1m
bash scripts/news_scraper_script.sh hatke
sleep 1m
bash scripts/news_scraper_script.sh travel
sleep 1m
bash scripts/news_scraper_script.sh miscellaneous
sleep 1m
bash scripts/news_scraper_script.sh fashion
sleep 1m
bash scripts/news_scraper_script.sh