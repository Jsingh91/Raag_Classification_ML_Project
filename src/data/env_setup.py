import sys
from pathlib import Path
import logging
class ProjectEnvironmentManager:
  """
  Creates the environment needed for a project.

  Attributes:
      logger(logging.Logger): The logger instance for tracking events.
      is_colab (bool): Flag indicating if the execution environment is Google Colab.
      base_path (pathlib.Path): The root directory path for the project.
  """
  def __init__(self)-> None:
    logger_name = f"{__name__}.{self.__class__.__name__}"
    self.logger = logging.getLogger(logger_name)
    self.logger.info(f"Initialized Successfully")
    self.is_colab = 'google.colab' in sys.modules
    if self.is_colab:
      self.base_path = Path('/content/drive/MyDrive')
    else:
      self.base_path = Path.cwd()
  def _mount_drive(self)-> None:
    """
    Mounts drive to Google Colab.
    """
    if self.is_colab:
      try:
        from google.colab import drive
        drive.mount('/content/drive')
        self.logger.info('Drive Successfully Mounted!')
      except Exception as e:
        self.logger.error(f"Failed to mount drive: {e}")
  def _build_directory_tree(self) -> None:
    """
    Creates the Cookiecutter industry standard folder structure.
    """
    self.logger.info("Starting construction of Cookiecutter structure...")
    self.folder_blueprint = [
'Raag_Classification_ML_Project/data/raw',

'Raag_Classification_ML_Project/data/interim',

'Raag_Classification_ML_Project/data/processed',

'Raag_Classification_ML_Project/notebooks',

'Raag_Classification_ML_Project/src/data',

'Raag_Classification_ML_Project/src/features',

'Raag_Classification_ML_Project/src/models'
]
    self.logger.info(f"Blueprint loaded. Ready to build at: {self.base_path}")
    for folder in self.folder_blueprint:
      target_path = self.base_path/folder
      target_path.mkdir(parents=True, exist_ok=True)
      self.logger.info(f"Verified/Created directory: {target_path}")
  def setup(self)-> None:
    """Executes the complete environment setup workflow."""
    self.logger.info("Initializing project environment setup...")
    self._mount_drive()
    self._build_directory_tree()
    self.logger.info("Environment setup complete.")
