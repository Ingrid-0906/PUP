# -*- coding: utf-8 -*-
"""cats.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YyWdLBMxXbqqb0zrKrLQaLbR4o8rc4c2
"""
"""# Projeto Machine Learning Allcart - Product Categorization
Author: Ingrid Cadu<br>
Data: Sept 07, 2022<br>
<br>
The categorization takes the 3 last categories, however the 3rd column is discarted.<br>
E.g.<br>
Beverages › Beverage Syrups & Concentrates › Concentrates<br>
I have token:<br>
Beverages › Beverage Syrups & Concentrates›
"""

""" Windows does not requires this but colab, does:
import requests

# Importing darth.py from github / Delayed 44m
url = 'https://raw.githubusercontent.com/Ingrid-0906/Obiwan_2022/main/darth.py'
red = requests.get(url)
with open('darth.py', 'w') as filer:
  filer.write(red.text)
  
import darth as dt
"""

#opening model
import joblib
import requests

# Importing darth.py from github / Delayed 44m
url = 'https://raw.githubusercontent.com/Ingrid-0906/Obiwan_2022/main/darth.py'
red = requests.get(url)
with open('darth.py', 'w') as filer:
  filer.write(red.text)
  
import darth as dt

# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

class cats:
  def __init__(self, title):
    self.title = title
    
  def prepare(self, excluded="‘.%/)("):
    """ 
    (str) -> list(str)
    """
    self.title = dt.encode_string(self.title)
    self.title = dt.tokenize_title_string(self.title,'')
    self.title = dt.remove_words_list(self.title, set(dt.stopwords.words('english')))
    self.title = dt.remove_numeric_list(self.title)
    self.title = dt.stemming(self.title)
    self.title = dt.remove_chars(self.title)
    self.title = ' '.join(self.title)
    return self
    
    # change the dir! download the code and models in folder and send to him! I still need to conclude the personal care models
    
  def categorize_grocery(self):
    accuracy = 0
    modelNumber = 1
    results = list()
    api_grocery = dt.vectorizer.transform([self.title])
    for category in dt.data_frame.columns[1:]:
      filename = "/content/drive/MyDrive/Colab Notebooks/PUP/model_obiwan/"+str(modelNumber)+"model.sav"
      model = joblib.load(filename) # loading already saved model
      modelNumber += 1
      # calculating test accuracy
      prediction = model.predict(api_grocery)
      likely = model.decision_function(api_grocery)
      if prediction==1:
        #print('CATEGORY {} -> {}'.format(category,likely))
        results.append(category)
    return results

"""# Testing with function"""

# Function to classify if grocery or personal product
def CATS(word):
  w = cats([word]).prepare().categorize_grocery()
  if len(w)>1:
    w = w[:2]
  else:
    w = ['Other']
  return w
