# streamlit-twitter-stream
Live stream tweets based on keywords to database using SQLAlchemy. Tweets are assigned a sentiment score and data is presented via streamlit.
## Requiremnts

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```

## Usage

Environment variables must be set as per config.py for DB and Tweepy settings.

Streaming:

```bash
python run_stream.py "Keyword1,Keyword2"
```

Streamlit app
```bash
streamlit run app,py
```
