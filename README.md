___
# GOST 34.10-2018 realization
Implementation of the signature protocol on elliptic curves according to 
GOST R 34.10-2018. Description of signature file format:
```
SEQUENCE {- header
  SET { - set of keys, 1 enabled
    SEQUENCE {- first "key"
      OCTET STRING – algorithm identifier (GOST signature protocol)
        80 06 07 00
      UTF8String 'gostSignKey' - may not be used
      SEQUENCE {- public key value
        INTEGER - x-coordinate of point Q
           QX QX … QX
        INTEGER - y-coordinate of point Q
           QY QY … QY
      }
      SEQUENCE {- cryptosystem parameters
        SEQUENCE {- field parameters
          INTEGER - prime number p
            PP PP … PP
        }
        SEQUENCE {- curve parameters
          INTEGER - coefficient A of the equation of the curve
            AA AA … AA
          INTEGER - coefficient B of the curve equation
            BB BB … BB
        }
        SEQUENCE {- generator of the group of points of the curve
          INTEGER – x-coordinate of generator point P
            PX PX … PX
          INTEGER – y-coordinate of generator point P
            PY PY … PY
        }
        INTEGER - group order q
          RR RR … RR
      } – cryptosystem parameters
      SEQUENCE {- message signature
        INTEGER - number r
          XR XR … XR
        INTEGER - number s
          SS SS … SS
      }
    }
  SEQUENCE {} – file parameters, not used
}
```
___
This implementation of GOST 34.10-2018 do not assume the generation of 
an elliptic curve. Used elliptic curve with these parameters:
```
Group:
Module (p) = 57896044630612021680684936114742422271145183870487080309667128995208157569947
group order (q) = 28948022315306010840342468057371211135571302038761442251594012761075345324491

Elliptic curve parameters:
a = 1
b = 19750513962881385028059495396984460236743646692126413053976069443380491067343

Generator point:
P = (43490682822985073571091311123441225129011272278165566160439297012894969619553,
53273700124912449490307054424387372532482586733448415163119878489682918137700)
```