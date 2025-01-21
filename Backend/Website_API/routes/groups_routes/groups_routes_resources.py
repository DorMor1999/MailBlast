from .groups import Groups
from.groups_user import GroupsUser

def init_groups_routes_resources(api):
    api.add_resource(GroupsUser, "/api/groups/user/<int:user_id>/")
    api.add_resource(Groups, "/api/groups/")
    #api.add_resource(UserById, "/api/groups/<int:group_id>")