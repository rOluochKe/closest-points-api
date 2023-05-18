from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import Point, ClosestPoints
from .serializers import PointSerializer
from .views import PointAPIView


class PointAPITest(TestCase):
    def test_closest_points(self):
        url = reverse('points')
        data = {'points': '2,2;-1,30;20,11;4,5'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        closest_points_entry = ClosestPoints.objects.first()

        closest_points = closest_points_entry.closest_points.all()
        original_points = closest_points_entry.original_points.all()

        serializer = PointSerializer(original_points, many=True)
        expected_data = {
            'original_points': serializer.data,
            'closest_points': PointSerializer(closest_points, many=True).data,
        }

        self.assertEqual(response.data, expected_data)
        # Corrected assertion
        self.assertEqual(len(response.data['closest_points']), 2)


class PointModelTest(TestCase):
    def test_find_closest_points(self):
        point1 = Point.objects.create(x=2, y=2)
        point2 = Point.objects.create(x=-1, y=30)
        point3 = Point.objects.create(x=20, y=11)
        point4 = Point.objects.create(x=4, y=5)

        closest_points = PointAPIView.find_closest_points(
            [point1, point2, point3, point4])

        self.assertEqual(len(closest_points), 2)  # Corrected assertion
        self.assertIn(point1, closest_points)
        self.assertIn(point4, closest_points)
        self.assertNotIn(point2, closest_points)
        self.assertNotIn(point3, closest_points)
