(defglobal ?*oll-pv* = 0)
(defglobal ?*pll-pv* = 0)

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
(assert (rotate-macro B yy 100))
(assert (rotate-macro R y 101))
(assert (rotate-macro L y' 102))
(assert (rotate-macro F o 103))
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
	(block (id ?id)  (type ?t&center))
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

(defrule init-face-data
	(block (id ?id) (type ?t&center))
	(facelet (id ?id) (side ?s) (color ?c))
   =>
	(assert (face ?s ?c))
)
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
;;Confirm if the bottom center is white,
;;if it is, enter phase 1
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

(defrule confirm-oll-phase
	?f <- (phase 2)
	(forall
	(block (id ?id1) (type corner|edge) (layer 1))
	(facelet (id ?id1) (type H)  (color w))
	(facelet (id ?id1) (type V1) (side ?s1)(color ?c1))
	(face ?s1 ?c1)
	)
	(forall
	(block (id ?id2) (type edge) (layer 2))
	(facelet (id ?id2) (type V1) (side ?s2)(color ?c2))
	(facelet (id ?id2) (type V2) (side ?s3)(color ?c3))
	(face ?s2 ?c2)
	(face ?s3 ?c3)
	)
	=>
	(printout t "#confirm phase oll" crlf)
	(assert (phase 3))
	(retract ?f)
)
(defrule confirm-pll-phase
	?f <- (phase 3)
	(forall 
	(block (id ?id) (layer 3))
	(facelet (id ?id) (side U) (color y)))
	=>
	(printout t "#confirm phase pll" crlf)
	(assert (phase 4))
	(retract ?f)
)
(defrule confirm-end-phase
	?f <- (phase 4)
	(forall
	(block (id ?id1) (layer 3) (type ~center))
	(facelet (id ?id1) (side U) (color y))
	(facelet (id ?id1) (type V1) (side ?s1) (color ?c1))
	(face ?s1 ?c1)
	)
	=>
	(printout t "#confirm phase end" crlf)
	(printout t "s:5;p:0;h:End" crlf)
	(assert (phase 5))
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
;;(assert (init-macro 3 1 align_up 8 F))
;;(assert (init-macro 4 2 align_up 2 F'F'));;this is not possible
(assert (init-macro 5 2 align_up 4 F'UF))
;;(assert (init-macro 6 2 align_up 8 FU'F'))
;;if already in up positon, flip 
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
	(or (and (test (neq ?s F)) (rotate-macro ?s ?h ?f))
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
	
	(or (and (test (neq ?s1 F)) (rotate-macro ?s1 ?h ?f))
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
	(or (and (test (neq ?s2 F)) (rotate-macro ?s2 ?h ?f))
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
	(or (and (test (neq ?s2 F)) (rotate-macro ?s2 ?h ?f))
		(and (test (eq ?s2 F)) (up-rotate-macro ?s1 F ?h ?f))
	)
	=>
	(printout t "t1:(" ?x " " ?y " " ?z ");")
	(printout t "s:1;f:" ?f ";p:1;h:" ?h crlf)
) 


(defrule init-f21-macro
=>
;;F2L PATTERN 1, corner not OK, edge not OK.
(assert (f2l-macro 1 1 0 6 0 "y'(U'R'UR)" ))
(assert (f2l-macro 1 2 12 0 0 "(URU'R')"))
(assert (f2l-macro 1 3 32 4 0 "(RUR')"))
(assert (f2l-macro 1 4 4 128 0 "y'(R'U'R)"))
(assert (f2l-macro 1 5 128 4 0 "U'(RUR'U)(RUR')"))
(assert (f2l-macro 1 6 4 32 0 "y'U(R'U'RU')(R'U'R)"))
(assert (f2l-macro 1 7 0 132 0 "y'(UR'U'R)(U'2R'UR)"))
(assert (f2l-macro 1 8 36 0 0 "U'(RUR')U2(RU'R')"))
(assert (f2l-macro 1 9 0 36 0 "y'(UR'U')(U'RU)U(R'UR)"))
(assert (f2l-macro 1 10 132 0 0 "(U'RU)(UR'U')U'(RU'R')"))
(assert (f2l-macro 1 11 0 128 4 "y'(U'R'U)(URU')(R'UR)"))
(assert (f2l-macro 1 12 32 0 4 "(URU')(U'R'U)(RU'R')"))
(assert (f2l-macro 1 13 128 0 4 "(RU'R'U)U(RUR')"))
(assert (f2l-macro 1 14 0 32 4 "y'(R'URU'2)(R'U'R)"))
(assert (f2l-macro 1 21 4 8 0 "U'(RU2R')Uy'(R'U'R)"))
(assert (f2l-macro 1 22 4 2 0 "y'U(R'URU')(R'U'R)"))
(assert (f2l-macro 1 23 2 4 0 "(RU'R'U)(RU'R'U)U(RU'R')"))
(assert (f2l-macro 1 24 8 4 0 "U'(RU'R'U)(RUR')"))
(assert (f2l-macro 1 25 6 0 0 "(RUR')U2(RU'R'U)(RU'R')"))
(assert (f2l-macro 1 26 0 12 0 "(RU'R'U)Uy'(R'U'R)"))
(assert (f2l-macro 1 34 0 2 4 "y'(R'U2R)U(R'U'R)"))
(assert (f2l-macro 1 35 2 0 4 "(RUR'U')U'(RUR'U')(RUR')"))
(assert (f2l-macro 1 36 8 0 4 "(RU2R')U'(RUR')"))
(assert (f2l-macro 1 37 0 8 4 "(FURU'R'F')(RU'R')"))

;;F2L PATTERN 2, corner not OK, edge OK.
(assert (f2l-macro 2 15 0 4 0 "U'(RU2R')U(RUR')"))
(assert (f2l-macro 2 16 4 0 0 "U'(RU'R'U)U(RU'R')"))
(assert (f2l-macro 2 19 0 0 4 "(RUR'U')2(RUR')"))

;;F2L PATTERN 3,Corner wrong, layer 2 flipped
(assert (f2l-macro 3 17 0 4 0 "y'U(R'U'RU')y(RUR')"))
(assert (f2l-macro 3 18 4 0 0 "U'(RUR'U)y'(R'U'R)"))
(assert (f2l-macro 3 20 0 0 4 "U'(R'FRF')(RU'R')"))
)
(deffunction f2l-hpos-value (?p ?c ?fc ?rc) 
	(bind ?v1 0)
	(bind ?v2 0)
	(bind ?v3 0)	
	(if (eq ?c ?fc) then (bind ?v1 (integer (** 2 (- ?p 1)))) else
	(if (eq ?c ?rc) then (bind ?v2 (integer (** 2 (- ?p 1)))) else
	(if (eq ?c w) then (bind ?v3 (integer (** 2 (- ?p 1)))))))
	(create$ ?v1 ?v2 ?v3)
)

(deffunction f2l-pattern-match (?pv_f ?pv_r ?pv_w ?hv_f ?hv_r ?hv_w)
	(if (and (= ?hv_f ?pv_f) (= ?hv_r ?pv_r) (= ?hv_w ?pv_w)) then 
		(create$ TRUE O) else 
	(if (and (= ?hv_f (mod (* ?pv_f 4) 255)) 
			 (= ?hv_r (mod (* ?pv_r 4) 255)) 
			 (= ?hv_w (mod (* ?pv_w 4) 255))) then 
		(create$ TRUE U) else
	(if (and (= ?hv_f (mod (* ?pv_f 16) 255)) 
			 (= ?hv_r (mod (* ?pv_r 16) 255)) 
			 (= ?hv_w (mod (* ?pv_w 16) 255))) then 
		(create$ TRUE UU) else
	(if (and (= ?hv_f (mod (* ?pv_f 64) 255)) 
			 (= ?hv_r (mod (* ?pv_r 64) 255)) 
			 (= ?hv_w (mod (* ?pv_w 64) 255))) then 
		(create$ TRUE U') else
		(create$ FALSE N))
	))) 
)


(defrule f2l-pattern-1 "corner not OK, edge not OK."
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (type corner) (status wrong))
	(block (id ?id2) (pos ?p2&:(= ?p2 (+ 3 ?p1))) (status wrong))
	(facelet (id ?id1) (type V1) (side ?s1))
	(facelet (id ?id1) (type V2) (side ?s2))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
    (block (id ?id5&:(= (block-id w ?c1 ?c2) ?id5)) (cord ?x1 ?y1 ?z1) (layer 3))
	(block (id ?id6&:(= (block-id - ?c1 ?c2) ?id6)) (cord ?x2 ?y2 ?z2) (layer 3))
    (facelet (id ?id5) (side U) (pos ?p5) (color ?c5))
	(facelet (id ?id6) (side U) (pos ?p6) (color ?c6))
	(rotate-macro ?s1 ?h1 ?x)
	(f2l-macro 1 ?f ?pv_f ?pv_r ?pv_w ?h2)
	=>
	(bind ?hv1 (f2l-hpos-value ?p5 ?c5 ?c1 ?c2))
	(bind ?hv2 (f2l-hpos-value ?p6 ?c6 ?c1 ?c2))
	(bind ?hv1_1 (nth$ 1 ?hv1))
	(bind ?hv1_2 (nth$ 2 ?hv1))
	(bind ?hv1_3 (nth$ 3 ?hv1))
	(bind ?hv2_1 (nth$ 1 ?hv2))
	(bind ?hv2_2 (nth$ 2 ?hv2))
	(bind ?hv2_3 (nth$ 3 ?hv2))
	(bind ?hv_f (+ ?hv1_1 ?hv2_1))
	(bind ?hv_r (+ ?hv1_2 ?hv2_2))
	(bind ?hv_w (+ ?hv1_3 ?hv2_3))
	(bind ?m (f2l-pattern-match ?pv_f ?pv_r ?pv_w ?hv_f ?hv_r ?hv_w))
	(if (nth$ 1 ?m) then 
		(printout t "s:2;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
		(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
		(if (neq ?s1 F) then (printout t "f:" ?f ";p:1;h:" ?h1 crlf) else		
			(if (eq O (nth$ 2 ?m)) then 
				(printout t "f:" ?f ";p:0;h:" ?h2 crlf) else
				(printout t "f:" ?f ";p:0;h:" (nth$ 2 ?m) ?h2 crlf)
			)
		)	
	)
)

(defrule f2l-pattern-2 "Corner wrong, edge OK."
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (type corner) (status wrong))
	(block (id ?id2) (pos ?p2&:(= ?p2 (+ 3 ?p1))) (cord ?x1 ?y1 ?z1) (status ok))
	(facelet (id ?id1) (type V1) (side ?s1))
	(facelet (id ?id1) (type V2) (side ?s2))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
    (block (id ?id5&:(= (block-id w ?c1 ?c2) ?id5)) (cord ?x2 ?y2 ?z2) (layer 3))
    (facelet (id ?id5) (side U) (pos ?p5) (color ?c5))
	(rotate-macro ?s1 ?h1 ?x)
	(f2l-macro 2 ?f ?pv_f ?pv_r ?pv_w ?h2)
	=>
	(bind ?hv1 (f2l-hpos-value ?p5 ?c5 ?c1 ?c2))
	(bind ?hv_f (nth$ 1 ?hv1))
	(bind ?hv_r (nth$ 2 ?hv1))
	(bind ?hv_w (nth$ 3 ?hv1))
		
	(bind ?m (f2l-pattern-match ?pv_f ?pv_r ?pv_w ?hv_f ?hv_r ?hv_w))
	
	(if (nth$ 1 ?m) then 
		(printout t "s:2;t1:(" ?x1 " " ?y1 " " ?z1 ");" )	
		(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");" )	
		(if (neq ?s1 F) then (printout t "f:" ?f ";p:1;h:" ?h1 crlf) else		
			(if (eq O (nth$ 2 ?m)) then 
				(printout t "f:" ?f ";p:0;h:" ?h2 crlf) else
				(printout t "f:" ?f ";p:0;h:" (nth$ 2 ?m) ?h2 crlf)
			)
		)	
	)
)

(defrule f2l-pattern-3 "Corner wrong, layer 2 flipped"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (type corner) (status wrong))
	(block (id ?id2) (pos ?p2&:(= ?p2 (+ 3 ?p1))) (cord ?x1 ?y1 ?z1) (status flipped))
	(facelet (id ?id1) (type V1) (side ?s1))
	(facelet (id ?id1) (type V2) (side ?s2))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
    (block (id ?id5&:(= (block-id w ?c1 ?c2) ?id5)) (cord ?x2 ?y2 ?z2) (layer 3))
    (facelet (id ?id5) (side U) (pos ?p5) (color ?c5))
	(rotate-macro ?s1 ?h1 ?x)
	(f2l-macro 3 ?f ?pv_f ?pv_r ?pv_w ?h2)
	=>
	(bind ?hv1 (f2l-hpos-value ?p5 ?c5 ?c1 ?c2))
	(bind ?hv_f (nth$ 1 ?hv1))
	(bind ?hv_r (nth$ 2 ?hv1))
	(bind ?hv_w (nth$ 3 ?hv1))
		
	(bind ?m (f2l-pattern-match ?pv_f ?pv_r ?pv_w ?hv_f ?hv_r ?hv_w))
	
	(if (nth$ 1 ?m) then 
		(printout t "s:2;t1:(" ?x1 " " ?y1 " " ?z1 ");" )	
		(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");" )	
		(if (neq ?s1 F) then (printout t "f:" ?f ";p:1;h:" ?h1 crlf) else		
			(if (eq O (nth$ 2 ?m)) then 
				(printout t "f:" ?f ";p:0;h:" ?h2 crlf) else
				(printout t "f:" ?f ";p:0;h:" (nth$ 2 ?m) ?h2 crlf)
			)
		)	
	)
)

(defrule f2l-pattern-4 "Corner OK, edge flipped, figure 31"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (cord ?x1 ?y1 ?z1) (type corner) (status ok))
	(block (id ?id2) (pos ?p2&:(= ?p2 (+ 3 ?p1))) (cord ?x2 ?y2 ?z2) (status flipped))
	(facelet (id ?id1) (type V1) (side ?s1))
	(rotate-macro ?s1 ?h1 ?x)
	=>
	(printout t "s:2;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (neq ?s1 F) then (printout t "f:31;p:1;h:" ?h1 crlf) else
	(printout t "f:31;p:0;h:(RU'R'U)y'(R'U2RU'2)(R'UR)" crlf))
)

(defrule f2l-pattern-5-1 "Corner flipped, edge OK,figure 28"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (cord ?x1 ?y1 ?z1) (type corner) (status flipped))
	(block (id ?id2) (pos ?p2&:(= ?p2 (+ 3 ?p1))) (cord ?x2 ?y2 ?z2) (status ok))
	(facelet (id ?id1) (type V1) (side ?s1) (color w))
	(rotate-macro ?s1 ?h1 ?x)
	=>
	(printout t "s:2;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (neq ?s1 F) then (printout t "p:1;h:" ?h1 crlf) else
	(printout t "f:28;p:0;h:(RUR'U')(RU'2R'U')(RUR')"  crlf))
)

(defrule f2l-pattern-5-2 "Corner flipped, edge OK, figure 27"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (cord ?x1 ?y1 ?z1) (type corner) (status flipped))
	(block (id ?id2) (pos ?p2&:(= ?p2 (+ 3 ?p1))) (cord ?x2 ?y2 ?z2) (status ok))
	(facelet (id ?id1) (type V1) (side ?s1) (color ~w))
	(rotate-macro ?s1 ?h1 ?x)
	=>
	(printout t "s:2;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (neq ?s1 F) then (printout t "f:27;p:3;h:" ?h1 crlf) else
	(printout t "f:27;p:0;h:(RU'R'U)(RU2)(R'URU'R')"  crlf))
)

(defrule f2l-pattern-6-1 "Corner flipped, edge flipped, figure 30"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (cord ?x1 ?y1 ?z1) (type corner) (status flipped))
	(block (id ?id2) (pos ?p2&:(= ?p2 (+ 3 ?p1))) (cord ?x2 ?y2 ?z2) (status flipped))
	(facelet (id ?id1) (type V1) (side ?s1) (color w))
	(rotate-macro ?s1 ?h ?x)
	=>
	(printout t "s:2;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (neq ?s1 F) then (printout t "f:30;p:1;h:" ?h crlf) else
	(printout t "f:30;p:0;h:(RU'R')(U'RU'R'U)y'(R'U'R)" crlf))
)

(defrule f2l-pattern-6-2 "Corner flipped, edge flipped"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (cord ?x1 ?y1 ?z1) (type corner) (status flipped))
	(block (id ?id2) (pos ?p2&:(= ?p2 (+ 3 ?p1))) (cord ?x2 ?y2 ?z2) (status flipped))
	(facelet (id ?id1) (type V1) (side ?s1) (color ~w))
	(rotate-macro ?s1 ?h ?x)
	=>
	(printout t "s:2;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (neq ?s1 F) then (printout t "f:29;p:1;h:" ?h crlf) else
	(printout t "f:29;p:0;h:(RU)F(RUR'U')(F'R')"  crlf))
)

(defrule f2l-pattern-7 "Corner OK, edge on layer 3"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (type corner) (cord ?x1 ?y1 ?z1) (status ok))
	(block (id ?id2) (pos ?p2&:(= ?p2 (+ 3 ?p1))) (status wrong))
	(facelet (id ?id1) (type V1) (side ?s1))
	(facelet (id ?id1) (type V2) (side ?s2))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
    (block (id ?id5&:(= (block-id - ?c1 ?c2) ?id5)) (cord ?x2 ?y2 ?z2) (layer 3))
	(facelet (id ?id5) (type V1) (side ?s3) (color ?c3))	
	(rotate-macro ?s1 ?h1 ?x)
	(up-rotate-macro ?s3 F ?h2 ?y)
	(up-rotate-macro ?s3 R ?h3 ?z)
	=>
	(printout t "s:2;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (eq ?c3 ?c1) then 
		(if (neq ?s1 F) then (printout t "f:32;p:1;h:" ?h1 crlf) else
			(if (eq ?s3 F) then (printout t "f:32;p:0;h:(URU'R'U')y'(R'UR)" crlf) else
				(printout t "f:32;p:0;h:" ?h2 "(URU'R'U')y'(R'UR)" crlf))) 
	else 
		(if (neq ?s1 F) then (printout t "f:33;p:1;h:" ?h1 crlf) else
			(if (eq ?s3 R) then (printout t "f:33;p:0;h:(R'F'RU)(RU'R'F)" crlf) else
				(printout t "f:33;p:0;h:" ?h3 "(R'F'RU)(RU'R'F)" crlf))) 
	)
)

(defrule f2l-pattern-8-1 "Corner flipped, edge on layer 3, pattern 1"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (type corner) (cord ?x1 ?y1 ?z1) (status flipped))
	(facelet (id ?id1) (type V1) (side ?s1)) 
	(facelet (id ?id1) (type V2) (side ?s2) (color w))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
    (block (id ?id5&:(= (block-id - ?c1 ?c2) ?id5)) (cord ?x2 ?y2 ?z2) (layer 3))
	(facelet (id ?id5) (type V1) (side ?s3) (color ?c3))	
	(rotate-macro ?s1 ?h1 ?x)
	(up-rotate-macro ?s3 F ?h2 ?y)
	(up-rotate-macro ?s3 R ?h3 ?z)
	=>
	(printout t "s:2;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (eq ?c3 ?c1) then 
		(if (neq ?s1 F) then (printout t "f:38;p:1;h:" ?h1 crlf) else
			(if (eq ?s3 F) then (printout t "f:38;p:0;h:y'(R'UR)U'(R'UR)" crlf) else
				(printout t "f:38;p:0;h:" ?h2 "y'(R'UR)U'(R'UR)" crlf))) 
	else 
		(if (neq ?s1 F) then (printout t "f:39;p:1;h:" ?h1 crlf) else
			(if (eq ?s3 R) then (printout t "f:39;p:0;h:(RUR')U'(RUR')" crlf) else
				(printout t "f:39;p:0;h:" ?h3 "(RUR')U'(RUR')" crlf))) 
	)
)

