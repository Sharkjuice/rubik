(defglobal ?*oll-pv* = 0)
(defglobal ?*pll-pv* = 0)
(defglobal ?*pll-side-pv* = 0)
(defglobal ?*pll-corner-pv* = 0)


(deftemplate block
   (slot id)
   (multislot cord)
   (slot type)
   (slot pos)
   (slot layer)
   (slot status)
)

(deftemplate facelet
   (slot id)
   (slot side)
   (slot type)
   (slot pos)
   (slot color)
   (slot vpos)
)

(defrule zero-phase-macro
=>
(assert (zero-macro U xx))
(assert (zero-macro F x'))
(assert (zero-macro B x))
(assert (zero-macro R z))
(assert (zero-macro L z'))
(assert (zero-macro D none))
(assert (zero-macro U xx))
)

(defrule rotate-macro "rotate a face to F "
=>
(assert (rotate-macro B F yy 100))
(assert (rotate-macro R F y 101))
(assert (rotate-macro L F y' 102))
(assert (rotate-macro F F o 103))
(assert (rotate-macro B R y 104))
(assert (rotate-macro R R o 105))
(assert (rotate-macro L R yy 106))
(assert (rotate-macro F R y' 107))
)

(defrule up-rotate-macro "rotate the up layer facelet to F or R"
=>
(assert (up-rotate-macro B F UU 200))
(assert (up-rotate-macro R F U 201))
(assert (up-rotate-macro L F U' 202))
(assert (up-rotate-macro F F O 203))
(assert (up-rotate-macro B R U 204))
(assert (up-rotate-macro R R O 205))
(assert (up-rotate-macro L R UU 206))
(assert (up-rotate-macro F R U' 207))
)
  
(defrule init-cord-facelet
	=>
   (assert (cord_facelet x -1 F))
   (assert (cord_facelet x 1 B))
   (assert (cord_facelet y -1 D))
   (assert (cord_facelet y 1 U))
   (assert (cord_facelet z -1 R))
   (assert (cord_facelet z 1 L))
   (assert (cord_facelet x 0 O))
   (assert (cord_facelet y 0 O))
   (assert (cord_facelet z 0 O))
)


(deffunction color-value (?c)
(switch ?c
	(case - then 0)
	(case r then 1) 
	(case g then 2) 
	(case b then 4) 
	(case y then 8) 
	(case w then 16) 
	(case o then 32))
)

(deffunction side-color-value (?c)
(switch ?c
	(case r then 0) 
	(case g then 1) 
	(case b then 2) 
	(case o then 3)
	(case y then 0)
	(case w then 0)
))

(deffunction block-id (?c1 ?c2 ?c3) 
	(bind ?cv1 (color-value ?c1))
	(bind ?cv2 (color-value ?c2))
	(bind ?cv3 (color-value ?c3))
	(+ ?cv1 ?cv2 ?cv3)	
)

(deffunction block-type (?x ?y ?z)
	(bind ?t (+ (* ?x ?x) (* ?y ?y) (* ?z ?z)))
	(switch ?t
	(case 1 then center)  
	(case 2 then edge)  
	(case 3 then corner) 
	(case 0 then inner))
)
(deffunction block-pos(?x ?y ?z)
	(+ (* (+ ?x 1) 9) (* (+ ?y 1) 3) (+ ?z 1))
) 

(deffunction block-layer (?y)
	(+ ?y 2)
)
(deffunction facelet-pos (?s ?x ?y ?z ?t)
	(if (eq ?t center) then (return 9))
	(if (eq ?s F) then 
		(if (and (eq ?y -1) (eq ?z 1)) then (return 1)) 
		(if (and (eq ?y -1) (eq ?z 0)) then (return 2)) 
		(if (and (eq ?y -1) (eq ?z -1)) then (return 3)) 
		(if (and (eq ?y 0) (eq ?z -1)) then (return 4)) 
		(if (and (eq ?y 1) (eq ?z -1)) then (return 5)) 
		(if (and (eq ?y 1) (eq ?z 0)) then (return 6)) 
		(if (and (eq ?y 1) (eq ?z 1)) then (return 7)) 
		(if (and (eq ?y 0) (eq ?z 1)) then (return 8))
	)
	(if (eq ?s R) then (return (facelet-pos F ?z ?y (* -1 ?x) ?t))) 
	(if (eq ?s B) then (return (facelet-pos R ?z ?y (* -1 ?x) ?t))) 
	(if (eq ?s L) then (return (facelet-pos B ?z ?y (* -1 ?x) ?t))) 
	(if (eq ?s U) then (return (facelet-pos F (* -1 ?y) ?x ?z ?t))) 
	(if (eq ?s D) then (return (facelet-pos B (* -1 ?y) ?x ?z ?t))) 
)
(deffunction facelet-value (?p) 
	(integer (** 2 (- ?p 1)))
)

(deffunction side-value (?s)
(switch ?s
	(case F then 0)
	(case R then 4)
	(case B then 16)
	(case L then 64)
	(case U then 0)
	(case D then 0)
))

(deffunction face-number (?s) 
(switch ?s
	(case F then 1)
	(case R then 2)
	(case B then 3)
	(case L then 4)
	(case U then 5)
	(case D then 6)
))

(deffunction facelet-type (?s)
	(if (eq ?s O) then O else 	
	(if (or (eq ?s U) (eq ?s D)) then H else V1))
)
(deffunction distance (?p1 ?p2)
	(bind ?d (- ?p1 ?p2))
	(if (> ?d 0) then ?d else (+ ?d 8)) 
)

(deffunction is-next-facelet (?s1 ?s2)
	(bind ?sn1 (face-number ?s1))
	(bind ?sn2 (face-number ?s2))
	(bind ?d (- ?sn2 ?sn1))
	(if (< ?d 0) then (bind ?d (+ ?d 4)))
	(if (eq ?d 1) then TRUE else FALSE)
)

(deffunction ver-face-pos (?s ?p)
(if (eq F ?s) then (return (- 8 ?p)))
(if (eq R ?s) then (return (- 11 ?p)))
(if (eq B ?s) then (return (- 14 ?p)))
(if (eq L ?s) then (return (- 17 ?p)))
(if (eq U ?s) then (return ?p))
(if (eq D ?s) then (return ?p))
)

(defrule init-blocks
	(phase 0)
	?f <- (blk ?x ?y ?z ?cx ?cy ?cz)
	(cord_facelet x ?x ?fx)
	(cord_facelet y ?y ?fy)
	(cord_facelet z ?z ?fz)
   =>
   	(retract ?f)
    (bind ?id (block-id ?cx ?cy ?cz))
    (bind ?p (block-pos ?x ?y ?z))
	(bind ?t (block-type ?x ?y ?z))
	(bind ?l (block-layer ?y))
	(bind ?px (facelet-pos ?fx ?x ?y ?z ?t))
	(bind ?py (facelet-pos ?fy ?x ?y ?z ?t))
	(bind ?pz (facelet-pos ?fz ?x ?y ?z ?t))
	(bind ?ftx (facelet-type ?fx))
	(bind ?fty (facelet-type ?fy))
	(bind ?ftz (facelet-type ?fz))
	(bind ?vfpx (ver-face-pos ?fx ?px))
	(bind ?vfpy (ver-face-pos ?fy ?py))
	(bind ?vfpz (ver-face-pos ?fz ?pz))
	(assert (block (id ?id) (cord ?x ?y ?z) (status wrong)(pos ?p) (type ?t) (layer ?l)))
	(assert (facelet  (id ?id) (side ?fx) (type ?ftx) (pos ?px) (vpos ?vfpx) (color ?cx)))
	(assert (facelet  (id ?id) (side ?fy) (type ?fty) (pos ?py) (vpos ?vfpy) (color ?cy)))
	(assert (facelet  (id ?id) (side ?fz) (type ?ftz) (pos ?pz) (vpos ?vfpz) (color ?cz)))
)

(defrule init-faces
    (phase 1)
	(block (id ?id)  (type center))
	(facelet (id ?id)  (side ?s) (color ?c))	
	=>
   (assert (face ?s ?c))
)

(defrule remove-extra-faces
   ?f <- (facelet (side O))
   =>
   (retract ?f)
)

(defrule adjust-facelet
	?f1 <- (facelet (id ?id) (side ?s1) (type V1))
	?f2 <- (facelet (id ?id) (side ?s2&~?s1) (type V1))
   =>
   (bind ?o (is-next-facelet ?s1 ?s2))
   (if ?o then 
	(modify ?f1 (type V1)) 
	(modify ?f2 (type V2))
   else
	(modify ?f1 (type V2))
	(modify ?f2 (type V1))
	)   
)
(defrule adjust-center-status
	?f1 <- (block (id ?id) (type center) (status wrong))
   =>
	(modify ?f1 (status ok)) 
)

(defrule adjust-corner-status
	?f1 <- (block (id ?id) (type corner) (status wrong))
	(facelet (id ?id) (side ?s1) (type H))
	(facelet (id ?id) (side ?s2) (type V1))
	(facelet (id ?id) (side ?s3) (type V2))
	(face ?s1 ?c1)
	(face ?s2 ?c2)
	(face ?s3 ?c3)
	(test (eq ?id (block-id ?c1 ?c2 ?c3)))
   =>
	(modify ?f1 (status flipped)) 
)

(defrule adjust-edge-status
	?f1 <- (block (id ?id) (type edge) (status wrong))
	(facelet (id ?id) (side ?s1))
	(facelet (id ?id) (side ?s2&~?s1))
	(face ?s1 ?c1)
	(face ?s2 ?c2)
	(test (eq ?id (block-id - ?c1 ?c2)))
   =>
	(modify ?f1 (status flipped)) 
)

(defrule adjust-corner-status-2
	?f1 <- (block (id ?id) (type corner) (status flipped))
	(facelet (id ?id) (side ?s1) (type H) (color ?c1))
	(facelet (id ?id) (side ?s2) (type V1) (color ?c2))
	(facelet (id ?id) (side ?s3) (type V2) (color ?c3))
	(face ?s1 ?c1)
	(face ?s2 ?c2)
	(face ?s3 ?c3)
   =>
	(modify ?f1 (status ok)) 
)

(defrule adjust-edge-status-2
	?f1 <- (block (id ?id) (type edge) (status flipped))
	(facelet (id ?id) (side ?s1) (color ?c1))
	(facelet (id ?id) (side ?s2&~?s1) (color ?c2))
	(face ?s1 ?c1)
	(face ?s2 ?c2)
   =>
	(modify ?f1 (status ok)) 
)

;;(defrule init-face-data
;;(block (id ?id) (type ?t&center))
;;	(facelet (id ?id) (side ?s) (color ?c))
;;   =>
;;	(assert (face ?s ?c))
;;)
;;Confirm if the bottom center is white,
;;if it is, enter phase 1
(defrule confirm-init-phase
	?f <- (phase 0)
	(not (blk $?))
	(block (id ?id) (layer 1) (type center))
	(facelet (id ?id) (color w))
	=>
	(printout t "#confirm phase 1" crlf)
	(retract ?f)
	(assert (phase 1))
)
;;Confirm if the bottom center and bottom edge is OK,
;;if it is, enter phase 2
(defrule confirm-f2l-phase
	?f <- (phase 1)
	(forall 
	(block (id ?id) (layer 1) (type edge))
	(block (id ?id) (status ok)))
	=>
	(printout t "#confirm phase f2l" crlf)
	(retract ?f)
	(assert (phase 2))
)

(defrule confirm-layer1-phase
	?f <- (phase 2)
	(forall
	(block (id ?id1) (type corner) (layer 1))
	(facelet (id ?id1) (type H)  (color w))
	(facelet (id ?id1) (type V1) (side ?s1)(color ?c1))
	(face ?s1 ?c1)
	)
	=>
	(printout t "#confirm phase layer1" crlf)
	(assert (phase 3))
	(retract ?f)
)

(defrule confirm-oll-phase
	?f <- (phase 3)
	(forall
	(block (id ?id2) (type edge) (layer 2))
	(facelet (id ?id2) (type V1) (side ?s2)(color ?c2))
	(facelet (id ?id2) (type V2) (side ?s3)(color ?c3))
	(face ?s2 ?c2)
	(face ?s3 ?c3)
	)
	=>
	(printout t "#confirm phase oll" crlf)
	(assert (phase 4))
	(retract ?f)
)


(defrule confirm-pll-phase
	?f <- (phase 4)
	(forall 
	(block (id ?id) (layer 3))
	(facelet (id ?id) (side U) (color y)))
	=>
	(printout t "#confirm phase pll" crlf)
	(assert (phase 5))
	(retract ?f)
)

(defrule confirm-end-phase
	?f <- (phase 5)
	(not (block (id ?id) (layer 3) (status ~ok)))
	=>
	(printout t "#confirm phase end" crlf)
	(printout t "s:6;p:0;h:End" crlf)
	(assert (phase 6))
	(retract ?f)
)

(defrule zero-phase-next
	(phase 0)
	(block (id ?id) (cord ?x ?y ?z)(type center))
	(facelet (id ?id) (side ?s&~D) (color w))
	(zero-macro ?s ?h)
	=>
	(printout t "s:0;p:1;h:" ?h crlf)
)
(defrule init-phase-macro
=>
;;move the target face to the up position
(assert (init-macro 1 1 align_up 2 F'F'))
(assert (init-macro 2 1 align_up 4 F'))
(assert (init-macro 5 2 align_up 4 F'UF))
(assert (init-macro 7 align_flip 6 FRUR'))

;;if already aligned,move the target block to bottom
(assert (init-macro 8 align_down 4 F))
(assert (init-macro 9 align_down 6 FF))
(assert (init-macro 10 align_down 8 F'))
)

(defrule init-phase-next-1
	(phase 1)
	(block (id ?id) (cord ?x ?y ?z) (type edge))
	(facelet (id ?id) (color w))
	(facelet (id ?id) (side ?s) (pos ?p&~2) (color ?c&~w))
	(face ?s ?c)
	(or (and (test (neq ?s F)) (rotate-macro ?s F ?h ?f))
		(and (test (eq ?s F)) (init-macro ?f align_down ?p ?h))
	)
	=>
	(printout t "t1:(" ?x " " ?y " " ?z ");")
	(printout t "s:1;f:" ?f ";p:0;h:" ?h crlf)
)

(defrule init-phase-next-2 "edge is on layer3 but fliped"
	(phase 1)
	(block (id ?id) (cord ?x ?y ?z) (layer 3) (type edge))
	(facelet (id ?id) (side ?s1) (color w) (pos 6))
	(facelet (id ?id) (side ?s2) (color ?c&~w))
	(face ?s1 ?c)
	
	(or (and (test (neq ?s1 F)) (rotate-macro ?s1 F ?h ?f))
		(and (test (eq ?s1 F)) (init-macro ?f align_flip 6 ?h))
	)
	=>
	(printout t "t1:(" ?x " " ?y " " ?z ");")
	(printout t "s:1;f:" ?f ";p:1;h:" ?h crlf)
)

(defrule init-phase-next-3 "the edge is flipped, move to layer 3"
	(phase 1)
	(block (id ?id) (cord ?x ?y ?z) (layer 1|2) (type edge))
	(facelet (id ?id) (color w))
	(facelet (id ?id) (side ?s1) (color ?c&~w))
	(facelet (id ?id) (type V1) (pos ?p1) (side ?s2))
	(block (pos 1) (status ?t))
	(not (face ?s1 ?c))
	(or (and (test (neq ?s2 F)) (rotate-macro ?s2 F ?h ?f))
		(and (test (eq ?s2 F)) (test (eq ?t ok)) (init-macro ?f 2 align_up ?p1 ?h))
		(and (test (eq ?s2 F)) (test (neq ?t ok)) (init-macro ?f 1 align_up ?p1 ?h))
	)
	=>
	(printout t "t1:(" ?x " " ?y " " ?z ");")
	(printout t "s:1;f:" ?f ";p:2;h:" ?h crlf)
)

(defrule init-phase-next-4 "the edge on layer 3, adust face"
	(phase 1)
	(block (id ?id) (cord ?x ?y ?z) (layer 3) (type edge))
	(facelet (id ?id) (color w))
	(facelet (id ?id) (type V1) (side ?s1))
	(facelet (id ?id) (color ?c2&~w))
	(face ?s2 ?c2)
	(test (neq ?s1 ?s2))
	(or (and (test (neq ?s2 F)) (rotate-macro ?s2 F ?h ?f))
		(and (test (eq ?s2 F)) (up-rotate-macro ?s1 F ?h ?f))
	)
	=>
	(printout t "t1:(" ?x " " ?y " " ?z ");")
	(printout t "s:1;f:" ?f ";p:1;h:" ?h crlf)
) 


(defrule init-f21-macro
=>
;;F2L PATTERN 1, corner not OK, the ok corner is on layer 3.
(assert (f2l-macro 1 1 V2 "RUR'" ))
(assert (f2l-macro 2 1 V1 "F'U'F"))
(assert (f2l-macro 3 1 H "RU2R'U'"))
;;F2L PATTERN 2, corner not OK, the ok corner is on layer 1.
(assert (f2l-macro 4 2 R "RUR'U'"))
(assert (f2l-macro 5 2 D "F'U'F"))
)
(defrule f2l-pattern-1 "corner not OK，the OK corner is on layer 3."
	(phase 2)
	(block (id ?id1) (layer 1) (type corner) (status wrong) (cord ?x1 ?y1 ?z1))
	(facelet (id ?id1) (type V1) (side ?s1))
	(facelet (id ?id1) (type V2) (side ?s2))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
    (block (id ?id2&:(= (block-id w ?c1 ?c2) ?id2)) (cord ?x2 ?y2 ?z2) 
		(layer 3))
    (facelet (id ?id2) (type V1) (side ?s3))
    (facelet (id ?id2) (type ?s4) (color w))

	(rotate-macro ?s1 F ?h1 ?f1)
	(up-rotate-macro ?s3 F ?h2 ?f2)	
	(f2l-macro ?f3 1 ?s4 ?h3)
	=>
	(printout t "s:2;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "s:2;t2:(" ?x2 " " ?y2 " " ?z2 ");")	
	(if (neq ?s1 F) then (printout t "f:" ?f1 ";p:2;h:" ?h1 crlf) else		
		(if (neq ?s3 F) then (printout t "f:" ?f2 ";p:1;h:" ?h2 crlf) else
			(printout t "f:" ?f3 ";p:0;h:" ?h3 crlf)
		)
	)	
)

(defrule f2l-pattern-2 "corner not OK，the OK corner is on layer 1."
	(phase 2)
	(block (id ?id1) (layer 1) (type corner) (status wrong|flipped)
		 (cord ?x1 ?y1 ?z1))
	(facelet (id ?id1) (color w))
	(facelet (id ?id1) (type V1) (side ?s1) (color ?c1))
	(face ?s2 ?c1) 
	
	(rotate-macro ?s1 F ?h1 ?f1)
	(f2l-macro ?f2 2 ?s4 ?h2)
	=>
	(printout t "s:2;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(if (neq ?s1 F) then (printout t "f:" ?f1 ";p:2;h:" ?h1 crlf) else		
		(printout t "f:" ?f2 ";p:0;h:" ?h2 crlf)
	)	
)

(defrule init-sl2-macro "simple method, layer 1 is OK, macro for layer 2."
=>
;;SL2 PATTERN 1
(assert (sl2-macro 1 1 F "R'U'R'U'R'URUR" ))
(assert (sl2-macro 2 1 B "RURURU'R'U'R'"))
;;SL2 PATTERN 2
(assert (sl2-macro 3 2 F "R'U'R'U'R'URUR"))
)

(defrule sl2-pattern-1 "macro for layer 2, ok edge is on layer 3."
	(phase 3)
	(block (id ?id1) (layer 3) (type edge) (cord ?x1 ?y1 ?z1))
	(not (facelet (id ?id1) (color y)))
	(facelet (id ?id1) (type V1) (side ?s2) (color ?c2))
	(face ?s4 ?c2) 
	(test (or (neq R ?s2) (neq R ?s4)))

	(rotate-macro ?s4 R ?h1 ?f1)
	(up-rotate-macro ?s2 R ?h2 ?f2)	
	=>
	(printout t "s:3;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(if (neq ?s4 R) then (printout t "f:" ?f1 ";p:2;h:" ?h1 crlf) else		
		(if (neq ?s2 R) then (printout t "f:" ?f2 ";p:1;h:" ?h2 crlf))
	)	
)

(defrule sl2-pattern-2 "macro for layer 2, ok edge is on layer 3."
	(phase 3)
	(block (id ?id1) (layer 3) (type edge) (cord ?x1 ?y1 ?z1))
	(not (facelet (id ?id1) (color y)))
	(facelet (id ?id1) (type H) (color ?c1))
	(facelet (id ?id1) (side R) (color ?c2))
	(face ?s3 ?c1) (face R ?c2)
	
	(sl2-macro ?f3 1 ?s3 ?h3)
	=>
	(printout t "s:3;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "f:" ?f3 ";p:0;h:" ?h3 crlf)
)


(defrule sl2-pattern-3 "macro for layer 2, ok edge is on layer 2."
	(phase 3)
	(block (id ?id1) (layer 2) (type edge) (cord ?x1 ?y1 ?z1) (status ~ok))
	(not (facelet (id ?id1) (color y)))
	(facelet (id ?id1) (type V1) (side ?s1))
	
	(rotate-macro ?s1 F ?h1 ?f1)
	(sl2-macro ?f2 2 F ?h2 )		
	=>
	(printout t "s:3;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(if (neq ?s1 F) then (printout t "f:" ?f1 ";p:4;h:" ?h1 crlf) else		
		(printout t "f:" ?f2 ";p:3;h:" ?h2 crlf)
	)	
)

(defrule init-oll-macro 
=>
;;only one yellow block on up face
(assert (oll-macro 8 3770 "FRUR'U'F'"))
(assert (oll-macro 9 3798 "FRUR'U'F'"))
(assert (oll-macro 15 1170 "FRUR'U'F'"))
(assert (oll-macro 10 3506 "FRUR'U'F'"))
(assert (oll-macro 11 1691 "FRUR'U'F'"))
(assert (oll-macro 12 3282 "FRUR'U'F'"))
(assert (oll-macro 13 1175 "FRUR'U'F'"))
(assert (oll-macro 14 3226 "FRUR'U'F'"))

;;3 block line, paralle to F face
(assert (oll-macro 16 2758 "FRUR'U'F'"))
(assert (oll-macro 18 2730 "FRUR'U'F'"))
(assert (oll-macro 25 2690 "FRUR'U'F'"))
(assert (oll-macro 20 422 "FRUR'U'F'"))
(assert (oll-macro 21 2466 "FRUR'U'F'"))
(assert (oll-macro 22 707 "FRUR'U'F'"))
(assert (oll-macro 23 651 "FRUR'U'F'"))
(assert (oll-macro 24 387 "FRUR'U'F'"))
(assert (oll-macro 26 130 "FRUR'U'F'"))
(assert (oll-macro 28 646 "FRUR'U'F'"))
(assert (oll-macro 29 2242 "FRUR'U'F'"))
(assert (oll-macro 30 674 "FRUR'U'F'"))

;;3 block line, need to turn 90
(assert (oll-macro 17 676 "FRUR'U'F'"));;3668
(assert (oll-macro 19 455 "FRUR'U'F'"));;3640
(assert (oll-macro 31 450 "FRUR'U'F'"));;1080
(assert (oll-macro 43 602 "FRUR'U'F'"));;1099

;;3 block right angle
(assert (oll-macro 46 343 "FURU'R'F'"))
(assert (oll-macro 49 2646 "FURU'R'F'"))
(assert (oll-macro 56 282 "FURU'R'F'"))
(assert (oll-macro 27 18 "FURU'R'F'"))
(assert (oll-macro 36 51 "FURU'R'F'"))
(assert (oll-macro 41 310 "FURU'R'F'"))
(assert (oll-macro 53 275 "FURU'R'F'"))
(assert (oll-macro 55 338 "FURU'R'F'"))

;;3 block right angle,need to turn 180
(assert (oll-macro 50 315 "FURU'R'F'"));;3780
(assert (oll-macro 52 562 "FURU'R'F'"));;3208
(assert (oll-macro 33 86 "FURU'R'F'"));;1409
(assert (oll-macro 35 58 "FURU'R'F'"));;3712
(assert (oll-macro 37 2130 "FURU'R'F'"));1185
(assert (oll-macro 38 2102 "FURU'R'F'"));;3488
(assert (oll-macro 42 2326 "FURU'R'F'"));;1444

;;3 block right angle,need to turn -90
(assert (oll-macro 47 2394 "FURU'R'F'"));;2772
(assert (oll-macro 48 1351 "FURU'R'F'"));;469
(assert (oll-macro 51 567 "FURU'R'F'"));;441
(assert (oll-macro 54 2578 "FURU'R'F'"));;149
(assert (oll-macro 34 23 "FURU'R'F'"));;184
(assert (oll-macro 40 539 "FURU'R'F'"));;217
(assert (oll-macro 44 1610 "FURU'R'F'"));;595
(assert (oll-macro 45 2354 "FURU'R'F'"));;2452
(assert (oll-macro 57 534 "(R'U'RU')(R'U2R)(RUR'U')(R'FRF')"));;177

;;3 block right angle,need to turn 90
(assert (oll-macro 32 2074 "FURU'R'F'"));;1283
(assert (oll-macro 39 91 "FURU'R'F'"));1547

;;litter fish
(assert (oll-macro 1 577 "R'U2RUR'UR"));;521
(assert (oll-macro 2 2336 "R'U2RUR'UR"));;292
;;big pattern
(assert (oll-macro 7 264 "R'U2RUR'UR"));;516
(assert (oll-macro 5 2056 "R'U2RUR'UR"));;257
(assert (oll-macro 6 40   "R'U2RUR'UR"));;320
(assert (oll-macro 3 325 "R'U2RUR'UR"))
(assert (oll-macro 4 2376 "R'U2RUR'UR"));;2628
)

(defrule oll-face-value
	(declare (salience 120))
	(phase 4)
	(block (id ?id) (layer 3))
	(facelet (id ?id) (type V1|V2) (color y) (vpos ?p))
	=>
	(bind ?*oll-pv* (+ ?*oll-pv* (facelet-value ?p)))
)

(defrule oll-pattern
	(phase 4)
	(oll-macro ?f ?pv ?h)
	=>
	(if (= ?*oll-pv* ?pv) then 
		(printout t "s:4;p:0;h:" ?h ";f:" ?f crlf) else 
	(if (= ?*oll-pv* (mod (* ?pv 8) 4095)) then 
		(printout t "s:4;p:1;h:U;f:" ?f crlf) else
	(if (= ?*oll-pv* (mod (* ?pv 64) 4095)) then 
		(printout t "s:4;p:1;h:U2;f:" ?f crlf) else
	(if (= ?*oll-pv* (mod (* ?pv 512) 4095)) then 
		(printout t "s:4;p:1;h:U';f:" ?f crlf)
	))))
)

(defrule init-pll-macro 
=>
;;patern 1
(assert (pll-macro 2 6 1938 "x'(RU'RD2R'URD2R2)x"))
(assert (pll-macro 4 7 1170 "x'(RU'RD2R'URD2R2)x"))
(assert (pll-macro 5 10 3171 "x'(RU'RD2R'URD2R2)x"))
(assert (pll-macro 5 11 2163  "x'(RU'RD2R'URD2R2)x"))
(assert (pll-macro 5 14 3213 "x'(RU'RD2R'URD2R2)x"))
(assert (pll-macro 5 20 2275 "x'(RU'RD2R'URD2R2)x"))
(assert (pll-macro 5 21 910  "x'(RU'RD2R'URD2R2)x"))
;;pattern 2
(assert (pll-macro 5 9 2191 "x'(RU'RD2R'URD2R2)x"))
(assert (pll-macro 5 13 3087 "x'(RU'RD2R'URD2R2)x"))
(assert (pll-macro 5 15 2205 "x'(RU'RD2R'URD2R2)x"))
(assert (pll-macro 5 8 3101 "x'(RU'RD2R'URD2R2)x"))
;;pattern 4
(assert (pll-macro 5 12 2079 "x'(RU'RD2R'URD2R2)x"))
(assert (pll-macro 5 120 2061 "x'(RU'RD2R'URD2R2)x"))
;;pattern 5
(assert (pll-macro 1 3 2925 "(RU'R)(URUR)(U'R'U'R')R'"))
;;pattern 6
(assert (pll-macro 1 1 3053 "(RU'R)(URUR)(U'R'U'R')R'"))
)

(defrule pll-face-value
(declare (salience 120))
	(phase 5)
	(block (id ?id) (layer 3))
	(facelet (id ?id) (type V1|V2) (side ?s) (color ?c) (vpos ?p))
	(face ?s ?c)
	=>
	(bind ?*pll-pv* (+ ?*pll-pv* (facelet-value ?p)))
)

(defrule pll-side-value
(declare (salience 120))
	(phase 5)
	(face ?s ?c)
	=>
	(bind ?sv (side-value ?s))
	(bind ?cv (side-color-value ?c))
	(bind ?*pll-side-pv* (+ ?*pll-side-pv* (* ?sv ?cv)))
)

(defrule pll-coner-value
(declare (salience 120))
	(phase 5)
	(block (id ?id) (layer 3) (type corner))
	(facelet (id ?id) (type V2) (side ?s) (color ?c))
	=>
	(bind ?*pll-corner-pv* (+ ?*pll-corner-pv* 
		(* (side-value ?s) (side-color-value ?c))))
)

(defrule pll-coner-match
	(declare (salience 120))
	(phase 5)
	=>
	(if (= ?*pll-corner-pv* (mod (* ?*pll-side-pv* 4) 255)) then 
		(printout t "s:5;f:500;p:0;h:U'" crlf) else 
	(if (= ?*pll-corner-pv* (mod (* ?*pll-side-pv* 16) 255)) then 
		(printout t "s:5;f:500;p:0;h:U2" crlf) else
	(if (= ?*pll-corner-pv* (mod (* ?*pll-side-pv* 64) 255)) then 
		(printout t "s:5;f:500;p:0;h:U" crlf)  
	))) 
)

(deffunction pll-pattern-match (?pv)
	(if (= ?*pll-pv* ?pv) then 
		(create$ TRUE O) else 
	(if (= ?*pll-pv* (mod (* ?pv 8) 4095)) then 
		(create$ TRUE y) else
	(if (= ?*pll-pv* (mod (* ?pv 64) 4095)) then
		(create$ TRUE yy) else
	(if (= ?*pll-pv* (mod (* ?pv 512) 4095)) then
		(create$ TRUE y') else
		(create$ FALSE N))
	))) 
)

(defrule pll-pattern-default
	(phase 5)
	=>
	(printout t "s:5;f:0;p:1;h:U" crlf)  
)


(defrule pll-pattern
	(phase 5)
	(pll-macro ?x ?f ?pv ?h)
	=>
	(bind ?m (pll-pattern-match ?pv))
	(if (nth$ 1 ?m) then 
		(if (eq O (nth$ 2 ?m)) then 
			(printout t "s:5;f:" ?f ";p:0;h:" ?h crlf)  
		else
			(printout t "s:5;f:" ?f ";p:0;h:" (nth$ 2 ?m) ?h crlf)  
		)
	)
)


