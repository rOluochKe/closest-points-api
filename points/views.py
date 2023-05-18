from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Point, ClosestPoints
from .serializers import PointSerializer


class PointAPIView(APIView):
    def post(self, request):
        points_data = request.data.get('points', '')
        points = points_data.split(';')

        point_objects = []
        for point in points:
            x, y = point.split(',')
            point_objects.append(Point(x=int(x), y=int(y)))

        Point.objects.bulk_create(point_objects)

        closest_points = self.find_closest_points(point_objects)

        closest_points_entry = ClosestPoints.objects.create()
        closest_points_entry.original_points.set(point_objects)
        closest_points_entry.closest_points.set(closest_points)

        original_points_serializer = PointSerializer(point_objects, many=True)
        closest_points_serializer = PointSerializer(closest_points, many=True)

        response_data = {
            'original_points': original_points_serializer.data,
            'closest_points': closest_points_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @staticmethod
    def find_closest_points(points):
        closest_points = []
        min_distance = float('inf')

        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                point1 = points[i]
                point2 = points[j]

                distance = (point1.x - point2.x) ** 2 + \
                    (point1.y - point2.y) ** 2

                if distance < min_distance:
                    closest_points = [point1, point2]
                    min_distance = distance

        return closest_points