(defrule f2l-pattern-8-2 "Corner flipped, edge on layer 3, pattern 2"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (type corner) (cord ?x1 ?y1 ?z1) (status flipped))
	(facelet (id ?id1) (type V1) (side ?s1) (color w)) 
	(facelet (id ?id1) (type V2) (side ?s2))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
    (block (id ?id5&:(= (block-id - ?c1 ?c2) ?id5)) (cord ?x2 ?y2 ?z2) (layer 3))
	(facelet (id ?id5) (type V1) (side ?s3) (color ?c3))	
	(rotate-macro ?s1 ?h1 ?x)
	(up-rotate-macro ?s3 F ?h2 ?y)
	(up-rotate-macro ?s3 R ?h3 ?z)
	=>
	(printout t "s:2;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (eq ?c3 ?c1) then 
		(if (neq ?s1 F) then (printout t "f:41;p:1;h:" ?h1 crlf) else
			(if (eq ?s3 F) then (printout t "f:41;p:0;h:y'(R'U'R)U(R'U'R)" crlf) else
				(printout t "f:41;p:0;h:" ?h2 "y'(R'U'R)U(R'U'R)" crlf))) 
	else 
		(if (neq ?s1 F) then (printout t "f:40;p:1;h:" ?h1 crlf) else
			(if (eq ?s3 R) then (printout t "f:40;p:0;h:(RU'R')U(RU'R')"  crlf) else
				(printout t "f:40;p:0;h:" ?h3 "(RU'R')U(RU'R')" crlf)))
	)
)

