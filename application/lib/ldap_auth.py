from ldap3 import Server, Connection
import re

from application import app

def authenticate(username, password):

    if re.match("^z[0-9]{7}$", username) is None:
        return None

    user_dn = "CN={},OU=People{},OU=IDM_People,OU=IDM,DC=ad,DC=unsw,DC=edu,DC=au".format(username, username[-2:])
    try:
        server = Server(app.config["LDAP_URL"])
        conn = Connection(server, user_dn, password)
        if not conn.bind():
            return None

        base_dn = "OU=IDM_People,OU=IDM,DC=ad,DC=unsw,DC=edu,DC=au"

        attributes = ['displayNamePrintable']
        search_filter = "(cn={})".format(username)
        conn.search(base_dn, search_filter, attributes=attributes)
        name = conn.entries[0]['displayNamePrintable'].value
        return name

    except Exception as e:
        return None