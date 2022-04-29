from pygost import gost34112012
from curves.curves import *
from Crypto.Util.number import getRandomRange, inverse


class SignGOSTP34102018:
    def __init__(self, field_params: FieldParams, curve_params: CurveParams, P: CurvePoint):
        self.curve = Curve(field_params=field_params,
                           curve_params=curve_params,
                           P=P)

    @staticmethod
    def read_file(file_name):
        file = open(file_name, 'rb')
        text = file.read()
        file.close()
        return text

    @staticmethod
    def get_hash(text):
        hash = gost34112012.GOST34112012(text).hexdigest()

        return hash

    def get_private_key(self):
        d = int(input("Enter private key(d) or 0 for generate key:"))
        if d == 0:
            d = getRandomRange(1, self.curve.field_params.q)
            print(f"Generated key: {d}")

        return d

    def sign(self, file_name):
        d = self.get_private_key()

        byte_text = self.read_file(file_name)
        a = self.get_hash(byte_text)

        e = int(a, 16) % self.curve.field_params.q
        if e == 0:
            e = 1

        while True:
            while True:
                k = getRandomRange(1, self.curve.field_params.q)

                C = self.curve.multiply_P(k)
                Q = self.curve.multiply_P(d)

                r = C.x % self.curve.field_params.q
                if r != 0:
                    break

            s = (r*d + k*e) % self.curve.field_params.q
            if s != 0:
                break

        return Q, r, s

    def check_sign(self, file_name, Q: CurvePoint, r, s):
        if r < 0 or r > self.curve.field_params.q:
            return False

        if s < 0 or s > self.curve.field_params.q:
            return False

        byte_text = self.read_file(file_name)
        a = self.get_hash(byte_text)

        e = int(a, 16) % self.curve.field_params.q
        if e == 0:
            e = 1

        v = inverse(e, self.curve.field_params.q)

        z1 = (s*v) % self.curve.field_params.q
        z2 = (-1*r*v) % self.curve.field_params.q

        # z1 * P
        C_left = self.curve.multiply_P(z1)
        # rv * Q
        C_rigth = self.curve.multiply_point(z2, Q)

        C = self.curve.sum_points(C_left, C_rigth)

        R = C.x % self.curve.field_params.q

        return R == r
