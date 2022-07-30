BASEDIR=$(dirname $0)
echo "Script location: ${BASEDIR}"
_d="$BASEDIR"
# shellcheck disable=SC2164
cd "$_d"
# shellcheck disable=SC2103
# going up two levels
cd ..
cd ..

source env/bin/activate
# Going back 1 level  
cd -

BASEDIR=$(dirname $0)
echo "Script location: ${BASEDIR}"
echo "Scraping the category: ${1}"
NEWS_PROJ_ENV=STAGE python3 news_scraper.py "$1" > logs/news_scraper_"$1".log 2>&1&