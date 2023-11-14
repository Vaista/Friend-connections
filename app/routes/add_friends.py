from fastapi import APIRouter

from app.helpers.tokens import encrypt_data, decrypt_token
from app.models.neo_models import User

add_friend_router = APIRouter()


@add_friend_router.post("/users/add_friends/send_request/")
async def send_friend_request(token: str):
    """Create new users"""
    data = decrypt_token(token)
    sender_email = data.get('sender_email')
    receiver_email = data.get('receiver_email')

    if sender_email is None or receiver_email is None:
        return {'status': 'error', 'reason': 'emails missing'}

    sender = User.nodes.get(email=sender_email)
    receiver = User.nodes.get(email=receiver_email)
    sender.send_friend_request(other_user=receiver)

    return {'status': 'success'}


@add_friend_router.post("/users/add_friends/delete_request/")
async def delete_friend_request(token: str):
    """Delete an already existing friend request"""
    data = decrypt_token(token)
    email1 = data.get('email1')
    email2 = data.get('email2')

    if email1 is None or email2 is None:
        return {'status': 'error', 'reason': 'emails missing'}

    user1 = User.nodes.get(email=email1)
    user2 = User.nodes.get(email=email2)
    user1.delete_friend_request(other_user=user2)

    return {'status': 'success'}


@add_friend_router.post("/users/add_friends/accept_request/")
async def accept_friend_request(token: str):
    """Accept the friend requests between 2 users"""
    data = decrypt_token(token)
    email1 = data.get('email1')
    email2 = data.get('email2')

    if email1 is None or email2 is None:
        return {'status': 'error', 'reason': 'emails missing'}

    user1 = User.nodes.get(email=email1)
    user2 = User.nodes.get(email=email2)

    user1.make_friend(other_user=user2)

    return {'status': 'success'}


@add_friend_router.get("/users/add_friends/received_requests/")
async def received_friend_requests(token: str):
    """Returns the received requests by the user"""
    data = decrypt_token(token)
    email = data.get('email')

    if email is None:
        return {'status': 'error', 'reason': 'email missing'}

    user = User.nodes.get(email=email)

    # To fetch friend requests received by user2
    received_requests = user.get_received_friend_requests()
    try:
        received_requests = [{
            'email': req.email,
            'name': f'{req.first_name} {req.last_name}'
        } for req in received_requests[0]]
    except:
        received_requests = []

    token = encrypt_data({'data': received_requests})
    return {'status': 'success', 'token': token}


@add_friend_router.get("/users/add_friends/sent_requests/")
async def sent_friend_requests(token: str):
    """Returns sent requests by the user"""
    data = decrypt_token(token)
    email = data.get('email')

    if email is None:
        return {'status': 'error', 'reason': 'email missing'}

    user = User.nodes.get(email=email)

    # To fetch friend requests received by user2
    sent_requests = user.get_sent_friend_requests()
    try:
        sent_requests = [{
            'email': req.email,
            'name': f'{req.first_name} {req.last_name}'
        } for req in sent_requests[0]]
    except:
        sent_requests = []

    token = encrypt_data({'data': sent_requests})
    return {'status': 'success', 'token': token}


@add_friend_router.post("/users/friends/delete_friend/")
async def delete_friend(token: str):
    """Delete a user from user's friend list"""
    data = decrypt_token(token)
    email1 = data.get('email1')
    email2 = data.get('email2')

    if email1 is None or email2 is None:
        return {'status': 'error', 'reason': 'emails missing'}

    user1 = User.nodes.get(email=email1)
    user2 = User.nodes.get(email=email2)

    user1.remove_friend(other_user=user2)

    return {'status': 'success'}
