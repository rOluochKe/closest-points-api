from django.db import models


class Point(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return f"{self.x},{self.y}"

    @classmethod
    def find_closest_points(cls):
        points = cls.objects.all()
        closest_points = []

        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                point1 = points[i]
                point2 = points[j]

                distance = (point1.x - point2.x) ** 2 + \
                    (point1.y - point2.y) ** 2

                if not closest_points or distance < closest_points[0]['distance']:
                    closest_points = [
                        {
                            'point1': point1,
                            'point2': point2,
                            'distance': distance,
                        }
                    ]
                elif distance == closest_points[0]['distance']:
                    closest_points.append(
                        {
                            'point1': point1,
                            'point2': point2,
                            'distance': distance,
                        }
                    )

        return closest_points


class ClosestPoints(models.Model):
    original_points = models.ManyToManyField(
        Point, related_name='original_points')
    closest_points = models.ManyToManyField(
        Point, related_name='closest_points')

    def __str__(self):
        original_points_str = ', '.join(str(point) for point in self.original_points.all())
        closest_points_str = ', '.join(str(point) for point in self.closest_points.all())
        return f"Original Points: {original_points_str}\nClosest Points: {closest_points_str}"
