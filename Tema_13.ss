(define lista1 (list 5 6 -8))
(define lista2 (list 9 5 1))

(define c1 (make-rectangular (list-ref lista1 0) (list-ref lista2 0)) )
(define c2 (make-rectangular (list-ref lista1 1) (list-ref lista2 1)) )
(define c3 (make-rectangular (list-ref lista1 2) (list-ref lista2 2)) )

(define listac (list c1 c2 c3))

(define r1 (real-part (list-ref listac 0)))
(define r2 (real-part (list-ref listac 1)))
(define r3 (real-part (list-ref listac 2)))

(define listaSortata (list-sort (list r1 r2 r3)))