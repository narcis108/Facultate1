(define serie
    (lambda (n)
      (if (= n 0) '()
          (append (serie (- n 1)) (list (/ (* (+ n 1) n) 2)))
       )
    )
)
; se defineste serie(n)=n(n+1)/2

(define l1 (serie 20))

(define list-head
  (lambda (ls n)
    (if (= n 0)
        '()
        (cons (car ls) (list-head (cdr ls) (- n 1))))))
;apelare (list-head l1 5)	
;primele 5	
      

(define list5
  (lambda (ls n)
    (if (null? ls)
        '()
    (if (< n 20)
        (if (< (+ n 5) 20)
           (cons (list-ref ls n) (list5 ls (+ n 5)))
           (cons (list-ref ls n) ())
    ))
        ))) 
;apelare (list5 l1 0)
;se porneste de la primul element (pozitia 0) si dupa se apeleaza recursiv,
;adunand 5 la pozitia initiala 
;din 5 in 5