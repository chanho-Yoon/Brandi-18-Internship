def error_response(server_message, user_message):
    response = {"server_message" : message,
                "user_message" : user_message}
    return response

def post_response(message):
    response = {"message": message}
    return response

def get_response(results):
    response = {"results" : results}
    return response



