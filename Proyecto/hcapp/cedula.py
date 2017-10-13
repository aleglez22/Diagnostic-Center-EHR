import math
def verificar(cedulaRuc):
  num=len(cedulaRuc)
  if num==9:
     cedulaRuc = cedulaRuc[:0] + '0' + cedulaRuc[0:]
     num=len(cedulaRuc)
  array=cedulaRuc
  print (array)
  print (num)

  if (num==10 and cedulaRuc != 0000000000 and cedulaRuc != 2222222222 and cedulaRuc != 9999999999 ):
    total = 0
    digito = int(array[9])*1
    for i in range(num-1):  # -1 o 1
      mult=0
      if i%2 !=0:
        total=total+ (int(array[i])*1)
      else:
        mult=(int(array[i])*2)
        if mult>9:
          total=total+(mult -9)
        else:
          total=total+mult
    decena = total / 10;
    decena = math.floor( decena )
    decena = ( decena + 1 ) * 10
    final =  ( decena - total )

    if (final == 10 and digito == 0) or ( final == digito ):
      return True
    else:
      print( "el digito autoverificador de su cedula es incorrecto debe ser" + str(final))
      return False
  else:
    print("menr de 10 digitos")
    return False









