from .customers import Customers
from .customers_group import CustomersGroup
from .customer_by_id import CustomerById 


def init_customers_routes_resources(api):
    api.add_resource(CustomersGroup, "/api/customers/group/<int:group_id>/")
    api.add_resource(Customers, "/api/customers/")
    api.add_resource(CustomerById, "/api/customers/<int:customer_id>")