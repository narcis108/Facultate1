(define lista1 '(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20))
(define lista2 '(-1 -2 -3 -4 -5 -6 -7 -8 -9 -10 -11 -12 -13 -14 -15 -16 -17 -18 -19 -20))

(define calculeaza
  (lambda (l1 l2)
    (if(null? lista1)
     (print "Lista vida!"l1)
     (print "Minimul lista1: "(apply min l1))
          
    )
    (if(null? l2)
     (print "Lista vida!"l2)
     (print "Minimul lista2: "(apply min l2))
        
    )
    (print "Suma minimelor este: "(+ (apply min l1) (apply min l2)))
  )
)
;(calculeaza lista1 lista2)