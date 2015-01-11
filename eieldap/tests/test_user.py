import pytest

from ..users import User
from ..users import BASEDN


def test_create_valid_user():
    ''' Sanity check and I have to start somewhere, can I simply create a User
    maybe even work as an example of how to create a user
    '''
    User('Gunea', 'Pig', 1, 'p8ss!w0rd')
    User(last_name='Pig', password='password', first_name='Gunea', yos=1)


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
    user = User('Gunea', 'Pig', 1, password='p8ss!ng')
    assert user.samba_nt_password is not None
    assert user.samba_lm_password is not None


def test_password_must_have_length_greater_than_6():
    with pytest.raises(TypeError):
        User('Gunea', 'Pig', 1, password='p8ss!')


def test_password_must_have_atleast_one_punctuation():
    with pytest.raises(TypeError):
        User('Gunea', 'Pig', 1, password='p8ssing')


def test_password_must_have_atleast_one_numeral():
    with pytest.raises(TypeError):
        User('Gunea', 'Pig', 1, password='pass!ng')


def test_yos_must_be_between_1_and_7():
    with pytest.raises(TypeError):
        User('Gunea', 'Pig', 0, password='p8ss!ng')
    with pytest.raises(TypeError):
        User('Gunea', 'Pig', 8, password='p8ss!ng')


def test_if_no_username_given_auto_generated_from_name():
    user = User('Gunea', 'Pig', 1, password='p8ss!ng')
    assert user.username == 'pigg'


def test_dn_set_based_username():
    user = User('Gunea', 'Pig', 1, password='p8ss!ng')
    assert user.username == 'pigg'
    assert user.dn == 'uid=%s,%s' % (user.username, BASEDN)


def test_home_directory_generated_using_yos():
    user = User('Gunea', 'Pig', 1, password='p8ss!ng')
    assert user.home_directory == '/home/ug/pigg'


def test_uid_generated_using_yos():
    user = User('Gunea', 'Pig', 1, password='p8ss!ng')
    assert int(user.uid_number) >= 1000
    assert int(user.uid_number) < 2000


def test_samba_sid_set_from_uid():
    user = User('Gunea', 'Pig', 1, password='p8ss!ng')
    assert user.samba_sid is not None


def test_gid_generated_using_yos():
    user = User('Gunea', 'Pig', 1, password='p8ss!ng')
    assert user.gid_number == '1000'


