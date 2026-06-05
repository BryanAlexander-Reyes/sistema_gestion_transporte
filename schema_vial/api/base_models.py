from django.db import models

class SoftDeleteModel(models.Model):
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.activo = False
        self.save(update_fields=["activo", "fecha_modificacion"])

    def restore(self):
        self.activo = True
        self.save(update_fields=["activo", "fecha_modificacion"])