(defrule f2l-pattern-9 "Corner not in place, but is a layer 1 corner"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (cord ?x1 ?y1 ?z1) (type corner) (status wrong))
	(facelet (id ?id1) (color w))
	(facelet (id ?id1) (side ?s1) (type V1))	
	(rotate-macro ?s1 ?h ?x)	
	=>
	(printout t "s:2;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(if (neq ?s1 F) then (printout t "f:42;p:3;h:" ?h crlf) else 
	(printout t "f:42;p:2;h:(RUR')"  crlf))
)

(defrule f2l-pattern-10 "edge not in place, but is a layer 2 edge"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 2) (type edge) (cord ?x1 ?y1 ?z1) (status wrong))
	(not (facelet (id ?id1) (color w|y)))
	(facelet (id ?id1) (type V1) (side ?s1))
	(facelet (id ?id1) (type V2) (side ?s2))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
	(block (id ?id2&:(= ?id2 (block-id - ?c1 ?c2))) (cord ?x2 ?y2 ?z2) (layer 3))
	(facelet (id ?id2) (side ?s3) (type V1) (color ?c3))	
	(rotate-macro ?s1 ?h1 ?x)
	(up-rotate-macro ?s3 F ?h2 ?y)
	(up-rotate-macro ?s3 R ?h3 ?z)
	=>
	(printout t "s:2;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (eq ?c3 ?c1) then 
		(if (neq ?s1 F) then (printout t "f:32;p:1;h:" ?h1 crlf) else
			(if (eq ?s3 F) then (printout t "f:32;p:0;h:(URU'R'U')y'(R'UR)" crlf) else
				(printout t "f:32;p:0;h:" ?h2 "(URU'R'U')y'(R'UR)" crlf))) 
	else 
		(if (neq ?s1 F) then (printout t "f:33;p:1;h:" ?h1 crlf) else
			(if (eq ?s3 R) then (printout t "f:33;p:0;h:(R'F'RU)(RU'R'F)" crlf) else
				(printout t "f:33;p:0;h:" ?h3 "(R'F'RU)(RU'R'F)" crlf))) 
	)
	
	
)

