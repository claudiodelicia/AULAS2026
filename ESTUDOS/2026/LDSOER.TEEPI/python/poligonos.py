poligono = int(input("digite o numero do poligono que vc quer calcular a area: 1.triangulo, 2.retangulo, 3.trapezio, 4.losango, 5.circulo, 6.quadrado"))
if poligono == 1:
   base = float(input("qual a base?"))
   altura = float(input('qual a altura?'))
   print(f"a area do seu triangulo com base:{base} e altura{altura} e de {(base * altura)/ 2}cm²")
elif poligono == 2:
   base = float(input("qual a sua base?"))
   altura = float(input("qual a sua altura?"))
   print(f"a area do seu quadrado com base:{base} e altura{altura} e de {base * altura}cm²")
elif poligono == 3:
   basemaior = float(input("qual a sua base maior?"))
   basemenor = float(input('qual a sua base menor?'))
   altura = float(input("qual a sua altura?"))
   print(f"a area do seu trapezio com base menor{basemenor}, base maior{basemaior} e altura{altura} e de {((basemaior + basemenor)* altura)/ 2 }cm²")
elif poligono == 4:
   diagonalmaior = float(input("qual a sua diagonal maior?"))
   diagonalmenor = float(input("qual a sua diagonal menor?"))
   print(f"a area do seu losango com diagonal maior:{diagonalmaior} e diagonal menor{diagonalmenor} e de {(diagonalmenor * diagonalmaior)/ 2}cm²")
elif poligono == 5:
   pi = float(input("qual valor de pi?"))
   raio = float(input("qual valor do seu raio?"))
   print(f"a area do seu circulo com pi{pi} e raio{raio} e de {(raio**2)* pi}")
elif poligono == 6:
   lado = float(input("qual o lado do seu quadrado"))
   print(f"a area do seu quadrado com lado{lado} e de{lado**2}")
else:
   print("não tem esse poligono")  
   