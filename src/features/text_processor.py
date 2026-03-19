import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
import re
from collections.abc import Generator
from pathlib import Path
class GurmukhiTokenizer:
  """
   Normalizes & filters the gurbani text and splits text into seperate words.

  Attributes:
  df(pd.DataFrame): The Gurbani Hymns Dataframe.
  target_column(str): The target column that will be used to normalize,clean,tokenize text.
  pattern(str): The regex pattern used to normalize text.
  replacement_text(str): The replacement text that will be used to normalize the text.
  filter_col(str): The column name that will be passed to clean and remove noise data.
  filter_word(str): The word that will be passed as an argumement to filter filter_col to remove noise data.
  """
  df:pd.DataFrame
  target_column:str
  pattern:str
  replacement_text:str
  filter_col:str
  filter_word:str
  def __init__(self,df: pd.DataFrame,target_column:str,pattern: str,replacement_text:str,filter_col:str,filter_word:str)-> None:
    """
    Args:
  df(pd.DataFrame): The Gurbani Hymns Dataframe.
  target_column(str): The target column that will be used to normalize,clean,tokenize text.
  pattern(str): The regex pattern used to normalize text.
  replacement_text(str): The replacement text that will be used to normalize the text.
  filter_col(str): The column name that will be passed to clean and remove noise data.
  filter_word(str): The word that will be passed as an argumement to filter filter_col to remove noise data.
    """
    logger_name = f"{__name__}.{self.__class__.__name__}"
    self.logger = logging.getLogger(logger_name)
    self.logger.info("Initialized Successfully.")
    self.df = df
    self.target_column = target_column
    self.pattern = pattern
    self.replacement_text = replacement_text
    self.filter_col = filter_col
    self.filter_word = filter_word
  def tokenize_and_filter(self)-> Generator[list[str],None,None]:

    """
    Normalizes & filters the gurbani text and splits text into seperate words.
    """
    gurbani_df = self.df.dropna(subset=[self.filter_col]).copy()
    gurbani_df = gurbani_df[gurbani_df[self.filter_col].ne(self.filter_word)]
    gurbani_df[self.target_column] = gurbani_df[self.target_column].str.replace(
        pat=self.pattern,
        repl=self.replacement_text,
        regex=True
    )
    gurbani_df[self.target_column] = gurbani_df[self.target_column].str.split()
    for token_list in gurbani_df[self.target_column]:
      yield token_list

if __name__ =='__main__':
  logging.basicConfig(
    level= logging.INFO,
    format='%(asctime)s |%(name)-s |%(levelname)s in %(filename)s:%(lineno)d: %(message)s',
    datefmt= "%Y-%m-%d %H:%M:%S",
    force=True
 )
  try:
    file_path = Path('/content/drive/MyDrive/Raag_Classification_ML_Project/data/interim/extracted_gurbani.csv')
    df = pd.read_csv(file_path)
  except FileNotFoundError as e:
    logging.info(f"Error: The file {file_path} was not found. Check the path {e}.")
  pattern = r'[^\u0A00-\u0A65\u0A70-\u0A7F\s]+'
  target_column = 'Hymn_Text'
  replacement_text = ""
  filter_col = 'Raag_label'
  filter_word = 'None'
  gurbani_tokenizer = GurmukhiTokenizer(df=df,target_column=target_column,pattern=pattern,replacement_text=replacement_text,filter_col=filter_col,filter_word=filter_word)
  gurbani_tokenizer.logger.info("Starting tokenization process...")
  all_tokenized_hymns = list(gurbani_tokenizer.tokenize_and_filter())
  gurbani_tokenizer.logger.info(f"Successfully tokenized {len(all_tokenized_hymns)} hymns.")
  print("\\nFirst 3 tokenized lists:")
  for i in range(3):
    print(all_tokenized_hymns[i])