(defrule f2l-pattern-11 "edge not in place, but is a layer 2 edge"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 2) (cord ?x1 ?y1 ?z1) (type edge) (status wrong))
	(not (facelet (id ?id1) (color w|y)))
	(facelet (id ?id1) (type V1) (side ?s1))
	(facelet (id ?id1) (type V2) (side ?s2))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
	(block (id ?id2&:(= ?id2 (block-id - ?c1 ?c2)))  (layer 2))	
	(block (id ?id3) (layer 3) (cord ?x2 ?y2 ?z2) (type edge))
	(facelet (id ?id3) (color y))
	(facelet (id ?id3) (type V1) (side ?s3))
	(not (and (block (id ?id4&:(< ?id4 ?id3)) (layer 3) (type edge))
			  (facelet (id ?id4) (color y))))			  
	(rotate-macro ?s1 ?h1 ?x)
	(up-rotate-macro ?s3 R ?h2 ?y)		  
	=>
	(printout t "s:2;t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (neq ?s1 F) then (printout t "f:33;p:3;h:" ?h1 crlf) else 
	(if (neq ?s3 R) then (printout t "f:33;p:2;h:" ?h2 "(R'F'RU)(RU'R'F)" crlf) else 
		(printout t "f:33;p:2;h:(R'F'RU)(RU'R'F)"  crlf)))
)

