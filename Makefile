install:

	pip install -r requirements.txt
	python -m nltk.downloader stopwords

run:

	set FLASK_APP=app.py&& set FLASK_ENV=development&& flask run --host=0.0.0.0 --port=3000
