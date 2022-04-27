.PHONY: setup build install-build uninstall-build publish clean test lint run

# Setup Constants
POETRY_VERSION = 1.1.11
 

# Set up environment and install dependencies
setup:
	@echo Install Poetry Version $(POETRY_VERSION)
	[ -f ./poetry.lock ] && rm -r poetry.lock || echo lock file not found
	pip install --upgrade --force-reinstall 'poetry==$(POETRY_VERSION)'
	@echo 🧰 Installing  Dependencies 
	poetry install

# clean data 
clean:
	@echo 🧹 cleanup
	rm -r ./Data/Rating/*.json || echo dir file not found

# format code
lint:
	@echo ♻️ Reformatting Code
	poetry run black .

# run data pipeline
run:
	@echo 🚀 Running Procedure
	poetry run python main.py

# run tweet generate and publish 
publish:
	@echo 📣 Tweeting
	make generate 
	@echo Tweet insight
	cd ./src/TweetService/ && node tweet.js

tweet:
	@echo Tweet insight
	cd ./src/TweetService/ && node tweet.js

generate:
	@echo Remove Files in Tweets folder
	rm -r ./src/TweetService/Tweets/* || echo dir file not found
	@echo Generating Tweets
	cd ./src/TweetService/ && node generate.js 

host:
	@echo 🏠 Running Host
	cd ./src/TweetService/src/ && http-server -p 8080


	