from portal.displayconf.models import API

def create_new(name, address):
    return API(name=name, base_address=address)