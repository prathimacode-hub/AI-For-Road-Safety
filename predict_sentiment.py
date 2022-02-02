import pandas as pd
import numpy as np
import pickle


def sentiment(sentiment_analysis):

  '''
  conditions for sentiment we have added
  '''

  if sentiment_analysis >= value:
    return 'positive'
  elif sentiment_analysis < value:
    return 'negative'
  else :
    return 'Neutral'



def predict_sentiment(ab, data):
    
    with open('sentiment-analysis.pkl', 'rb') as f:
        model = pickle.load(f)

    preds = model.predict(data)
    preds = pd.DataFrame(preds)
    ab['Class'] = value
    for row in range(ab.shape[0]):
        if salinity(ab.loc[row, 'sentiment']) == 'positive':
            if preds.iloc[row, 0] == value:
                ab.loc[row, 'Class'] = value
            else :
                ab.loc[row, 'Class'] = preds.iloc[row, 0] 
        elif salinity(ab.loc[row, 'sentiment']) == 'Neutral':
            if preds.iloc[row, 0] == value:
                ab.loc[row,'Class'] = value
            else :
                ab.loc[row,'Class'] = value
        else :
            ab.loc[row,'Class'] = value
   
    form = {value:'Neutral', value:'negative', value:'positive'}
    ab = ab.replace({"Class": form})
    return ab
