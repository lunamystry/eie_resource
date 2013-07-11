from resource import eieldap


class Users():
    first_name = None;
    last_name = None;
    username = None;
    yos = None;
    nt_password = None;
    lm_password = None;
    plain_password = None;
    uid_number = None;
    gid_number = None;
    smb_rid = None;

    def save(self, attr):
        """ if the user exists update, if not create"""
        user = eieldap.find_one(attr["dn"])
        if user:
            eieldap.update(attr)
            return attr["dn"]
        else:
            eieldap.create(attr)
            return attr["dn"]
        return "error"
