def is_administrator(user):
    return user.groups.filter(name='admin').exists()

def is_estructura(user):
    return user.groups.filter(name='staff').exists()

def is_hr(user):
    return user.groups.filter(name='hr').exists()

def is_estandar(user):
    return user.groups.filter(name='estandar').exists()
