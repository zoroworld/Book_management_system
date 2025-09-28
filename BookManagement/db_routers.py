# myproject/routers.py
class DbRouter:
    """
    Route 'books' and auth-related models to MySQL.
    """

    apps_mysql = ['user','book', 'auth', 'contenttypes', 'sessions', 'admin']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.apps_mysql:
            return 'mysql_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.apps_mysql:
            return 'mysql_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in self.apps_mysql or obj2._meta.app_label in self.apps_mysql:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.apps_mysql:
            return db == 'mysql_db'
        return None
