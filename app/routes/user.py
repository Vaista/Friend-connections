from fastapi import APIRouter
from app.models.pydantic_models import ReceivedToken
from neomodel import Q

from app.helpers.tokens import encrypt_data, decrypt_token
from app.models.neo_models import User

user_router = APIRouter()


@user_router.post("/users/create/")
async def create_user(data: ReceivedToken):
    """Create new users"""
    data = decrypt_token(data.token)
    email = data.get('email').lower()
    first_name = data.get('first_name').title()
    last_name = data.get('last_name').title()

    user = User.nodes.get_or_none(email=email)
    if user is None:
        user = User(email=email, first_name=first_name, last_name=last_name)
        user.save()

    return {'status': 'success'}


@user_router.get("/users/user_list/")
async def fetch_user_list():
    """Fetch the User List"""
    user_list = User.nodes.all()
    user_dict = {'users': []}
    for user in user_list:
        user_dict['users'].append({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        })
    token = encrypt_data(user_dict)
    return {'data': token}


@user_router.get("/users/user_list/search/")
async def search_user(token: str):
    """Search the user as per the input search query"""
    data = decrypt_token(token)
    result_data = []
    if data:
        search_query_list = data.get('search_query').strip().split(" ")
        for query in search_query_list:
            users = User.nodes.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query)
            ).all()
            for user in users:
                user_data = {'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name}
                if user_data not in result_data:
                    result_data.append(user_data)
    encrypted_token = encrypt_data({'data': result_data})
    return {'data': encrypted_token}
