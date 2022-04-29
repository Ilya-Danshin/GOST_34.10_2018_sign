from asn1 import Decoder, Encoder, Numbers
from curves.curves import FieldParams, CurveParams, CurvePoint

class ASN1:
    @staticmethod
    def encode(Q: CurvePoint, field: FieldParams, curve: CurveParams, P: CurvePoint, r, s):
        encoder = Encoder()
        encoder.start()

        encoder.enter(Numbers.Sequence)                             # Заголовок
        encoder.enter(Numbers.Set)                                  # Множество ключей

        encoder.enter(Numbers.Sequence)                             # Первый "ключ"
        encoder.write(b'\x80\x06\x07\x00', Numbers.OctetString)     # Идентификатор алгоритма
        encoder.write(b'gostSignKey', Numbers.UTF8String)           #

        encoder.enter(Numbers.Sequence)                             # Значение открытого ключа
        encoder.write(Q.x, Numbers.Integer)
        encoder.write(Q.y, Numbers.Integer)
        encoder.leave()

        encoder.enter(Numbers.Sequence)                             # Параметры криптосистемы

        encoder.enter(Numbers.Sequence)                             # Параметры поля
        encoder.write(field.p, Numbers.Integer)                     # p
        encoder.leave()

        encoder.enter(Numbers.Sequence)                             # Параметры кривой
        encoder.write(curve.a, Numbers.Integer)                     # A
        encoder.write(curve.b, Numbers.Integer)                     # B
        encoder.leave()

        encoder.enter(Numbers.Sequence)                             # Образующая группы точек кривой
        encoder.write(P.x, Numbers.Integer)
        encoder.write(P.y, Numbers.Integer)
        encoder.leave()

        encoder.write(field.q, Numbers.Integer)                     # Порядок группы
        encoder.leave()

        encoder.enter(Numbers.Sequence)                             # Подпись сообщения
        encoder.write(r, Numbers.Integer)
        encoder.write(s, Numbers.Integer)
        encoder.leave()

        encoder.leave()
        encoder.leave()

        encoder.enter(Numbers.Sequence)
        encoder.leave()

        encoder.leave()

        return encoder.output()

    @staticmethod
    def decode(sign):
        decoder = Decoder()
        decoder.start(sign)

        decoder.enter()
        decoder.enter()
        decoder.enter()
        decoder.read()
        decoder.read()

        decoder.enter()
        Q_x = decoder.read()[1]
        Q_y = decoder.read()[1]
        decoder.leave()

        decoder.enter()

        decoder.enter()
        p = decoder.read()[1]
        decoder.leave()

        decoder.enter()
        a = decoder.read()[1]
        b = decoder.read()[1]
        decoder.leave()

        decoder.enter()
        P_x = decoder.read()[1]
        P_y = decoder.read()[1]
        decoder.leave()

        q = decoder.read()[1]
        decoder.leave()

        decoder.enter()
        r = decoder.read()[1]
        s = decoder.read()[1]
        decoder.leave()

        decoder.leave()
        decoder.leave()

        decoder.enter()
        decoder.leave()

        decoder.leave()

        Q = CurvePoint(Q_x, Q_y)
        field_params = FieldParams(p, q)
        curve_params = CurveParams(a, b)
        P = CurvePoint(P_x, P_y)

        return Q, field_params, curve_params, P, r, s