(defrule init-oll-macro 
=>
(assert (oll-macro 1 521 "(RU2R')(U'RU'R')"))
(assert (oll-macro 2 292 "(RUR'U)(RU2R')"))
(assert (oll-macro 3 325 "(RU)(UR'U'R)2(U'R')"))
(assert (oll-macro 3 325 "(RU2R')(U'RUR')(U'RU'R')"))
(assert (oll-macro 4 2628 "(RU2R')(R'U')(R2U'R2U)(UR)"))
(assert (oll-macro 5 257 "(rUR'U')(r'FRF')"))
(assert (oll-macro 6 320 "(R2D')(RU2R')(DRU2R)"))
(assert (oll-macro 7 516 "F'(rUR'U')(r'FR)"))
(assert (oll-macro 8 3770 "(RU2R')(R'FRF')U2(R'FRF')"))
(assert (oll-macro 9 3798 "(FRUR'U'F')(fRUR'U'f')"))
(assert (oll-macro 10 3506 "(fRUR'U'f')U'(FRUR'U'F')"))
(assert (oll-macro 11 1691 "(fRUR'U'f')U(FRUR'U'F')"))
(assert (oll-macro 12 3282 "(RUR'U)(R'FRF')U2(R'FRF')"))
(assert (oll-macro 13 1175 "(rUR'URU2r')(r'U'RU'R'U2r)"))
(assert (oll-macro 14 3226 "(M'U)(RUR'U')M(R'FRF')"))
(assert (oll-macro 15 1170 "(rUR'U')M2U(RU'R'U')M"))
(assert (oll-macro 16 2758 "f(RUR'U')2f'"))
(assert (oll-macro 17 3668 "R'(F'U'FU')(RUR'U)R"))
(assert (oll-macro 18 2730 "(rUr')(URU'R')2(rU'r')"))
(assert (oll-macro 19 3640 "(RU2R2U')(RU'R'U2)(FRF')"))
(assert (oll-macro 20 422 "(rU'r')U'(rUr')(F'UF)"))
(assert (oll-macro 21 2466 "(r'U'r)(R'U'RU)(r'Ur)"))
(assert (oll-macro 22 707 "(R'FR)U(R'F'R)(FU'F')"))
(assert (oll-macro 23 651 "(rUr')(RUR'U')(rU'r')"))
(assert (oll-macro 24 387 "(RUR'U')(R'FRF')"))
(assert (oll-macro 25 2690 "FRUR'U'F'"))
(assert (oll-macro 26 130 "(RUR'U')r(R'URU')r'"))
(assert (oll-macro 27 18 "(rUR'U'r')(RURU'R')"))
(assert (oll-macro 28 646 "(RUR')(F'U'FU)(RU2R')"))
(assert (oll-macro 29 2242 "R'(FRUR'U'F')(UR)"))
(assert (oll-macro 30 674 "(RUR2U'R')(FRURU'F')"))
(assert (oll-macro 31 1080 "(R'U')(R'FRF')(UR)"))
(assert (oll-macro 32 1283 "(R'U')(FURU'R'F')R"))
(assert (oll-macro 33 1409 "(RU)(B'U'R'URB)R'"))
(assert (oll-macro 34 184 "(B'U'R'URB)"))
(assert (oll-macro 35 3712 "fRUR'U'f'"))
(assert (oll-macro 36 51 "(FRU'R')U'(RUR'F')"))
(assert (oll-macro 37 1185 "(RU2R')(R'FRF')(RU2R')"))
(assert (oll-macro 38 3488 "(r'U2R)(UR'Ur)"))
(assert (oll-macro 39 1547 "(rU2R')(U'RU'r')"))
(assert (oll-macro 40 217 "(r'U'RU')(R'U2r)"))
(assert (oll-macro 41 310 "(rUR'U)(RU2r')"))
(assert (oll-macro 42 1444 "M'(RUR'U)(RU2R')(UM)"))
(assert (oll-macro 43 1099 "U(FRUR'U'F')U(FRUR'U'F')"))
(assert (oll-macro 44 595 "(RUR'U')(R'FR2UR'U'F')"))
(assert (oll-macro 45 2452 "(RUR'U)(R'FRF')(RU2R')"))
(assert (oll-macro 46 343 "(rU)(UR'U'R)2(U'r')"))
(assert (oll-macro 47 2772 "B'(R'U'RU)2B"))
(assert (oll-macro 48 469 "(r'U')(U'RUR')2(Ur)"))
(assert (oll-macro 49 2646 "F(RUR'U')2F'"))
(assert (oll-macro 50 3780 "(r'U)(r2U'(r2U')(r2)(Ur')"))
(assert (oll-macro 51 441 "(RB')(R2F)(R2B)(R2F'R)"))
(assert (oll-macro 52 3208 "(fRUR2U')R'(UR2U'R'f')"))
(assert (oll-macro 53 275 "(RUR'U')(RU'R'F')U'(FRUR')"))
(assert (oll-macro 54 149 "(R'U'RU')(R'U2R)(FRUR'U'F')"))
(assert (oll-macro 55 338 "(RUR'U)(RU2R')(FRUR'U'F')"))
(assert (oll-macro 56 282 "(RUR'U)(RU'R'U')(R'FRF')"))
(assert (oll-macro 57 177 "(R'U'RU')(R'U2R)(RUR'U')(R'FRF')"))
)

