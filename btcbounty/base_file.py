#! /usr/bin/env python

import random
import array
import cPickle
import struct

class CurveFp( object ):
  def __init__( self, p, a, b ):
    self.__p = p
    self.__a = a
    self.__b = b

  def p( self ):
    return self.__p

  def a( self ):
    return self.__a

  def b( self ):
    return self.__b

  def contains_point( self, x, y ):
    return ( y * y - ( x * x * x + self.__a * x + self.__b ) ) % self.__p == 0

class Point( object ):
  def __init__( self, curve, x, y, order = None ):
    self.__curve = curve
    self.__x = x
    self.__y = y
    self.__order = order
    if self.__curve: assert self.__curve.contains_point( x, y )
    if order: assert self * order == INFINITY

  def __add__( self, other ):
    if other == INFINITY: return self
    if self == INFINITY: return other
    assert self.__curve == other.__curve
    if self.__x == other.__x:
      if ( self.__y + other.__y ) % self.__curve.p() == 0:
        return INFINITY
      else:
        return self.double()

    p = self.__curve.p()
    l = ( ( other.__y - self.__y ) * \
          inverse_mod( other.__x - self.__x, p ) ) % p
    x3 = ( l * l - self.__x - other.__x ) % p
    y3 = ( l * ( self.__x - x3 ) - self.__y ) % p
    return Point( self.__curve, x3, y3 )

  def negative (self):
    negative_self = Point( self.__curve, self.__x, -self.__y, self.__order )
    return negative_self


  def __mul__( self, other ):
    def leftmost_bit( x ):
      assert x > 0
      result = 1L
      while result <= x: result = 2 * result
      return result / 2

    e = other
    if self.__order: e = e % self.__order
    if e == 0: return INFINITY
    if self == INFINITY: return INFINITY
    assert e > 0
    e3 = 3 * e
    negative_self = Point( self.__curve, self.__x, -self.__y, self.__order )
    i = leftmost_bit( e3 ) / 2
    result = self
    while i > 1:
      result = result.double()
      if ( e3 & i ) != 0 and ( e & i ) == 0: result = result + self
      if ( e3 & i ) == 0 and ( e & i ) != 0: result = result + negative_self
      i = i / 2
    return result

  def __rmul__( self, other ):
    return self * other

  def __str__( self ):
    if self == INFINITY: return "infinity"
    return "(%d,%d)" % ( self.__x, self.__y )

  def double( self ):
    if self == INFINITY:
      return INFINITY

    p = self.__curve.p()
    a = self.__curve.a()
    l = ( ( 3 * self.__x * self.__x + a ) * \
          inverse_mod( 2 * self.__y, p ) ) % p
    x3 = ( l * l - 2 * self.__x ) % p
    y3 = ( l * ( self.__x - x3 ) - self.__y ) % p
    return Point( self.__curve, x3, y3 )

  def halve( self ):
    if self == INFINITY:
      return INFINITY

    p = self.__curve.p()
    a = self.__curve.a()

    # next three lines must be reverted somehow, then I am a multi millionaire :-)
    # as a=0 in this case, I have eliminated it!
    l = ( ( 3 * self.__x * self.__x ) * inverse_mod( 2 * self.__y, p ) ) % p
    x3 = ( l * l - 2 * self.__x ) % p
    y3 = ( l * ( self.__x - x3 ) - self.__y ) % p


    return Point( self.__curve, x3, y3 )

  def x( self ):
    return self.__x

  def y( self ):
    return self.__y

  def curve( self ):
    return self.__curve

  def order( self ):
    return self.__order

INFINITY = Point( None, None, None )

def inverse_mod( a, m ):
  if a < 0 or m <= a: a = a % m
  c, d = a, m
  uc, vc, ud, vd = 1, 0, 0, 1
  while c != 0:
    q, c, d = divmod( d, c ) + ( c, )
    uc, vc, ud, vd = ud - q*uc, vd - q*vc, uc, vc
  assert d == 1
  if ud > 0: return ud
  else: return ud + m

_p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2FL
_r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141L
_b = 0x0000000000000000000000000000000000000000000000000000000000000007L
_a = 0x0000000000000000000000000000000000000000000000000000000000000000L
_Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798L
_Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8L

class Public_key( object ):
  def __init__( self, generator, point ):
    self.curve = generator.curve()
    self.generator = generator
    self.point = point
    n = generator.order()
    if not n:
      raise RuntimeError, "Generator point must have order."
    if not n * point == INFINITY:
      raise RuntimeError, "Generator point order is bad."
    if point.x() < 0 or n <= point.x() or point.y() < 0 or n <= point.y():
      raise RuntimeError, "Generator point has x or y out of range."


sex = CurveFp( _p, _a, _b )
ass = Point( sex, _Gx, _Gy, _r )
g = ass

if __name__ == "__main__":
  print '======================================================================='
  ### generate privkey
  challenge = Public_key(g, Point( sex, 0x4641b45737ee8e11ae39899060160507d61a30928b0d3e37b6aede29b4ed807bL, 0xb61b706b81dbb5512c556dfd16815cced84e2fa12b5c8b6440057355f0df2a12L))
  for k in range(1,9999999,1):
    ppp=challenge.point

    # find the correct k
    k=1
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    ppp=ppp + k*g
    if ppp.x() == g.x():
        print "found!!!!!!!"
    #    print hex(ppp.x())  + " not matching " + hex(g.x())