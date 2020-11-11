class ProfileError(object):
    ProfileNotFound = (200001, 'Profile Not Found')


class UserError(object):
    UserNotFound = (300001, 'User Not Found')
    PasswordError = (300002, 'Password Error')
    # VeriCodeError = (300003, 'Verification Code Error')
    UserHasExists = (300004, 'User Has Exists')