(defrule oll-face-value
	(declare (salience 120))
	(phase 3)
	(block (id ?id) (layer 3))
	(facelet (id ?id) (type V1|V2) (color y) (vpos ?p))
	=>
	(bind ?*oll-pv* (+ ?*oll-pv* (facelet-value ?p)))
)

(defrule oll-pattern
	(phase 3)
	(oll-macro ?f ?pv ?h)
	=>
	(if (= ?*oll-pv* ?pv) then 
		(printout t "s:3;p:0;h:" ?h ";f:" ?f crlf) else 
	(if (= ?*oll-pv* (mod (* ?pv 8) 4095)) then 
		(printout t "s:3;p:1;h:U;f:" ?f crlf) else
	(if (= ?*oll-pv* (mod (* ?pv 64) 4095)) then 
		(printout t "s:3;p:1;h:U2;f:" ?f crlf) else
	(if (= ?*oll-pv* (mod (* ?pv 512) 4095)) then 
		(printout t "s:3;p:1;h:U';f:" ?f crlf)
	))))
)

(defrule init-pll-macro 
=>
;clockwize/anticlockwize =1/2, figure number in the manual card, and pattern number, macro
(assert (pll-macro 1 1 3053 "(RU'R)(URUR)(U'R'U'R2)"))
(assert (pll-macro 2 2 3053 "(R2U)(RUR'U')(R'U')(R'UR')"))
(assert (pll-macro 1 3 2925 "(M2U)(M2U)U(M2U)(M2)"))
(assert (pll-macro 2 4 2925 "(M'UM')(M'UM')(M'UM')U2M2U'"))
(assert (pll-macro 1 5 1938 "x'(R2D2)(R'U'R)D2(R'UR')"))
(assert (pll-macro 2 6 1938 "x'(RU'R)D2(R'UR)(D2R2)"))
(assert (pll-macro 4 7 1170 "x'(RU'R'D)(RUR'D')(RUR'D)(RU'R'D')x"));this is a symetric pattern
(assert (pll-macro 5 8 2947 "(RUR'U')(R'F)(R2U'R'U')(RUR'F')"))
(assert (pll-macro 5 9 3857 "(R'U'F')(RUR'U')(R'F)(R2U'R'U')(RUR'UR)"))
(assert (pll-macro 5 10 3171 "(R'UR'd')(R'F'R2U')(R'UR'FRF)"))
(assert (pll-macro 5 11 2163  "(FRU'R')U'(RUR'F')(RUR'U')(R'FRF')"))
(assert (pll-macro 5 12 2016 "z(U'RD')(R2UR'U')R2U(DR')"))
(assert (pll-macro 5 13 3969 "(RUR'F')(RUR'U')(R'F)(R2U'R'U')"))
(assert (pll-macro 5 14 3213 "(R'U2)(RU2R')(FRU)R'(U'R'F')(R2U')"))
(assert (pll-macro 5 15 2835 "(RU'R'U')(RURD)(R'U'RD')(R'U2R'U')"))
(assert (pll-macro 1 16 224 "(R2u'RU')R(UR'uR2)(fR'f')"))
(assert (pll-macro 2 17 28  "(RUR')y'(R2u'RU')R'(UR'uR2)"))
(assert (pll-macro 1 18 14  "(R2uR'U)R'(U'Ru'R2)(F'UF)"))
(assert (pll-macro 2 19 112 "(R'd'F)(R2uR'U)R(U'Ru'R2)"))
(assert (pll-macro 5 20 2275 "(R'U)(RU'R')(F'U'F)(RUR')(FR'F')(RU'R)"))
(assert (pll-macro 5 21 910  "(RUR'U)(RUR'F')(RUR'U')(R'F)(R2U'R'U')(U'RU'R')"))
)
(defrule pll-face-value
(declare (salience 120))
	(phase 4)
	(block (id ?id) (layer 3))
	(facelet (id ?id) (type V1|V2) (side ?s) (color ?c) (vpos ?p))
	(face ?s ?c)
	=>
	(bind ?*pll-pv* (+ ?*pll-pv* (facelet-value ?p)))
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
	(phase 4)
	=>
	(printout t "s:4;f:0;p:1;h:U" crlf)  
)

