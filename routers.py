

class CommonRouter(object):
    """A router to control all database operations on common model"""

    def db_for_read(self, model, **hints):
        "Point all operations on common models to 'common'"
        if model._meta.object_name == 'Common1':
            return 'common'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on common models to 'common'"
        if model._meta.object_name == 'Common1':
            return 'common'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if common model is involved"
        if obj1._meta.object_name == 'Common1' or obj2._meta.object_name == 'Common1':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure common objects only appears on the 'common' db"
        if db == 'common':
            return model._meta.object_name == 'Common1'
        elif model._meta.object_name == 'Common1':
            return False
        return None

class UserRouter(object):
    """A router to fix where ORM looks for User object"""

    def db_for_read(self, model, **hints):
        if model._meta.object_name == 'User':
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.object_name == 'User':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.object_name == 'User' or obj2._meta.object_name == 'User':
            return True
        return None
    """
    def allow_syncdb(self, db, model):
        if db == 'default':
            return model._meta.object_name == 'User'
        elif model._meta.object_name == 'User':
            return False
        return None
    """
