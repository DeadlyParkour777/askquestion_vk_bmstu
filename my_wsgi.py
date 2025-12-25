from urllib.parse import parse_qs

def application(environ, start_response):
    method = environ.get('REQUEST_METHOD')
    
    query_string = environ.get('QUERY_STRING', '')
    get_params = parse_qs(query_string)
    
    post_params = {}
    if method == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size)
            post_params = parse_qs(request_body.decode('utf-8'))
        except (ValueError, KeyError):
            pass

    output = [
        f"Request Method: {method}\n".encode('utf-8'),
        f"GET Params: {get_params}\n".encode('utf-8'),
        f"POST Params: {post_params}\n".encode('utf-8')
    ]

    status = '200 OK'
    response_headers = [('Content-type', 'text/plain; charset=utf-8')]
    
    start_response(status, response_headers)
    return output
