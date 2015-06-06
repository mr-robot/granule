__author__ = 'beast'
import simpleldap

class LDAPAuth(object):

    def __init__(self, server, port, encryption, user_dn, supported_group):
        self.server = server
        self.user_dn = user_dn
        self.supported_group = supported_group
        self.port = port
        self.encryption = encryption



    def authenticate(self, username, password):
        with simpleldap.Connection(self.server, port=self.port,encryption=self.encryption) as conn:
            is_valid = conn.authenticate(self.user_dn % (username), password)

            if is_valid:
                return True

        return False

    def check_user_in_group(self, username, group=None):
        selected_group = self.supported_group
        if not group:
            selected_group = group


        with simpleldap.Connection(self.server) as conn:
            try:
                result = conn.search("(&(cn=%s)(memberOf=*%s*))" % (username, selected_group))

                if len(result) > 0:
                    return True
            except:
                return False

        return False