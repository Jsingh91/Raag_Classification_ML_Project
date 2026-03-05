import sys
from pathlib import Path
import logging
from collections.abc import Generator
class ProjectEnvironmentManager:
  """
  Creates the environment needed for a project.

    Args:
        project_name (str): The name of the project. Defaults to "Project_Name".

    Attributes:
        project_name (str): The name of the project.
        logger (logging.Logger): The logger instance for tracking events.
        is_colab (bool): Flag indicating if the execution environment is Google Colab.
        base_path (Path): The root directory path for the project.
        folder_blueprint (list[str]): The standard Cookiecutter directory paths.
  """
  def __init__(self, project_name: str = "Project_Name")-> None:
    self.project_name = project_name
    logger_name = f"{__name__}.{self.__class__.__name__}"
    self.logger = logging.getLogger(logger_name)
    self.logger.info(f"Initialized Successfully")
    self.is_colab = 'google.colab' in sys.modules
    self.base_path = Path('/content/drive/MyDrive') if self.is_colab else Path.cwd()
    self.folder_blueprint: list[str] = [
f'{self.project_name}/data/raw',

f'{self.project_name}/data/interim',

f'{self.project_name}/data/processed',

f'{self.project_name}/notebooks',

f'{self.project_name}/src/data',

f'{self.project_name}/src/features',

f'{self.project_name}/src/models'
]
    
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
    self.logger.info(f"Blueprint loaded. Ready to build at: {self.base_path}")
    self.logger.info("Starting construction of Cookiecutter structure...")
    for target_path in self._generate_blueprint():
      try:
        target_path.mkdir(parents=True, exist_ok=True)
        if 'src' in target_path.parts:
          (target_path/"__init__.py").touch(exist_ok=True)
        self.logger.info(f"Verified/Created directory: {target_path}")
      except OSError as e:
        self.logger.error(f"Failed to create directory {target_path}: {e}")
    
    

  def _generate_blueprint(self)-> Generator[Path, None, None]:
    """
    Generates the standard Cookiecutter project directory paths one at a time.

    Yields:
    Path: The next directory path to be created in the project architecture.

    """
   
    for folder in self.folder_blueprint:
      target_path = self.base_path/folder
      yield target_path


  def setup(self)-> None:
    """Executes the complete environment setup workflow."""
    self.logger.info("Initializing project environment setup...")
    self._mount_drive()
    self._build_directory_tree()
    self.logger.info("Environment setup complete.")
if __name__ == '__main__':
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s |%(name)-s |%(levelname)s in %(filename)s:%(lineno)d: %(message)s',
    datefmt= "%Y-%m-%d %H:%M:%S",
    force=True
  )
  env_manager = ProjectEnvironmentManager(project_name="Raag_Classification_ML_Project")
  env_manager.setup()
