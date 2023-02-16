from transformers import pipeline
import pandas as pd
import re

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                    "]+", re.UNICODE)
    return re.sub(emoj, '', data)


def preprocess(text):

    text=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
    text = text.lower()
    return text  


classifier = pipeline("zero-shot-classification",model="facebook/bart-large-mnli")
options=["Cricket","Undefined"]
hypothesis_template = "The topic of this TikTok is {}."




df=pd.read_csv("training/cricket-11456.csv")

print(df.columns)

desc=df['com.ss.android.ugc.trill:id/bc5'].to_list()

for description in desc:
    try:
        text=remove_emojis(description)
    except:
        text="Unrecognized"
    text=preprocess(text)
    if text== "":
        text="Empty"
    print(text)
    res=classifier(sequences=text, candidate_labels= options, hypothesis_template=hypothesis_template)

    print(res["scores"])

