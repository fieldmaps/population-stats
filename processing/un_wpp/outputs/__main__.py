from processing.un_wpp.outputs import merge
from processing.un_wpp.outputs.utils import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    merge.main()
