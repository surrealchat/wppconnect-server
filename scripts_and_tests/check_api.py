import requests
import json
HOST = "http://localhost:22000/"
SECRET = "MYsecrettokenisveryGoodBecauseOurSurrealAppRocksSoNicely12k939"

SESSION = "MySession"
TOKEN="$2b$10$30keirsC8e5FjRcp4p5X0uZGcDeSkMiqzBUtCPhqKZfUqDzAi.78W"

def get_authentication_token(session=SESSION, host=HOST, secret=SECRET):
    url = f"{host.rstrip('/')}/api/{session}/{secret}/generate-token"
    response = requests.post(url)
    return response.json()

def format_token(token):
    # Replace / with _ and + with - in the token
    return token.replace('/', '_').replace('+', '-')

# token_response = get_authentication_token()
# TOKEN = token_response['token']
# print(f"Token is {TOKEN}")

def _generic_api_post(url_part, headers, session=SESSION, token=TOKEN, data=None):
    url = f"{HOST.rstrip('/')}/api/{session}/{url_part}"
    headers["Authorization"] = f"Bearer {token}"
    response = requests.post(url, headers=headers, json=data)
    return response

def _generic_api_get(url_part, headers, session=SESSION, token=TOKEN):
    url = f"{HOST.rstrip('/')}/api/{session}/{url_part}"
    headers["Authorization"] = f"Bearer {token}"
    response = requests.get(url, headers=headers)
    return response


def start_session(session=SESSION, token=TOKEN):
    # Format the token before using it
    formatted_token = format_token(token)
    url = f"{HOST.rstrip('/')}/api/{session}/start-session"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {formatted_token}"
    }
    response = requests.post(url, headers=headers)
    return response.json()

def get_qr_code(session=SESSION, token=TOKEN, path="qr/"):
    formatted_token = format_token(token)
    url = f"{HOST.rstrip('/')}/api/{session}/qrcode-session"
    headers = {
        "Accept": "application/json", 
        "Content-Type": "application/json",
        "Authorization": f"Bearer {formatted_token}"
    }
    response = requests.get(url, headers=headers)

    status = response.status_code 
    header = response.headers #json
    qrcode = response.text
    
    # Debug information
    print(f"Status Code: {status}")
    print(f"Response Headers: {headers}")
    

    if response.status_code == 200:
        # Save PNG image data if content type is image/png
        if 'content-type' in header and header['content-type'] == 'image/png':
             _save_qr_code_as_file(qrcode, session=session, path=path)
    else:
        print(f"Error response from server: {response.text}")
        response.raise_for_status()

def _save_qr_code_as_file(qrcode, session="", path=""):
    with open(path + f'qrcode_{session}.png', 'wb') as f:
        f.write(response.content)
        print("QR code saved as qrcode.png")

def get_list_of_chats(session=SESSION, token=TOKEN):
    url_part = "list-chats"
    headers = {
        "Accept": "application/json", 
        "Content-Type": "application/json",
        "id": "<chatId>",
        "count": "20",
        "direction": "after",
        "onlyGroups": "False",
        "onlyUsers": "False",
        "onlyWithUnreadMessage": "False",
        "withLabels": "[]"
    }
    response = _generic_api_post(url_part, headers, session=session, token=token)
    status = response.status_code
    headers = response.headers
    data = response.text

    if status == 200:   
        try:
            return response.json()
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return None
    else:
        print(f"Error response from server: {response.text}")
        response.raise_for_status()
        return None
    