(defrule pll-pattern
	(phase 4)
	(pll-macro 5 ?f ?pv ?h)
	=>
	(bind ?m (pll-pattern-match ?pv))
	(if (nth$ 1 ?m) then 
		(if (eq O (nth$ 2 ?m)) then 
			(printout t "s:4;f:" ?f ";p:0;h:" ?h crlf)  
		else
			(printout t "s:4;f:" ?f ";p:0;h:" (nth$ 2 ?m) ?h crlf)  
		)
	)
)

(deffunction pll-pattern-out (?c1 ?c2 ?c3 ?d ?f ?pv ?h)
	(bind ?m (pll-pattern-match ?pv))
	(if (nth$ 1 ?m) then
		(if (eq O (nth$ 2 ?m)) then 
			(if (eq ?c1 ?c2) then
				(if (= 1 ?d) then (printout t "s:4;f:" ?f ";p:0;h:" ?h crlf))
			else 
				(if (eq ?c1 ?c3) then
					(if (= 2 ?d) then (printout t "s:4;f:" ?f ";p:0;h:" ?h crlf))
				)
			)
		else
			(if (eq ?c1 ?c2) then
				(if (= 1 ?d) then (printout t "s:4;f:" ?f ";p:0;h:" (nth$ 2 ?m) ?h crlf))
			else 
				(if (eq ?c1 ?c3) then
					(if (= 2 ?d) then (printout t "s:4;f:" ?f ";p:0;h:" (nth$ 2 ?m) ?h crlf))
				)
			)
		)
	)	
)

(deffunction pll-pattern-out-ex (?c1 ?c2 ?c3 ?c4 ?c5 ?c6 ?d ?f ?pv ?h)
	(bind ?m (pll-pattern-match ?pv))
	(if (nth$ 1 ?m) then
		(if (eq O (nth$ 2 ?m)) then 
			(if (and (eq ?c1 ?c3) (eq ?c5 ?c4)) then
				(if (= 1 ?d) then (printout t "s:4;f:" ?f ";p:0;h:" ?h crlf))
			else 
				(if (and (eq ?c2 ?c4) (eq ?c6 ?c3)) then
					(if (= 2 ?d) then (printout t "s:4;f:" ?f ";p:0;h:" ?h crlf))
				)
			)
		else
			(if (and (eq ?c1 ?c3) (eq ?c5 ?c4)) then
				(if (= 1 ?d) then (printout t "s:4;f:" ?f ";p:0;h:" (nth$ 2 ?m) ?h crlf))
			else 
				(if (and (eq ?c2 ?c4) (eq ?c6 ?c3)) then
					(if (= 2 ?d) then (printout t "s:4;f:" ?f ";p:0;h:" (nth$ 2 ?m) ?h crlf))
				)
			)
		)
	)	
)


(defrule pll-pattern-2
	(phase 4)
	(pll-macro ?d ?f&1|2 ?pv ?h)	

	(block (id ?id0) (layer 3) (type edge) (status ok))
	(facelet (id ?id0) (pos ?p0) (side U))
	(facelet (id ?id1) (pos ?p1&:(= 4 (distance ?p0 ?p1))) (side U))
	(facelet (id ?id2) (pos ?p2&:(= 2 (distance ?p2 ?p1))) (side U))	
	(facelet (id ?id3) (pos ?p3&:(= 2 (distance ?p1 ?p3))) (side U))
	
	(facelet (id ?id1) (type V1) (color ?c1))
	(facelet (id ?id2) (type V1) (side ?s2))
	(facelet (id ?id3) (type V1) (side ?s3))
	(face ?s2 ?c2)
	(face ?s3 ?c3)
	=>
	(pll-pattern-out ?c1 ?c2 ?c3 ?d ?f ?pv ?h)
)

