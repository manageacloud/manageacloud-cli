import dao.api_instance


def list_instances():
    """
        List available instances in the account
    """
    return dao.api_instance.get_list()


