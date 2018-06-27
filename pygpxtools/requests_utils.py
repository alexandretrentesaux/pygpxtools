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
<<<<<<< HEAD
=======


def req_url_builder(url):
    print('todo')
>>>>>>> 3763fefaab4b067f69df8233ed278811d71032e5
