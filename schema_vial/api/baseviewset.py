import logging
from html import escape
from datetime import date, datetime
from decimal import Decimal

from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AuditoriaRegistro
# from .permissions import RolePermission

logger = logging.getLogger("api.operaciones")


class BaseViewSet(viewsets.ModelViewSet):
    # Roles y permisos
    permission_classes = [AllowAny]

    # Auditoría de registros
    audit_enabled = True

    def get_queryset(self):
        queryset = super().get_queryset()

        if (
            hasattr(queryset.model, "activo")
            and self.request
            and "activo" not in self.request.query_params
        ):
            return queryset.filter(activo=True)

        return queryset

    def log_operation(self, operation, instance=None, extra=None):
        model_name = self.get_queryset().model.__name__
        pk = getattr(instance, "pk", None)
        user = getattr(self.request, "user", None)
        username = user.username if user and user.is_authenticated else "anonimo"

        logger.info(
            "%s | modelo=%s | id=%s | usuario=%s | metodo=%s | ruta=%s | extra=%s",
            operation,
            model_name,
            pk,
            username,
            self.request.method,
            self.request.get_full_path(),
            extra or {},
        )

    # Auditoría de registros
    def serialize_audit_data(self, instance):
        data = {}

        for field in instance._meta.fields:
            value = getattr(instance, field.name)

            if isinstance(value, models.Model):
                value = value.pk
            elif isinstance(value, Decimal):
                value = str(value)
            elif isinstance(value, (datetime, date)):
                value = value.isoformat()

            data[field.name] = value

        return data

    # Auditoría de registros
    def save_audit_record(self, action, instance=None, previous_data=None, new_data=None):
        if not self.audit_enabled:
            return

        user = getattr(self.request, "user", None)

        AuditoriaRegistro.objects.create(
            modelo=self.get_queryset().model.__name__,
            registro_id=str(getattr(instance, "pk", "")) if instance else None,
            accion=action,
            usuario=user if user and user.is_authenticated else None,
            metodo=self.request.method,
            ruta=self.request.get_full_path(),
            datos_anteriores=previous_data,
            datos_nuevos=new_data,
        )

    def success_response(self, message, data=None, status_code=status.HTTP_200_OK):
        return Response(
            {
                "success": True,
                "message": message,
                "status_code": status_code,
                "data": data
                
            },
            status=status_code
        )

    def error_response(self, message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        return Response(
            {
                "success": False,
                "message": message,
                "errors": errors
            },
            status=status_code
        )

    # Exportación de información (Excel)
    def clean_excel_value(self, value):
        if value is None:
            return ""

        if isinstance(value, models.Model):
            value = str(value)
        elif isinstance(value, Decimal):
            value = str(value)
        elif isinstance(value, (datetime, date)):
            value = value.isoformat()

        return str(value).replace("\r", " ").replace("\n", " ")

    # Exportación de información (Excel)
    @action(detail=False, methods=["get"], url_path="exportar-excel")
    def export_excel(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        model = queryset.model
        fields = model._meta.fields
        filename = f"{model._meta.model_name}.xls"

        response = HttpResponse(content_type="application/vnd.ms-excel; charset=utf-8")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        response.write("\ufeff")
        response.write("<table><thead><tr>")

        for field in fields:
            response.write(f"<th>{escape(field.verbose_name)}</th>")

        response.write("</tr></thead><tbody>")

        for item in queryset:
            response.write("<tr>")

            for field in fields:
                value = self.clean_excel_value(getattr(item, field.name))
                response.write(f"<td>{escape(value)}</td>")

            response.write("</tr>")

        response.write("</tbody></table>")
        self.log_operation("EXPORT_EXCEL", extra={"total": queryset.count()})

        return response

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            self.log_operation("LIST", extra={"paginated": True})

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.log_operation("LIST", extra={"paginated": False})

        return self.success_response(
        "Consulta realizada correctamente",
        serializer.data
    )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.log_operation("RETRIEVE", instance)

        return self.success_response(
            "Registro encontrado",
            serializer.data
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.save()
            self.log_operation("CREATE", instance)
            # Auditoría de registros
            self.save_audit_record(
                "CREATE",
                instance,
                new_data=self.serialize_audit_data(instance)
            )

            return self.success_response(
                "Registro creado correctamente",
                serializer.data,
                status.HTTP_201_CREATED,
            )
        return self.error_response(
            "Error de validación",
            serializer.errors
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # Auditoría de registros
        previous_data = self.serialize_audit_data(instance)

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )

        if serializer.is_valid():
            instance = serializer.save()
            self.log_operation("UPDATE", instance)
            # Auditoría de registros
            self.save_audit_record(
                "UPDATE",
                instance,
                previous_data=previous_data,
                new_data=self.serialize_audit_data(instance)
            )

            return self.success_response(
                "Registro actualizado correctamente",
                serializer.data
            )

        return self.error_response(
            "Error de validación",
            serializer.errors
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Auditoría de registros
        previous_data = self.serialize_audit_data(instance)

        if hasattr(instance, "soft_delete"):
            instance.soft_delete()
            self.log_operation("SOFT_DELETE", instance)
            # Auditoría de registros
            self.save_audit_record(
                "SOFT_DELETE",
                instance,
                previous_data=previous_data,
                new_data=self.serialize_audit_data(instance)
            )
        else:
            instance.delete()
            self.log_operation("DELETE", instance)
            # Auditoría de registros
            self.save_audit_record(
                "DELETE",
                instance,
                previous_data=previous_data
            )

        return self.success_response(
            "Registro eliminado correctamente"
        )

    @action(detail=True, methods=["post"])
    def restore(self, request, *args, **kwargs):
        queryset = super().get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        instance = get_object_or_404(
            queryset,
            **{self.lookup_field: lookup_value}
        )
        self.check_object_permissions(self.request, instance)

        if not hasattr(instance, "restore"):
            return self.error_response(
                "Este registro no soporta restauracion",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Auditoría de registros
        previous_data = self.serialize_audit_data(instance)
        instance.restore()
        serializer = self.get_serializer(instance)
        self.log_operation("RESTORE", instance)
        # Auditoría de registros
        self.save_audit_record(
            "RESTORE",
            instance,
            previous_data=previous_data,
            new_data=self.serialize_audit_data(instance)
        )

        return self.success_response(
            "Registro restaurado correctamente",
            serializer.data
        )
