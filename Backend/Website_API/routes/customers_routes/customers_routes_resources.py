from .customers import Customers


def init_customers_routes_resources(api):
    #api.add_resource(GroupsUser, "/api/groups/user/<int:user_id>/")
    api.add_resource(Customers, "/api/customers/")
    #api.add_resource(GroupById, "/api/groups/<int:group_id>")