def send_message(message, session=SESSION, token=TOKEN, number="491605740074"):
    url = f"http://localhost:22000/api/{session}/send-message"
    
    # Headers for authentication and content type
    headers = {
        "accept": "*/*",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # Request body as a dictionary
    data = {
        "phone": number
    ,
        "isGroup": False,  # boolean, not string
        "isNewsletter": False,  # boolean, not string
        "isLid": False,  # boolean, not string
        "message": str(message)
    }
    
    response = requests.post(url, headers=headers, json=data)  # Use json parameter to automatically format JSON
    
    try:
        data = response.json()
        return data
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        print(f"Raw response text: {response.text}")
        response.raise_for_status()
        return None
    

def get_chat_messages(number, session=SESSION, token=TOKEN, max_messages=10):
    url_part = f"all-messages-in-chat/{number}"
    headers = {
        "Accept": "application/json", 
        "Content-Type": "application/json",
    }

    response = _generic_api_get(url_part, headers, session=session, token=token)

    status = response.status_code
    headers = response.headers

    if status == 200:
        res = response.json()
        messages = res['response']
        return messages
    else:
        print(f"Error response from server: {response.text}")
        response.raise_for_status()
        return None
    

def get_unread_messages(session=SESSION, token=TOKEN):
    url_part = "all-unread-messages"
    headers = {
        "Accept": "application/json", 
        "Content-Type": "application/json",
    }
    response = _generic_api_get(url_part, headers, session=session, token=token)
    status = response.status_code
    headers = response.headers
    data = response.text

    if status == 200:
        return response.json()
    else:
        print(f"Error response from server: {response.text}")
        response.raise_for_status()


def get_unread_chats_from_unread_messages(response):
    unread_messages = response['response']
    unread_chats = []
    unread_chats_dict = {}
    for message in unread_messages:
        chat_id = message['from']
        chat_name = message['sender']['name']
        sender_id = message['sender']['id']['user']
        sender_name = message['sender']['name']
        unread_chats_dict[chat_id] = chat_name
    return unread_chats_dict

def set_message_as_unread(phone, session=SESSION, token=TOKEN):
    url_part = f"mark-unseen"
    headers = {
        "Accept": "application/json", 
        "Content-Type": "application/json",
    }
    data = {
        "phone": phone,
        "isGroup": False,
    }
    response = _generic_api_post(url_part, headers, session=session, token=token, data=data)
    return response.json()
    
if __name__ == "__main__":
    # Start the session
    # response = start_session()
    # print(f"start session response: {response} ")

    # Get QR code
    #get_qr_code(token=TOKEN)


    # Get unread chats
    # chats = get_list_of_chats(token=TOKEN)
    # for chat in chats:
    #     # get the chat id and the chat name
    #     chat_id = chat['id']['user']
    #     chat_name = chat['contact']['name']
    #     print(f"chat_id: {chat_id}, chat_name: {chat_name}")

    #     messages = get_chat_messages(number=chat_id, session=SESSION, token=TOKEN)
    #     for message in messages:
    #         if "body" not in message:
    #             continue
    #         #print(f"message: {message}\n\n")
    #         print(f"{message['sender']['name']} (fm: {message['fromMe']}): {message['content']}")

    #     break

    unread_chats = get_unread_chats_from_unread_messages(get_unread_messages(session=SESSION, token=TOKEN))
    print(f"unread_chats: {unread_chats}")

    # response = send_message(
    #     message="Do you like it to get messages from here?",
    #     session=SESSION,
    #     token=TOKEN,
    #     chat_id="491605740074"
    # )

    chat_id = "491605740074"
    messages = get_chat_messages(number=chat_id, session=SESSION, token=TOKEN)
    for message in messages:
        if "body" not in message:
            continue
        print(f"{message['sender']['name']} (fm: {message['fromMe']}): {message['body']}")

    unread_chats = get_unread_chats_from_unread_messages(get_unread_messages(session=SESSION, token=TOKEN))
    print(f"unread_chats: {unread_chats}")

    mark_as_read = set_message_as_unread(phone=chat_id, session=SESSION, token=TOKEN)

    unread_chats = get_unread_chats_from_unread_messages(get_unread_messages(session=SESSION, token=TOKEN))
    print(f"unread_chats: {unread_chats}")
    
    # print(f"response: \n{response}")