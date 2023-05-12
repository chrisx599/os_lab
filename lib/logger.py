import logging

# configurate logging
logging.basicConfig(
    level=logging.INFO,          # set logging level INFO
    format='%(asctime)s %(levelname)s: %(message)s',   # set loggin style
    datefmt='%Y-%m-%d %H:%M:%S', # set time style
    filename='system.log',      # set output log file name 
    filemode='a'                # set mode of input
)

# use logger to logging
logger = logging.getLogger(__name__)

# demo of how to use
logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('error message')
logger.critical('critial message')