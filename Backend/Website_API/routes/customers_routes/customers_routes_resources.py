from .customers import Customers
from .customers_group import CustomersGroup 


def init_customers_routes_resources(api):
    api.add_resource(CustomersGroup, "/api/customers/group/<int:group_id>/")
    api.add_resource(Customers, "/api/customers/")
    #api.add_resource(GroupById, "/api/groups/<int:group_id>")