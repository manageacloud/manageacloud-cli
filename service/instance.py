import auth
import dao.api_instance

def list():
    """
        List available instances in the account
    """
    auth_header = auth.get_auth_header()
    dao.api_instance.get_list(auth_header)


