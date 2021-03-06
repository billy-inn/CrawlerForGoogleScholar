#!/bin/bash

cd crawler/crawler
conf=conf

if [ $1 = 1 ]; then
	if [ $# = 3 ]; then
		echo $3 > ${conf}
		echo $2 >> ${conf}
		echo "mode 1 is chosen."
		echo "The start url is $2."
		echo "The target database is $3."
		scrapy crawl 1
	else
		echo "usage: run 1 start_url target_database"
	fi
elif [ $1 = 2 ]; then
	if [ $# = 4 ]; then
		echo $2 > ${conf}
		echo $3 >> ${conf}
		echo $4 >> ${conf}
		echo "mode 2 is chosen."
		echo "The profile database is $2."
		echo "The start index is $3."
		echo "The finish index is $4."
		scrapy crawl 2
	else
		echo "usage: run 2 profile_database start_index finish_index"
	fi
elif [ $1 = 3 ]; then
	echo "mode 3"
else
	echo "invaild mode!"
fi
