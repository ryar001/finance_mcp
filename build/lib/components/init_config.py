import yaml # Import yaml
from pathlib import Path # Import Path
from src.components.logging_utils import LoggingUtils # Import LoggingUtils
# --- Logging Setup ---
settings_path = Path(__file__).parent / 'settings.yml' # Adjust path to settings.yml
with open(settings_path, 'r') as f:
    settings = yaml.safe_load(f)

log_settings = settings.get('log_setting', {})
log_file = log_settings.get('log_file')
log_dir = log_settings.get('log_dir')
log_level = log_settings.get('log_level')
print_output = log_settings.get('print_output', False) # Default to False if not specified

log_utils = LoggingUtils(
    log_file=log_file,
    log_dir=log_dir,
    log_level=log_level,
    print_output=print_output
)
logger = log_utils.get_logger()
# --- End Logging Setup ---
