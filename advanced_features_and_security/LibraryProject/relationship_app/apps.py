from django.apps import AppConfig


class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relationship_app'


    def ready(self):
        """
        This method is called when Django starts.
        It is used to import signals or perform any startup tasks.
        """
        import relationship_app.signals
