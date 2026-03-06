from pathlib import Path
import logging
import zipfile
class SikhJSDataIngestor:
  """
    Ingests and extracts the SikhJS raw data archive.
    Attributes:
        zip_path (Path): Path to the Zip Folder.
        target_dir (Path): Path to the directory where the files will be extracted.
        target_folder (str): Name of the path from where the files will be extracted from.
  """
  zip_path:Path
  target_dir:Path 
  target_folder:str

  def __init__(self,zip_path:Path,target_dir:Path,target_folder:str)-> None:
     """
     Args:
        zip_path (Path): Path to the Zip Folder.
        target_dir (Path): Path to the directory where the files will be extracted.
        target_folder (str): Name of the path from where the files will be extracted from.
     """
     logger_name = f"{__name__}.{self.__class__.__name__}"
     self.logger = logging.getLogger(logger_name)
     self.logger.info(f"Initialized Successfully")
     self.zip_path = zip_path
     self.target_dir = target_dir
     self.target_folder = target_folder
  
    
  def extract_target_files(self)-> None:
      """
      Extracts the 'Ang' files that have the gurbani information.
      Raises:
      FileNotFoundError: If the specified zip archive cannot be found.
      zipfile.BadZipFile: If it is not a valid or a reabable file.
      Exception: Any unexpected error happens during extraction.

      """
      try:
        if self.target_dir.exists():
          self.logger.info("Directory already extracted. Skipping unzip process.")
          return
        else:
          self.logger.info(f"Target Directory not found. Extracting to {self.target_dir}")
        with zipfile.ZipFile(file=self.zip_path,mode='r') as my_zip:
          all_files = my_zip.namelist()
          files_to_extract = (file for file in all_files if file.startswith(self.target_folder))
          my_zip.extractall(path=self.target_dir, members=files_to_extract)
        self.logger.info("Unpacking complete!")
      except FileNotFoundError as e:
        self.logger.error(f"We could not find the ZIP file at {self.zip_path}. Please check the path! {e}")
      except zipfile.BadZipFile as e:
        self.logger.exception(f"The file exists, but it is not a valid or readable ZIP file. {e}")
      except Exception as e:
        self.logger.error(f"An unexpected error occured during extraction: {e}")
if __name__ == '__main__':
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s |%(name)-s |%(levelname)s in %(filename)s:%(lineno)d: %(message)s',
    datefmt= "%Y-%m-%d %H:%M:%S",
    force=True
  )
  zip_path = Path('/content/drive/MyDrive/Raag_Classification_ML_Project/data/raw/SikhJS-0.7.0.zip')
  target_dir = Path('/content/drive/MyDrive/Raag_Classification_ML_Project/data/raw/SikhJS_Extracted')
  target_folder = 'SikhJS-0.7.0/assets/docs/json/SGGS/Ang'
  data_ingestor = SikhJSDataIngestor(zip_path=zip_path,target_dir=target_dir,target_folder=target_folder)
  data_ingestor.extract_target_files()

