import pytest

from ..users import User
from ..users import BASEDN

valid_password = 'p8ssW0rd'


def test_create_valid_user():
    ''' Sanity check and I have to start somewhere, can I simply create a User
    maybe even work as an example of how to create a user
    '''
    User('pigg', 1, valid_password, first_name='Gunea', last_name='Pig')
    User(last_name='Pig', username='pigg', password=valid_password, yos=1)
    u = User(username='pigg',
             last_name='Pig',
             password=valid_password,
             first_name='Gunea',
             yos=1,
             home_directory="/home/directrory")
    assert u.home_directory == "/home/directrory"


def test_cannot_create_invalid_user():
    ''' Example of what an invalid user looks like
    '''
    with pytest.raises(TypeError):
        User()
    with pytest.raises(TypeError):
        User('Gunea', 'Pig')


def test_password_must_be_string():
    with pytest.raises(TypeError):
        User('Gunea', 'Pig', 1, password=3)


def test_ntlm_passwords_generated_automatically():
    user = User('Gunea', 1, valid_password)
    assert user.samba_nt_password is not None
    assert user.samba_lm_password is not None


def test_password_must_have_length_greater_than_6():
    with pytest.raises(TypeError):
        User('Gunea', 1, password=valid_password[:-3])


def test_password_must_have_atleast_one_numeral():
    with pytest.raises(ValueError):
        User('Gunea', 1, password='passW@rd')


def test_yos_must_be_between_1_and_7():
    with pytest.raises(TypeError):
        User('Gunea', 0, password=valid_password)
    with pytest.raises(TypeError):
        User('Gunea', 8, password=valid_password)


def test_dn_set_based_username():
    user = User('pigg', 1, password=valid_password)
    assert user.username == 'pigg'
    assert user.dn == 'uid=%s,%s' % (user.username, BASEDN)


def test_home_directory_generated_using_yos():
    user = User('pigg', 1, password=valid_password)
    assert user.home_directory == '/home/ug/pigg'


def test_uid_generated_using_yos():
    user = User('Gunea', 1, password=valid_password)
    assert int(user.uid_number) >= 1000
    assert int(user.uid_number) < 2000


def test_samba_sid_set_from_uid():
    user = User('Gunea', 1, password=valid_password)
    assert user.samba_sid is not None


def test_gid_generated_using_yos():
    user = User('Gunea', 1, password=valid_password)
    assert user.gid_number == '1000'
