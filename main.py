from SignGOSTP34102018.sign_gost_p_3410_2018 import SignGOSTP34102018
from curves.curves import FieldParams, CurveParams, CurvePoint
from asn1_handler.asn1_handler import ASN1
from file_generate.file_generate import RandomFileGenerator


def mode_choose():
    mode = int(input("Choose mode:\n\
                     1. Sign file\n\
                     2. Check sign\n\
                     3. Generate random file\n\
                     \n\
                     0. Exit\n"))

    return mode


def get_file():
    file_name = input("File name:")

    return file_name


def get_asn1_file():
    file_name = input("Sign file name:")

    return file_name


def create_new_file_and_write(in_file_name, message, resolution):
    counter = 0
    new_name = ''
    for sym in in_file_name[::-1]:
        if sym == '.':
            new_name += in_file_name[:len(in_file_name) - counter]
            new_name += resolution
        counter += 1

    out_file = open(new_name, 'wb')
    out_file.write(message)
    out_file.close()


def main():

    while True:
        mode = mode_choose()

        if mode == 1:
            # Hardcode params
            p = 57896044630612021680684936114742422271145183870487080309667128995208157569947
            q = 28948022315306010840342468057371211135571302038761442251594012761075345324491
            a = 1
            b = 19750513962881385028059495396984460236743646692126413053976069443380491067343
            xP = 43490682822985073571091311123441225129011272278165566160439297012894969619553
            yP = 53273700124912449490307054424387372532482586733448415163119878489682918137700

            field_params = FieldParams(p=p, q=q)
            curve_params = CurveParams(a=a, b=b)
            P = CurvePoint(x=xP, y=yP)
            # Create signer
            signer = SignGOSTP34102018(field_params, curve_params, P)

            file_name = get_file()
            # Sign file
            Q, r, s = signer.sign(file_name)
            # Get sign in asn1 format
            encoded_file = ASN1.encode(Q, field_params, curve_params, P, r, s)
            # Create file
            create_new_file_and_write(file_name, encoded_file, 'asn1')
        elif mode == 2:
            file_name = get_asn1_file()
            file = open(file_name, "rb")
            sign_asn1 = file.read()
            file.close()

            file_name = get_file()

            Q, field_params, curve_params, P, r, s = ASN1.decode(sign_asn1)

            signer = SignGOSTP34102018(field_params=field_params, curve_params=curve_params, P=P)
            is_correct = signer.check_sign(file_name, Q, r, s)

            if is_correct:
                print("Sign is correct!")
            else:
                print("Sign is incorrect!")
        elif mode == 3:
            file_name = input("File name:")
            size = int(input("File size:"))

            RandomFileGenerator.generate(file_name, size)
        elif mode == 0:
            break


if __name__ == '__main__':
    main()