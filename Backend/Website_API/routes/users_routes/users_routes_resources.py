from .all_users import AllUsers
from .auth import Auth
from .user_by_id import UserById

def init_users_routes_resources(api):
    api.add_resource(AllUsers, "/api/users/")
    api.add_resource(Auth, "/api/users/auth/")
    api.add_resource(UserById, "/api/users/<int:user_id>")