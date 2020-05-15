from api.models import Travel
from api.serializers import TravelSerialization, TravelCreateSerialization

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class TravelView(APIView, LimitOffsetPagination):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):

        travels = Travel.objects.filter(user=request.user).all().order_by('-id')
        travels_paginated = self.paginate_queryset(travels, request, view=self)
        serializer = TravelSerialization(travels_paginated, many=True)
        return self.get_paginated_response(serializer.data)

    def patch(self, request, travel_id):

        travel = Travel.objects.filter(user=request.user, id=travel_id).first()
        
        if not travel:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        serializer = TravelSerialization(travel, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):

        # use user id from token
        request.data['user'] = request.user.id

        serializer = TravelCreateSerialization(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
