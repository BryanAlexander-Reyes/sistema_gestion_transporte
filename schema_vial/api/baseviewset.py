import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

logger = logging.getLogger("api.operaciones")


class BaseViewSet(viewsets.ModelViewSet):
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

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )

        if serializer.is_valid():
            instance = serializer.save()
            self.log_operation("UPDATE", instance)

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

        if hasattr(instance, "soft_delete"):
            instance.soft_delete()
            self.log_operation("SOFT_DELETE", instance)
        else:
            instance.delete()
            self.log_operation("DELETE", instance)

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

        instance.restore()
        serializer = self.get_serializer(instance)
        self.log_operation("RESTORE", instance)

        return self.success_response(
            "Registro restaurado correctamente",
            serializer.data
        )
