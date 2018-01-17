
(define serie
    (lambda (n)
      (if (= n 0) '()
          (append (serie (- n 1)) (list (/ (* (+ n 1) n) 2)))
       )
    )
)
; se defineste serie(n)=n(n+1)/2

(define l1 (serie 20))

(define f1
  (lambda (x)
    (* x x)
  )
)

(define f2
  (lambda (lista)
    (write "Prima lista:")
    (newline)
    (write lista)
    (newline)
    (write "Lista formata din patratul fiecarui element din prima lista:")
    (newline)
    (map f1 lista)
  ) 
)