import json

ADMIN_ID = 914396732

def load_user_set():
    user_set = set()
    with open("users.json", 'r')as f:
        try:
            user_set = set(json.load(f))
        except:
            user_set = set()
    return user_set

def set_user(message):
    current_user_set = load_user_set()
    if not (message.chat.id in current_user_set):
        with open("users.json", "w") as f:
            current_user_set.add(message.chat.id)
            json.dump(list(current_user_set),f)
