import zipfile
from pathlib import Path
import logging
class SikhJSDataIngestor:
  """
  Ingests and extracts the SikhJS raw data archive.
  """
  def __init__(self)-> None:
    logger_name = f"{__name__}.{self.__class__.__name__}"
    self.logger = logging.getLogger(logger_name)
    self.logger.info(f"Initialized Successfully")
    self.zip_path = Path('/content/drive/MyDrive/Raag_Classification_ML_Project/data/raw/SikhJS-0.7.0.zip')
    self.target_dir = Path("/content/drive/MyDrive/Raag_Classification_ML_Project/data/raw/SikhJS_Extracted")
    
  def extract_target_files(self)-> None:
      """
      Extracts the 'Ang' files that have the gurbani information.

      """
      try:
        if self.target_dir.exists():
          self.logger.info("Directory already extracted. Skipping unzip process.")
          return
        else:
          self.logger.info(f"Target Directory not found. Extracting to {self.target_dir}")
        with zipfile.ZipFile(file=self.zip_path,mode='r') as my_zip:
          all_files = my_zip.namelist()
          files_to_extract = [file for file in all_files if file.startswith('SikhJS-0.7.0/assets/docs/json/SGGS/Ang')]
          self.logger.info(f"Found {len(files_to_extract)} Gurbani Json files.")
          my_zip.extractall(path=self.target_dir, members=files_to_extract)
        self.logger.info("Unpacking complete!")
      except FileNotFoundError as e:
        self.logger.error(f"We could not find the ZIP file at {self.zip_path}. Please check the path! {e}")
      except zipfile.BadZipFile as e:
        self.logger.exception(f"The file exists, but it is not a valid or readable ZIP file. {e}")
      except Exception as e:
        self.logger.error(f"An unexpected error occured during extraction: {e}")

