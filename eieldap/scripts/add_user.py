from eieldap.models import users

user = {"username": "mbulil",
        "first_name": "Leonard",
        "last_name": "Mbuli",
        "email": ["0705871Y@students.wits.ac.za"],
        "password": "passing",
        "hosts": ['babbage.ug.eie.wits.ac.za',
                  'testing.ug.eie.wits.ac.za'],
        "yos": "4"}

if users.save(user):
    print "Saved"
