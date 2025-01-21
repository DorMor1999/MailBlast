from .groups import Groups

def init_groups_routes_resources(api):
    #api.add_resource(AllUsers, "/api/groups/user/<int:group_id>")
    api.add_resource(Groups, "/api/groups/")
    #api.add_resource(UserById, "/api/groups/<int:group_id>")