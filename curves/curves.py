from dataclasses import dataclass
from Crypto.Util.number import inverse


@dataclass
class FieldParams:
    p: int
    q: int


@dataclass
class CurveParams:
    a: int
    b: int


@dataclass
class CurvePoint:
    x: int
    y: int


class Curve:
    def __init__(self, field_params: FieldParams, curve_params: CurveParams, P: CurvePoint):
        self.field_params = field_params
        self.curve_params = curve_params
        self.P = P

    def double_point(self, point: CurvePoint):
        if point.x == 0 and point.y == 1:
            return CurvePoint(0, 1)

        alpha_top = (3*(point.x**2) + self.curve_params.a) % self.field_params.p
        alpha_bottom = inverse(2*point.y, self.field_params.p) % self.field_params.p

        alpha = (alpha_top * alpha_bottom) % self.field_params.p

        x = (alpha**2 - 2*point.x) % self.field_params.p
        y = (alpha*(point.x - x) - point.y) % self.field_params.p

        return CurvePoint(x, y)

    def sum_points(self, point1: CurvePoint, point2: CurvePoint):
        if point1.x == 0 and point1.y == 1:
            return point2

        if point2.x == 0 and point2.y == 1:
            return point1

        if point1.x == point2.x and point1.y == point2.y:
            return self.double_point(point1)

        if point1.x == point2.x:
            return CurvePoint(0, 1)

        alpha_top = (point2.y - point1.y) % self.field_params.p
        alpha_bottom = inverse(point2.x - point1.x, self.field_params.p)

        alpha = (alpha_top * alpha_bottom) % self.field_params.p

        x = (alpha**2 - point1.x - point2.x) % self.field_params.p
        y = (alpha*(point1.x - x) - point1.y) % self.field_params.p

        return CurvePoint(x, y)

    def multiply_P(self, k):
        return self.multiply_point(k, self.P)

    def multiply_point(self, k, point: CurvePoint):
        Q = CurvePoint(0, 1)
        if k == 0:
            return Q
        if k == 1:
            return point
        if k == 2:
            return self.double_point(point)

        binary_k = "{0:b}".format(k)

        for i in binary_k:
            Q = self.double_point(Q)
            if i == '1':
                Q = self.sum_points(Q, point)

        return Q
