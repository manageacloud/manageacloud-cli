import os
import logging

import maccli.dao.api_auth


__version__ = '1.0a2'

# : The username used to authenticate with the API
user = maccli.dao.api_auth.load_from_file()[0] or os.environ.get('MAC_USER', None)

#: The ApiKey used to authenticate with the API
apikey = maccli.dao.api_auth.load_from_file()[1] or os.environ.get('MAC_APIKEY', None)

#: The API endpoint to use
base_url = os.environ.get('MAC_BASE_URL', "https://manageacloud.com/api/v1/")

logger = logging.getLogger("mac-cli")