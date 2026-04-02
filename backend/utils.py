import os
import logging

def setup_logging(level=logging.INFO):
    """
    Standard logger setup for the entire application.
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger("SmartDataTool")

def ensure_directory(path):
    """
    Ensures that a directory exists, creating it if necessary.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path

def sanitize_filename(filename):
    """
    Removes characters that aren't allowed in file names.
    """
    return "".join([c for c in filename if c.isalnum() or c in (' ', '.', '_')]).strip().replace(' ', '_')
