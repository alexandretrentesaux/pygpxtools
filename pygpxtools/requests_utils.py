# -*- encoding: utf-8 -*-

def req_headers_builder(method=None):
    """Create headers needed by requests method

    Args:
        method (str, optional): requests method (GET, POST, PUT, DELETE), GET is default feature so optional

    Returns:
        json: headers data for requests
    """
    # basic method GET
    headers = {
        'accept': 'application/json'
    }
    # addition for POST & PUT
    if method in ('POST', 'PUT'):
        headers.update({'Content-Type': 'application/json'})
    return headers
