from json.decoder import JSONDecodeError
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import logging
from collections.abc import Generator
class GurbaniJsonScriptExtractor:
  """
  Parses the Json files and extracts specific keys(columns) names and their respective values to convert this data into a pandas dataframe.

  Attributes:
  file_path (Path): Path to the Json files that will be parsed to extract specific data.

  """
  file_path:Path

  def __init__(self,file_path:Path)-> None:
    """
    Args:
    file_path (Path): Path to the Json files that will be parsed to extract specific data.

    """
    logger_name = f"{__name__}.{self.__class__.__name__}"
    self.logger = logging.getLogger(logger_name)
    self.logger.info("Initialized Successfully.")
    self.file_path = file_path
  def extract_json_data(self) -> Generator[tuple[str,str],None,None]:
    """
    Parses and extracts specific data from json files.
    Raises:
    json.JSONDecodeError: If the files being parsed are invalid JSON.
    FileNotFoundError: If the specified file path cannot be found.
    """
    try:
      self.logger.info("Starting JSON extraction generator...")
      for specific_file_path in self.file_path.glob("Ang*.json"):
        with open(file=specific_file_path,mode='r') as json_file:
          data = json.load(json_file)
        for file in data:
          melody_dict = file.get("melody") or {}
          label_value = melody_dict.get("melody")
          feature_value = file.get("text")
          yield label_value,feature_value
    except json.JSONDecodeError as e:
      self.logger.error(f"JSON Error:{e.msg}")
      self.logger.error(f"Error at line:{e.lineno}, column{e.colno}")
    except FileNotFoundError as e:
      self.logger.error(f"File path does not exist at {self.file_path}. Please check the path {e}.")

if __name__ == '__main__':
  logging.basicConfig(
      level= logging.INFO,
      format='%(asctime)s |%(name)-s |%(levelname)s in %(filename)s:%(lineno)d: %(message)s',
      datefmt= "%Y-%m-%d %H:%M:%S",
      force=True
  )
  file_path = Path('/content/drive/MyDrive/Raag_Classification_ML_Project/data/raw/SikhJS_Extracted/SikhJS-0.7.0/assets/docs/json/SGGS')
  gurbani_data_extractor = GurbaniJsonScriptExtractor(file_path=file_path)
  extracted_records = list(gurbani_data_extractor.extract_json_data())
  df = pd.DataFrame(extracted_records,columns=['Raag_label', 'Hymn_Text'])
  logging.info(f"DataFrame built successfully with {len(df)} records.")
  print(df.head())
  output_path = Path("/content/drive/MyDrive/Raag_Classification_ML_Project/data/interim/extracted_gurbani.csv")
  try:
    gurbani_data_extractor.logger.info(f"Saving extracted data to {output_path}")
    df.to_csv(output_path,index=False)
    gurbani_data_extractor.logger.info("Data Successfully saved to interim storage.")
    
  except OSError as e:
    gurbani_data_extractor.logger.error(f"Failed to save data to disk: {e}")  
