#!/bin/bash

CRAWLER_HOME=/opt/stackoverflow

TODAY=$(date +%Y-%m-%d)

cd $CRAWLER_HOME

scrapy crawl stackoverflow -o $CRAWLER_HOME/data/json/$TODAY.json -t json &>/var/log/scrapy.log
