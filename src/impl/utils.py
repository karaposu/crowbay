
import logging
import yaml
import re
logger = logging.getLogger(__name__)

def create_db_session(dependencies):


    db_session_factory = dependencies.session_factory
    db_session_maker = db_session_factory()
    db_session = db_session_maker()
    return db_session





