from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response


class BaseViewSet(viewsets.ModelViewSet):

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

        return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return self.success_response(
        "Consulta realizada correctamente",
        serializer.data
    )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return self.success_response(
            "Registro encontrado",
            serializer.data
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

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
            serializer.save()

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
        instance.delete()

        return self.success_response(
            "Registro eliminado correctamente"
        )