BASEDIR=$(dirname $0)
echo "Script location: ${BASEDIR}"
_d="$BASEDIR"
# shellcheck disable=SC2164
cd "$_d"
# shellcheck disable=SC2103
# going up two levels
cd ..
git config --global user.email "trehansalil1@gmail.com"
git config --global user.name "Salil Trehan"
pip install -r requirements.txt
cd ..

source env/bin/activate
# Going back 1 level  
cd -

BASEDIR=$(dirname $0)
echo "Script location: ${BASEDIR}"


# if $1 is not set, then set it to "general"
if [ -z "$1" ]; then
    echo "No category specified. Setting it to 'general'"
    category="general"
    echo "Scraping the category: ${category}"
    NEWS_PROJ_ENV=STAGE python3 news_scraper.py > logs/news_scraper_"$category".log 2>&1&
else
    echo "Scraping the category: ${1}"
    category="$1"
    NEWS_PROJ_ENV=STAGE python3 news_scraper.py "$1" > logs/news_scraper_"$1".log 2>&1&
fi

# 