(defrule pll-pattern-3
	(phase 4)
	(pll-macro ?d ?f&3|4 ?pv ?h)
	(facelet (id ?id1) (pos 2) (side U))
	(facelet (id ?id2) (pos 6) (side U))
	(facelet (id ?id3) (pos 8) (side U))
	
	(facelet (id ?id1) (type V1) (side ?s1) (color ?c1))
	(facelet (id ?id2) (type V1) (side ?s2))
	(facelet (id ?id3) (type V1) (side ?s3))
	
	(face ?s2 ?c2)
	(face ?s3 ?c3)
	
	=>
	(if (= ?*pll-pv* ?pv) then 
		(if (and (neq ?c1 ?c2) (neq ?c1 ?c3)) then 
			(printout t "s:4;f:" ?f ";p:0;h:y" crlf)
		else 
			(if(eq ?c1 ?c2) then
				(if (= 1 ?d) then (printout t "s:4;f:" ?f ";p:0;h:" ?h crlf))
			else 
				(if (eq ?c1 ?c3) then
					(if (= 2 ?d) then (printout t "s:4;f:" ?f ";p:0;h:" ?h crlf))
				)
			)
		)
	)
)

(defrule pll-pattern-4
	(phase 4)
	(pll-macro ?d ?f&5|6 ?pv ?h)
	(block (id ?id0) (layer 3) (type corner) (status ok))
	(facelet (id ?id0) (pos ?p0) (side U))
	(facelet (id ?id1) (pos ?p1&:(= 4 (distance ?p0 ?p1))) (side U))
	(facelet (id ?id2) (pos ?p2&:(= 2 (distance ?p1 ?p2))) (side U))	
	(facelet (id ?id3) (pos ?p3&:(= 2 (distance ?p3 ?p1))) (side U))	
	(facelet (id ?id1) (type V1) (color ?c1))
	(facelet (id ?id2) (type V1) (side ?s2))
	(facelet (id ?id3) (type V1) (side ?s3))

	(face ?s2 ?c2)
	(face ?s3 ?c3)
	=>
	(pll-pattern-out ?c1 ?c2 ?c3 ?d ?f ?pv ?h)
)

(defrule pll-pattern-5
	(phase 4)
	(pll-macro ?d ?f&16|17 ?pv ?h)
	(block (id ?id0) (layer 3) (type corner) (status ok))
	(facelet (id ?id0) (pos ?p0) (side U))	
	(facelet (id ?id1) (pos ?p1&:(= 4 (distance ?p0 ?p1))) (side U))

	(facelet (id ?id1) (type V1) (color ?c1) (side ?s1))
	(facelet (id ?id1) (type V2) (color ?c2) (side ?s2))
	(face ?s2 ?c3)
	(face ?s1 ?c4)

	(facelet (id ?id2) (pos ?p2&:(= 1 (distance ?p2 ?p1))) (side U))	
	(facelet (id ?id3) (pos ?p3&:(= 1 (distance ?p1 ?p3))) (side U))	
	(facelet (id ?id2) (type V1) (color ?c5))
	(facelet (id ?id3) (type V1) (color ?c6))

	=>
	(pll-pattern-out-ex ?c1 ?c2 ?c3 ?c4 ?c5 ?c6 ?d ?f ?pv ?h)
)

(defrule pll-pattern-6
	(phase 4)
	(pll-macro ?d ?f&18|19 ?pv ?h)
	(block (id ?id0) (layer 3) (type corner) (status ok))
	(facelet (id ?id0) (pos ?p0) (side U))	
	(facelet (id ?id1) (pos ?p1&:(= 4 (distance ?p0 ?p1))) (side U))

	(facelet (id ?id1) (type V2) (color ?c1) (side ?s1))
	(facelet (id ?id1) (type V1) (color ?c2) (side ?s2))
	(face ?s2 ?c3)
	(face ?s1 ?c4)

	(facelet (id ?id2) (pos ?p2&:(= 1 (distance ?p1 ?p2))) (side U))	
	(facelet (id ?id3) (pos ?p3&:(= 1 (distance ?p3 ?p1))) (side U))	
	(facelet (id ?id2) (type V1) (color ?c5))
	(facelet (id ?id3) (type V1) (color ?c6))
	=>
	(pll-pattern-out-ex ?c1 ?c2 ?c3 ?c4 ?c5 ?c6 ?d ?f ?pv ?h)
)

(defrule pll-pattern-7
	(phase 4)
	(pll-macro 4 ?f ?pv ?h)
	(block (id ?id1) (layer 3) (type corner))
	(facelet (id ?id1) (pos 1) (side U))	
	(facelet (id ?id1) (type V1) (color ?c1))
	
	(block (id ?id2) (layer 3) (type corner))
	(facelet (id ?id2) (pos 3) (side U))	
	(facelet (id ?id2) (type V1) (side ?s))
	
	(face ?s ?c2)
	=>
	(bind ?m (pll-pattern-match ?pv))
	(if (nth$ 1 ?m) then 
		(if (eq ?c1 ?c2) then 
			(printout t "s:4;f:" ?f ";p:0;h:y"  crlf)
		 else
			(printout t "s:4;f:" ?f ";p:0;h:" ?h crlf)  
		)
	)
)
