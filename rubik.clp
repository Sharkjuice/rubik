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

(deftemplate side
   (slot id)
   (slot side)
   (slot type)
   (slot pos)
   (slot color)
   (slot vpos)
)

(defrule zero-phase-hint
=>
(assert (zero-hint U xx))
(assert (zero-hint F x'))
(assert (zero-hint B x))
(assert (zero-hint R z))
(assert (zero-hint L z'))
(assert (zero-hint D none))
(assert (zero-hint U xx))
)

(defrule rotate-hint "rotate a face to F "
=>
(assert (rotate-hint B yy))
(assert (rotate-hint R y))
(assert (rotate-hint L y'))
(assert (rotate-hint F o))
)

(defrule up-rotate-hint "rotate the up layer side to F or R"
=>
(assert (up-rotate-hint B F UU))
(assert (up-rotate-hint R F U))
(assert (up-rotate-hint L F U'))
(assert (up-rotate-hint F F O))
(assert (up-rotate-hint B R U))
(assert (up-rotate-hint R R O))
(assert (up-rotate-hint L R UU))
(assert (up-rotate-hint F R U'))
)
  
(defrule init-cord-side
	=>
   (assert (cord_side x -1 F))
   (assert (cord_side x 1 B))
   (assert (cord_side y -1 D))
   (assert (cord_side y 1 U))
   (assert (cord_side z -1 R))
   (assert (cord_side z 1 L))
   (assert (cord_side x 0 O))
   (assert (cord_side y 0 O))
   (assert (cord_side z 0 O))
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
(deffunction side-pos (?s ?x ?y ?z ?t)
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
	(if (eq ?s R) then (return (side-pos F ?z ?y (* -1 ?x) ?t))) 
	(if (eq ?s B) then (return (side-pos R ?z ?y (* -1 ?x) ?t))) 
	(if (eq ?s L) then (return (side-pos B ?z ?y (* -1 ?x) ?t))) 
	(if (eq ?s U) then (return (side-pos F (* -1 ?y) ?x ?z ?t))) 
	(if (eq ?s D) then (return (side-pos B (* -1 ?y) ?x ?z ?t))) 
)
(deffunction side-value (?p) 
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

(deffunction side-type (?s)
	(if (eq ?s O) then O else 	
	(if (or (eq ?s U) (eq ?s D)) then H else V1))
)
(deffunction distance (?p1 ?p2)
	(bind ?d (- ?p1 ?p2))
	(if (> ?d 0) then ?d else (+ ?d 8)) 
)

(deffunction is-next-side (?s1 ?s2)
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
	(cord_side x ?x ?fx)
	(cord_side y ?y ?fy)
	(cord_side z ?z ?fz)
   =>
   	(retract ?f)
    (bind ?id (block-id ?cx ?cy ?cz))
    (bind ?p (block-pos ?x ?y ?z))
	(bind ?t (block-type ?x ?y ?z))
	(bind ?l (block-layer ?y))
	(bind ?px (side-pos ?fx ?x ?y ?z ?t))
	(bind ?py (side-pos ?fy ?x ?y ?z ?t))
	(bind ?pz (side-pos ?fz ?x ?y ?z ?t))
	(bind ?ftx (side-type ?fx))
	(bind ?fty (side-type ?fy))
	(bind ?ftz (side-type ?fz))
	(bind ?vfpx (ver-face-pos ?fx ?px))
	(bind ?vfpy (ver-face-pos ?fy ?py))
	(bind ?vfpz (ver-face-pos ?fz ?pz))
	(assert (block (id ?id) (cord ?x ?y ?z) (status wrong)(pos ?p) (type ?t) (layer ?l)))
	(assert (side  (id ?id) (side ?fx) (type ?ftx) (pos ?px) (vpos ?vfpx) (color ?cx)))
	(assert (side  (id ?id) (side ?fy) (type ?fty) (pos ?py) (vpos ?vfpy) (color ?cy)))
	(assert (side  (id ?id) (side ?fz) (type ?ftz) (pos ?pz) (vpos ?vfpz) (color ?cz)))
)

(defrule init-faces
	(block (id ?id)  (type ?t&center))
	(side (id ?id)  (side ?s) (color ?c))	
	=>
   (assert (face ?s ?c))
)

(defrule remove-extra-faces
   ?f <- (side (side O))
   =>
   (retract ?f)
)

(defrule adjust-side
	?f1 <- (side (id ?id) (side ?s1) (type V1))
	?f2 <- (side (id ?id) (side ?s2&~?s1) (type V1))
   =>
   (bind ?o (is-next-side ?s1 ?s2))
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
	(side (id ?id) (side ?s1) (type H))
	(side (id ?id) (side ?s2) (type V1))
	(side (id ?id) (side ?s3) (type V2))
	(face ?s1 ?c1)
	(face ?s2 ?c2)
	(face ?s3 ?c3)
	(test (eq ?id (block-id ?c1 ?c2 ?c3)))
   =>
	(modify ?f1 (status flipped)) 
)

(defrule adjust-edge-status
	?f1 <- (block (id ?id) (type edge) (status wrong))
	(side (id ?id) (side ?s1))
	(side (id ?id) (side ?s2&~?s1))
	(face ?s1 ?c1)
	(face ?s2 ?c2)
	(test (eq ?id (block-id - ?c1 ?c2)))
   =>
	(modify ?f1 (status flipped)) 
)

(defrule adjust-corner-status-2
	?f1 <- (block (id ?id) (type corner) (status flipped))
	(side (id ?id) (side ?s1) (type H) (color ?c1))
	(side (id ?id) (side ?s2) (type V1) (color ?c2))
	(side (id ?id) (side ?s3) (type V2) (color ?c3))
	(face ?s1 ?c1)
	(face ?s2 ?c2)
	(face ?s3 ?c3)
   =>
	(modify ?f1 (status ok)) 
)

(defrule adjust-edge-status-2
	?f1 <- (block (id ?id) (type edge) (status flipped))
	(side (id ?id) (side ?s1) (color ?c1))
	(side (id ?id) (side ?s2&~?s1) (color ?c2))
	(face ?s1 ?c1)
	(face ?s2 ?c2)
   =>
	(modify ?f1 (status ok)) 
)

(defrule init-face-data
	(block (id ?id) (type ?t&center))
	(side (id ?id) (side ?s) (color ?c))
   =>
	(assert (face ?s ?c))
)

(defrule confirm-init-phase
	?f <- (phase 0)
	(not (blk $?))
	(block (id ?id) (layer 1) (type center))
	(side (id ?id) (color w))
	=>
	(printout t "#confirm phase 1" crlf)
	(retract ?f)
	(assert (phase 1))
)

(defrule confirm-f2l-phase
	?f <- (phase 1)
	(forall 
	(block (id ?id) (layer 1) (type edge))
	(side (id ?id) (side D) (color w)))
	=>
	(printout t "#confirm phase f2l" crlf)
	(retract ?f)
	(assert (phase 2))
)

(defrule confirm-oll-phase
	?f <- (phase 2)
	(forall
	(block (id ?id1) (type corner|edge) (layer 1))
	(side (id ?id1) (type H)  (color w))
	(side (id ?id1) (type V1) (side ?s1)(color ?c1))
	(face ?s1 ?c1)
	)
	(forall
	(block (id ?id2) (type edge) (layer 2))
	(side (id ?id2) (type V1) (side ?s2)(color ?c2))
	(side (id ?id2) (type V2) (side ?s3)(color ?c3))
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
	(side (id ?id) (side U) (color y)))
	=>
	(printout t "#confirm phase pll" crlf)
	(assert (phase 4))
	(retract ?f)
)
(defrule confirm-end-phase
	?f <- (phase 4)
	(forall
	(block (id ?id1) (layer 3) (type ~center))
	(side (id ?id1) (side U) (color y))
	(side (id ?id1) (type V1) (side ?s1) (color ?c1))
	(face ?s1 ?c1)
	)
	=>
	(printout t "#confirm phase end" crlf)
	(assert (phase 5))
	(retract ?f)
)

(defrule zero-phase-next
	(phase 0)
	(block (id ?id) (cord ?x ?y ?z)(type center))
	(side (id ?id) (side ?s&~D) (color w))
	(zero-hint ?s ?h)
	=>
	(printout t "p:1;h:" ?h crlf)
)
(defrule init-phase-hint
=>
;;move the target face to the up position
(assert (init-hint 1 align_up 2 F'F'))
(assert (init-hint 1 align_up 4 F'))
(assert (init-hint 1 align_up 8 F))
(assert (init-hint 2 align_up 2 F'F'))
(assert (init-hint 2 align_up 4 F'UF))
(assert (init-hint 2 align_up 8 FU'F'))
;;if already in up positon, flip 
(assert (init-hint align_flip 6 FRUR'))

;;if already aligned,move the target block to bottom
(assert (init-hint align_down 4 F))
(assert (init-hint align_down 6 FF))
(assert (init-hint align_down 8 F'))
)

(defrule init-phase-next-1
	(phase 1)
	(block (id ?id) (cord ?x ?y ?z) (type edge))
	(side (id ?id) (color w))
	(side (id ?id) (side ?s) (pos ?p&~2) (color ?c&~w))
	(face ?s ?c)
	(or (and (test (neq ?s F)) (rotate-hint ?s ?h))
		(and (test (eq ?s F)) (init-hint align_down ?p ?h))
	)
	=>
	(printout t "t1:(" ?x " " ?y " " ?z ")")
	(printout t ";f:1;p:0;h:" ?h crlf)
)

(defrule init-phase-next-2 "edge is on layer3 but fliped"
	(phase 1)
	(block (id ?id) (cord ?x ?y ?z) (layer 3) (type edge))
	(side (id ?id) (side ?s1) (color w) (pos 6))
	(side (id ?id) (side ?s2) (color ?c&~w))
	(face ?s1 ?c)
	
	(or (and (test (neq ?s1 F)) (rotate-hint ?s1 ?h))
		(and (test (eq ?s1 F)) (init-hint align_flip 6 ?h))
	)
	=>
	(printout t "t1:(" ?x " " ?y " " ?z ")")
	(printout t ";f:2;p:1;h:" ?h crlf)
)

(defrule init-phase-next-3 "the edge is flipped, move to layer 3"
	(phase 1)
	(block (id ?id) (cord ?x ?y ?z) (layer 1|2) (type edge))
	(side (id ?id) (color w))
	(side (id ?id) (side ?s1) (color ?c&~w))
	(side (id ?id) (type V1) (pos ?p1) (side ?s2))
	(block (pos 1) (status ?t))
	(not (face ?s1 ?c))
	(or (and (test (neq ?s2 F)) (rotate-hint ?s2 ?h))
		(and (test (eq ?s2 F)) (test (eq ?t ok)) (init-hint 2 align_up ?p1 ?h))
		(and (test (eq ?s2 F)) (test (neq ?t ok)) (init-hint 1 align_up ?p1 ?h))
	)
	=>
	(printout t "t1:(" ?x " " ?y " " ?z ")")
	(printout t ";f:3;p:2;h:" ?h crlf)
)

(defrule init-phase-next-4 "the edge on layer 3, adust face"
	(phase 1)
	(block (id ?id) (cord ?x ?y ?z) (layer 3) (type edge))
	(side (id ?id) (color w))
	(side (id ?id) (type V1) (side ?s1))
	(side (id ?id) (color ?c2&~w))
	(face ?s2 ?c2)
	(test (neq ?s1 ?s2))
	(or (and (test (neq ?s2 F)) (rotate-hint ?s2 ?h))
		(and (test (eq ?s2 F)) (up-rotate-hint ?s1 F ?h))
	)
	=>
	(printout t "t1:(" ?x " " ?y " " ?z ")")
	(printout t ";f:4;p:1;h:" ?h crlf)
) 


(defrule init-f21-hint
=>
;;F2L PATTERN 1, corner not OK, edge not OK.
(assert (f2l-hint 1 1 0 6 0 "y'(U'R'UR)" ))
(assert (f2l-hint 1 2 12 0 0 "(URU'R')"))
(assert (f2l-hint 1 3 32 4 0 "(RUR')"))
(assert (f2l-hint 1 4 4 128 0 "y'(R'U'R)"))
(assert (f2l-hint 1 5 128 4 0 "U'(RUR'U)(RUR')"))
(assert (f2l-hint 1 6 4 32 0 "y'U(R'U'RU')(R'U'R)"))
(assert (f2l-hint 1 7 0 132 0 "y'(UR'U'R)(U'2R'UR)"))
(assert (f2l-hint 1 8 36 0 0 "U'(RUR')U2(RU'R')"))
(assert (f2l-hint 1 9 0 36 0 "y'(UR'U')(U'RU)U(R'UR)"))
(assert (f2l-hint 1 10 132 0 0 "(U'RU)(UR'U')U'(RU'R')"))
(assert (f2l-hint 1 11 0 128 4 "y'(U'R'U)(URU')(R'UR)"))
(assert (f2l-hint 1 12 32 0 4 "(URU')(U'R'U)(RU'R'"))
(assert (f2l-hint 1 13 128 0 4 "(RU'R')U2(RUR')"))
(assert (f2l-hint 1 14 0 32 4 "y'(R'URU'2)(R'U'R)"))
(assert (f2l-hint 1 21 4 8 0 "U'(RU'2R'U)y'(R'U'R)"))
(assert (f2l-hint 1 22 4 2 0 "y'U(R'URU')(R'U'R)"))
(assert (f2l-hint 1 23 2 4 0 "(RU'R'U)(RU'R'U)(URU'R')"))
(assert (f2l-hint 1 24 8 4 0 "U'(RU'R'U)(RUR')"))
(assert (f2l-hint 1 25 6 0 0 "(RUR')U2(RU'R'U)(RU'R')"))
(assert (f2l-hint 1 26 0 12 0 "(RU'R'U2)y'(R'U'R)"))
(assert (f2l-hint 1 34 0 2 4 "y'(R'U2)(RUR'U'R)"))
(assert (f2l-hint 1 35 2 0 4 "(RUR'U2)(RUR'U')(RUR')"))
(assert (f2l-hint 1 36 8 0 4 "(RU)(UR'U')RUR')"))
(assert (f2l-hint 1 37 0 8 4 "(FURU'R'F')(RU'R')"))

;;F2L PATTERN 2, corner not OK, edge OK.
(assert (f2l-hint 2 15 0 4 0 "U'(RU'2R'U)(RUR')"))
(assert (f2l-hint 2 16 4 0 0 "U'(RU'R')U2(RU'R')"))
(assert (f2l-hint 2 19 0 0 4 "(RUR'U')2(RUR')"))

;;F2L PATTERN 3,Corner wrong, layer 2 flipped
(assert (f2l-hint 3 17 0 4 0 "y'U(R'U'RU')y(RUR')"))
(assert (f2l-hint 3 18 4 0 0 "U'(RUR'U)y'(R'U'R)"))
(assert (f2l-hint 3 20 0 0 4 "U'(R'FRF')(RU'R')"))
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
	(side (id ?id1) (type V1) (side ?s1))
	(side (id ?id1) (type V2) (side ?s2))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
    (block (id ?id5&:(= (block-id w ?c1 ?c2) ?id5)) (cord ?x1 ?y1 ?z1) (layer 3))
	(block (id ?id6&:(= (block-id - ?c1 ?c2) ?id6)) (cord ?x2 ?y2 ?z2) (layer 3))
    (side (id ?id5) (side U) (pos ?p5) (color ?c5))
	(side (id ?id6) (side U) (pos ?p6) (color ?c6))
	(rotate-hint ?s1 ?h1)
	(f2l-hint 1 ?f ?pv_f ?pv_r ?pv_w ?h2)
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
		(printout t "t1:(" ?x1 " " ?y1 " " ?z1 ");")	
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
	(side (id ?id1) (type V1) (side ?s1))
	(side (id ?id1) (type V2) (side ?s2))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
    (block (id ?id5&:(= (block-id w ?c1 ?c2) ?id5)) (cord ?x2 ?y2 ?z2) (layer 3))
    (side (id ?id5) (side U) (pos ?p5) (color ?c5))
	(rotate-hint ?s1 ?h1)
	(f2l-hint 2 ?f ?pv_f ?pv_r ?pv_w ?h2)
	=>
	(bind ?hv1 (f2l-hpos-value ?p5 ?c5 ?c1 ?c2))
	(bind ?hv_f (nth$ 1 ?hv1))
	(bind ?hv_r (nth$ 2 ?hv1))
	(bind ?hv_w (nth$ 3 ?hv1))
		
	(bind ?m (f2l-pattern-match ?pv_f ?pv_r ?pv_w ?hv_f ?hv_r ?hv_w))
	
	(if (nth$ 1 ?m) then 
		(printout t "t1:(" ?x1 " " ?y1 " " ?z1 ");" )	
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
	(side (id ?id1) (type V1) (side ?s1))
	(side (id ?id1) (type V2) (side ?s2))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
    (block (id ?id5&:(= (block-id w ?c1 ?c2) ?id5)) (cord ?x2 ?y2 ?z2) (layer 3))
    (side (id ?id5) (side U) (pos ?p5) (color ?c5))
	(rotate-hint ?s1 ?h1)
	(f2l-hint 3 ?f ?pv_f ?pv_r ?pv_w ?h2)
	=>
	(bind ?hv1 (f2l-hpos-value ?p5 ?c5 ?c1 ?c2))
	(bind ?hv_f (nth$ 1 ?hv1))
	(bind ?hv_r (nth$ 2 ?hv1))
	(bind ?hv_w (nth$ 3 ?hv1))
		
	(bind ?m (f2l-pattern-match ?pv_f ?pv_r ?pv_w ?hv_f ?hv_r ?hv_w))
	
	(if (nth$ 1 ?m) then 
		(printout t "t1:(" ?x1 " " ?y1 " " ?z1 ");" )	
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
	(side (id ?id1) (type V1) (side ?s1))
	(rotate-hint ?s1 ?h1)
	=>
	(printout t "t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (neq ?s1 F) then (printout t "f:31;p:1;h:" ?h1 crlf) else
	(printout t "f:31;p:0;h:(RU'R'U)y'(R'U2RU'2)(R'UR)" crlf))
)

(defrule f2l-pattern-5-1 "Corner flipped, edge OK,figure 28"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (cord ?x1 ?y1 ?z1) (type corner) (status flipped))
	(block (id ?id2) (pos ?p2&:(= ?p2 (+ 3 ?p1))) (cord ?x2 ?y2 ?z2) (status ok))
	(side (id ?id1) (type V1) (side ?s1) (color w))
	(rotate-hint ?s1 ?h1)
	=>
	(printout t "t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (neq ?s1 F) then (printout t "p:1;h:" ?h1 crlf) else
	(printout t "f:28;p:0;h:(RUR'U')(RU'2R'U')(RUR')"  crlf))
)

(defrule f2l-pattern-5-2 "Corner flipped, edge OK, figure 27"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (cord ?x1 ?y1 ?z1) (type corner) (status flipped))
	(block (id ?id2) (pos ?p2&:(= ?p2 (+ 3 ?p1))) (cord ?x2 ?y2 ?z2) (status ok))
	(side (id ?id1) (type V1) (side ?s1) (color ~w))
	(rotate-hint ?s1 ?h1)
	=>
	(printout t "t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (neq ?s1 F) then (printout t "f:27;p:3;h:" ?h1 crlf) else
	(printout t "f:27;p:0;h:(RU'R'U)(RU2)(R'URU'R')"  crlf))
)

(defrule f2l-pattern-6-1 "Corner flipped, edge flipped, figure 30"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (cord ?x1 ?y1 ?z1) (type corner) (status flipped))
	(block (id ?id2) (pos ?p2&:(= ?p2 (+ 3 ?p1))) (cord ?x2 ?y2 ?z2) (status flipped))
	(side (id ?id1) (type V1) (side ?s1) (color w))
	(rotate-hint ?s1 ?h)
	=>
	(printout t "t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (neq ?s1 F) then (printout t "f:30;p:1;h:" ?h crlf) else
	(printout t "f:30;p:0;h:(RU'R')(U'RU'R'U)y'(R'U'R)" crlf))
)

(defrule f2l-pattern-6-2 "Corner flipped, edge flipped"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (cord ?x1 ?y1 ?z1) (type corner) (status flipped))
	(block (id ?id2) (pos ?p2&:(= ?p2 (+ 3 ?p1))) (cord ?x2 ?y2 ?z2) (status flipped))
	(side (id ?id1) (type V1) (side ?s1) (color ~w))
	(rotate-hint ?s1 ?h)
	=>
	(printout t "t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (neq ?s1 F) then (printout t "f:29;p:1;h:" ?h crlf) else
	(printout t "f:29;p:0;h:(RU)F(RUR'U')(F'R')"  crlf))
)

(defrule f2l-pattern-7 "Corner OK, edge on layer 3"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 1) (type corner) (cord ?x1 ?y1 ?z1) (status ok))
	(block (id ?id2) (pos ?p2&:(= ?p2 (+ 3 ?p1))) (status wrong))
	(side (id ?id1) (type V1) (side ?s1))
	(side (id ?id1) (type V2) (side ?s2))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
    (block (id ?id5&:(= (block-id - ?c1 ?c2) ?id5)) (cord ?x2 ?y2 ?z2) (layer 3))
	(side (id ?id5) (type V1) (side ?s3) (color ?c3))	
	(rotate-hint ?s1 ?h1)
	(up-rotate-hint ?s3 F ?h2)
	(up-rotate-hint ?s3 R ?h3)
	=>
	(printout t "t1:(" ?x1 " " ?y1 " " ?z1 ");")	
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
	(side (id ?id1) (type V1) (side ?s1)) 
	(side (id ?id1) (type V2) (side ?s2) (color w))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
    (block (id ?id5&:(= (block-id - ?c1 ?c2) ?id5)) (cord ?x2 ?y2 ?z2) (layer 3))
	(side (id ?id5) (type V1) (side ?s3) (color ?c3))	
	(rotate-hint ?s1 ?h1)
	(up-rotate-hint ?s3 F ?h2)
	(up-rotate-hint ?s3 R ?h3)
	=>
	(printout t "t1:(" ?x1 " " ?y1 " " ?z1 ");")	
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
	(side (id ?id1) (type V1) (side ?s1) (color w)) 
	(side (id ?id1) (type V2) (side ?s2))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
    (block (id ?id5&:(= (block-id - ?c1 ?c2) ?id5)) (cord ?x2 ?y2 ?z2) (layer 3))
	(side (id ?id5) (type V1) (side ?s3) (color ?c3))	
	(rotate-hint ?s1 ?h1)
	(up-rotate-hint ?s3 F ?h2)
	(up-rotate-hint ?s3 R ?h3)
	=>
	(printout t "t1:(" ?x1 " " ?y1 " " ?z1 ");")	
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
	(side (id ?id1) (color w))
	(side (id ?id1) (side ?s1) (type V1))	
	(rotate-hint ?s1 ?h)	
	=>
	(printout t "t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(if (neq ?s1 F) then (printout t "f:42;p:3;h:" ?h crlf) else 
	(printout t "f:42;p:2;h:(RUR')"  crlf))
)

(defrule f2l-pattern-10 "edge not in place, but is a layer 2 edge"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 2) (type edge) (cord ?x1 ?y1 ?z1) (status wrong))
	(not (side (id ?id1) (color w|y)))
	(side (id ?id1) (type V1) (side ?s1))
	(side (id ?id1) (type V2) (side ?s2))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
	(block (id ?id2&:(= ?id2 (block-id - ?c1 ?c2))) (cord ?x2 ?y2 ?z2) (layer 3))
	(side (id ?id2) (side ?s3) (type V1) (color ?c3))	
	(rotate-hint ?s1 ?h1)
	(up-rotate-hint ?s3 F ?h2)
	(up-rotate-hint ?s2 R ?h3)
	=>
	(printout t "t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (eq ?c3 ?c1) then 
		(if (neq ?s1 F) then (printout t "f:32;p:3;h:" ?h1 crlf) 
		else (printout t "f:32;p:2;h:" ?h2 "(URU'R'U')y'(R'UR)" crlf)) 
	else 
		(if (neq ?s1 F) then (printout t "f:33;p:3;h:" ?h1 crlf) 
		else (printout t "f:33;p:2;h:" ?h3 "(R'F'RU)(RU'R'F)" crlf)) 
	)
)

(defrule f2l-pattern-11 "edge not in place, but is a layer 2 edge"
	(phase 2)
	(block (id ?id1) (pos ?p1) (layer 2) (cord ?x1 ?y1 ?z1) (type edge) (status wrong))
	(not (side (id ?id1) (color w|y)))
	(side (id ?id1) (type V1) (side ?s1))
	(side (id ?id1) (type V2) (side ?s2))
	(face ?s1 ?c1) (face ?s2 ?c2)
	
	(block (id ?id2&:(= ?id2 (block-id - ?c1 ?c2)))  (layer 2))	
	(block (id ?id3) (layer 3) (cord ?x2 ?y2 ?z2) (type edge))
	(side (id ?id3) (color y))
	(side (id ?id3) (type V1) (side ?s3))
	(not (and (block (id ?id4&:(< ?id4 ?id3)) (layer 3) (type edge))
			  (side (id ?id4) (color y))))			  
	(rotate-hint ?s1 ?h1)
	(up-rotate-hint ?s3 R ?h2)		  
	=>
	(printout t "t1:(" ?x1 " " ?y1 " " ?z1 ");")	
	(printout t "t2:(" ?x2 " " ?y2 " " ?z2 ");")
	(if (neq ?s1 F) then (printout t "f:33;p:3;h:" ?h1 crlf) else 
	(if (neq ?s3 R) then (printout t "f:33;p:2;h:" ?h2 "(R'F'RU)(RU'R'F)" crlf) else 
		(printout t "f:33;p:2;h:(R'F'RU)(RU'R'F)"  crlf)))
)

(defrule init-oll-hint 
=>
(assert (oll-hint 1 521 "(RU'2R')(U'RU'R')"))
(assert (oll-hint 2 292 "(RUR'U)(RU2R')"))
(assert (oll-hint 3 325 "(RU'2)(R'U'RUR'U')(RU'R')"))
(assert (oll-hint 4 2628 "(RU'2)(R'2U')(R2U')(R'2U'2R)"))
(assert (oll-hint 5 257 "(rUR'U')(rFRF')"))
(assert (oll-hint 6 320 "(R2D')(RU2R'D)(RU2R)"))
(assert (oll-hint 7 516 "(F')(rUR'U')(RU2R)"))
(assert (oll-hint 8 3770 "(RU'2)(R'2FRF')U2(R'FRF')"))
(assert (oll-hint 9 3798 "F(RUR'U')F'f(RUR'U')f'"))
(assert (oll-hint 10 3056 "f(RUR'U')f'U'F(RUR'U')F'"))
(assert (oll-hint 11 1691 "f(RUR'U')f'UF(RUR'U')F'"))
(assert (oll-hint 12 3282 "(RUR'U)(R'FRF')U2(R'FRF')"))
(assert (oll-hint 13 1175 "(rUR'U)(RU'2r')(r'U'RU')(R'U2r)"))
(assert (oll-hint 14 3226 "(r'RU)(RUR'U'r)(R'2FRF')"))
(assert (oll-hint 15 1170 "(rUR'U')M'2U(RU'R'U')M'"))
(assert (oll-hint 16 2758 "f(RUR'U')2f'"))
(assert (oll-hint 17 3668 "(R'F'U'FU')(RUR'UR)"))
(assert (oll-hint 18 2730 "(rUr')(URU'R')2(rU'r')"))
(assert (oll-hint 19 455 "R'F'(RURU')(R2F'R2)(U'R'URUR')"))
(assert (oll-hint 20 422 "(rU'r'U')(rUr')(F'UF)"))
(assert (oll-hint 21 2466 "(r'U'r)(R'U'RU)(rUr)"))
(assert (oll-hint 22 707 "(R'FRUR'F'R)(FU'F')"))
(assert (oll-hint 23 651 "(rUr')(RUR'U')(rU'r')"))
(assert (oll-hint 24 387 "(RUR'U')(R'FRF')"))
(assert (oll-hint 25 2690 "F(RUR'U')F'"))
(assert (oll-hint 26 130 "(RUR'U')r(R'URU')r'"))
(assert (oll-hint 27 18 "(rUR'U')(rRU)(RU'R')"))
(assert (oll-hint 28 646 "(RUR'F'U'F)U(RU2R')"))
(assert (oll-hint 29 2242 "(R'FRUR'U')(F'UR)"))
(assert (oll-hint 30 674 "(RUR2U')(R'F)(RURU')F"))
(assert (oll-hint 31 1080 "(R'U')(R'FRF')(UR)"))
(assert (oll-hint 32 1283 "(R'U'F)(URU'R')(F'R)"))
(assert (oll-hint 33 1409 "(RU)(B'U')(R'URBR')"))
(assert (oll-hint 34 184 "(B'U')(R'URB)"))
(assert (oll-hint 35 3712 "f(RUR'U')f'"))
(assert (oll-hint 36 51 "F(RU'R'U'RU)(R'F')"))
(assert (oll-hint 37 1185 "(RU'2R'2FRF')(RU'2R')"))
(assert (oll-hint 38 3488 "r'(U2)(RUR'U)r"))
(assert (oll-hint 39 1547 "r(U'2)(R'U'RU')r"))
(assert (oll-hint 40 217 "r'(U'RU'R'U2)r"))
(assert (oll-hint 41 310 "r(UR'URU'2)r'"))
(assert (oll-hint 42 1444 "r'(R2UR'U)(RU'2R'U)(rR')"))
(assert (oll-hint 43 1099 "(UF)(RUR'U')F'UF(RUR'U')F'"))
(assert (oll-hint 44 595 "(RUR'U')(R'FR2)(UR'U'F')"))
(assert (oll-hint 45 2452 "(RUR'U)(R'FRF')(RU'2R')"))
(assert (oll-hint 46 343 "(rU'2)(R'U'RUR'U')(RU'r')"))
(assert (oll-hint 47 2772 "B'(R'U'RU)2B"))
(assert (oll-hint 48 469 "(r'U2)(RUR'U')(RUR'U)r"))
(assert (oll-hint 49 2646 "F(RUR'U')2F'"))
(assert (oll-hint 50 3780 "(r'U)(r2U'r'2U')(r2Ur')"))
(assert (oll-hint 51 441 "(RB')(R2F)(R2B)(R2F'R)"))
(assert (oll-hint 52 3208 "f(RUR'2U')(R'U)(R2U'R')f'"))
(assert (oll-hint 53 275 "(RUR'U')(RU'R'F'U'F)(RUR')"))
(assert (oll-hint 54 149 "(R'U'RU'R'U2)(RFRUR'U'F')"))
(assert (oll-hint 55 338 "(RUR'U)(RU'2R'F)(RUR'U')F'"))
(assert (oll-hint 56 282 "(RUR'U)(RU'R'U')(R'FRF')"))
(assert (oll-hint 57 177 "(R'U'RU')(R'U2R)(RUR'U')(R'FRF')"))
)

(defrule oll-face-value
	(declare (salience 120))
	(phase 3)
	(block (id ?id) (layer 3))
	(side (id ?id) (type V1|V2) (color y) (vpos ?p))
	=>
	(bind ?*oll-pv* (+ ?*oll-pv* (side-value ?p)))
)

(defrule oll-pattern
	(phase 3)
	(oll-hint ?f ?pv ?h)
	=>
	(if (= ?*oll-pv* ?pv) then 
		(printout t "p:0;h:" ?h ";f:" ?f crlf) else 
	(if (= ?*oll-pv* (mod (* ?pv 8) 4095)) then 
		(printout t "p:1;h:U;f:" ?f crlf) else
	(if (= ?*oll-pv* (mod (* ?pv 64) 4095)) then 
		(printout t "p:1;h:UU;f:" ?f crlf) else
	(if (= ?*oll-pv* (mod (* ?pv 512) 4095)) then 
		(printout t "p:1;h:U';f:" ?f crlf)
	))))
)

(defrule init-pll-hint 
=>
(assert (pll-hint 1 1 3053 "(RU'R)(URUR)(U'R'U'R2)"))
(assert (pll-hint 2 2 3053 "(R2U)(RUR'U')(R'U')(R'UR')"))
(assert (pll-hint 1 3 2925 "M2UM2U2M2UM2"))
(assert (pll-hint 2 4 2925 "M'U(M'2U)2M'U2M'2U'"))
(assert (pll-hint 2 5 1938 "x'R2D2(R'U'R)D2(R'UR')"))
(assert (pll-hint 1 6 1938 "x'(RU'R)D2(R'UR)(D2R2)"))
(assert (pll-hint 5 7 1170 "x'(RU'R'D)(RUR'D')(RUR'D)(RU'R'D')x"))
(assert (pll-hint 5 8 2947 "(RUR'U')(R'F)(R2U'R'U')(RUR'F')"))
(assert (pll-hint 5 9 3857 "(R'U'F')(RUR'U')(R'F)(R2U'R'U')(RUR'UR)"))
(assert (pll-hint 5 10 3171 "(R'UR'd')(R'F'R2U')(R'UR'FRF)"))
(assert (pll-hint 5 11 2163  "F(RU'R'U')(RUR'F')(RUR'U')(R'FRF')"))
(assert (pll-hint 5 12 2016 "z(U'RD')(R2UR'U')R2U(DR')"))
(assert (pll-hint 5 13 3969 "(RUR'F')(RUR'U')(R'F)(R2U'R'U')"))
(assert (pll-hint 5 14 3213 "(R'U2)(RU'2)(R'FRUR'U')(R'F'R2U')"))
(assert (pll-hint 5 15 2835 "(RU'R'U')(RURD)(R'U'RD')(R'U2R'U')"))
(assert (pll-hint 1 16 224 "(R'2u'RU'R)(UR'u)(R2fR'f')"))
(assert (pll-hint 2 17 28  "(RUR')y'(R2u'RU')(R'UR'uR2)"))
(assert (pll-hint 2 18 14  "(R2u)(R'UR'U')(Ru')(R'2F'UF)"))
(assert (pll-hint 1 19 112 "(R'd'F)(R2u)(R'U)(RU'Ru'R'2)"))
(assert (pll-hint 5 20 2275 "(R'URU')(R'F'U')(FRUR'F)(R'F'RU'R)"))
(assert (pll-hint 5 21 910  "(RUR'U)(RUR'F')(RUR'U')(R'F)(R2U'R'U2)(RU'R')"))
;(assert (pll-hint 5 22 1904  "(RUR'U)(RUR'F')(RUR'U')(R'F)(R2U'R'U2)(RU'R')"))
)
(defrule pll-face-value
(declare (salience 120))
	(phase 4)
	(block (id ?id) (layer 3))
	(side (id ?id) (type V1|V2) (side ?s) (color ?c) (vpos ?p))
	(face ?s ?c)
	=>
	(bind ?*pll-pv* (+ ?*pll-pv* (side-value ?p)))
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
	(printout t "f:0;p:1;h:U" crlf)  
)

(defrule pll-pattern
	(phase 4)
	(pll-hint 5 ?f ?pv ?h)
	=>
	(bind ?m (pll-pattern-match ?pv))
	(if (nth$ 1 ?m) then 
		(if (eq O (nth$ 2 ?m)) then 
			(printout t "f:" ?f ";p:0;h:" ?h crlf)  
		else
			(printout t "f:" ?f ";p:0;h:" (nth$ 2 ?m) ?h crlf)  
		)
	)
)

(deffunction pll-pattern-out (?c1 ?c3 ?d ?f ?pv ?h)
	(bind ?m (pll-pattern-match ?pv))
	(if (nth$ 1 ?m) then
		(if (eq O (nth$ 2 ?m)) then 
			(if (eq ?c1 ?c3) then
				(if (= 1 ?d) then (printout t "f:" ?f ";p:0;h:" ?h crlf))
			else 
				(if (= 2 ?d) then (printout t "f:" ?f ";p:0;h:" ?h crlf)))
		else
			(if (eq ?c1 ?c3) then
				(if (= 1 ?d) then (printout t "f:" ?f ";p:0;h:" (nth$ 2 ?m) ?h crlf))
			else 
				(if (= 2 ?d) then (printout t "f:" ?f ";p:0;h:" (nth$ 2 ?m) ?h crlf)))
		)
	)	
)


(defrule pll-pattern-2
	(phase 4)
	(pll-hint ?d ?f&1|2 ?pv ?h)	

	(block (id ?id1) (layer 3) (type edge) (status ok))
	(side (id ?id1) (pos ?p1) (side U))
	(side (id ?id2) (pos ?p2&:(= 2 (distance ?p2 ?p1))) (side U))
	(side (id ?id3) (pos ?p3&:(= 2 (distance ?p1 ?p3))) (side U))	
	(side (id ?id2) (type V1) (side ?s2) (color ?c2))
	(side (id ?id3) (type V1) (side ?s3) (color ?c3))
	(face ?s2 ?c1)
	=>
	(pll-pattern-out ?c1 ?c3 ?d ?f ?pv ?h)
)

(defrule pll-pattern-3
	(phase 4)
	(pll-hint ?d ?f&3|4 ?pv ?h)
	(side (id ?id1) (pos 2) (side U))
	(side (id ?id2) (pos 4) (side U))
	(side (id ?id1) (type V1) (side ?s1) (color ?c1))
	(side (id ?id2) (type V1) (side ?s2))
	(face ?s2 ?c3)
	=>
	(pll-pattern-out ?c1 ?c3 ?d ?f ?pv ?h)
)

(defrule pll-pattern-4
	(phase 4)
	(pll-hint ?d ?f&5|6 ?pv ?h)
	(block (id ?id1) (layer 3) (type corner) (status ok))
	(side (id ?id1) (pos ?p1) (side U))
	(side (id ?id2) (pos ?p2&:(= 3 (distance ?p2 ?p1))) (side U))
	(side (id ?id3) (pos ?p3&:(= 3 (distance ?p1 ?p3))) (side U))	
	(side (id ?id2) (type V1) (side ?s2) (color ?c2))
	(side (id ?id3) (type V1) (side ?s3) (color ?c3))
	(face ?s2 ?c1)
	=>
	(pll-pattern-out ?c1 ?c3 ?d ?f ?pv ?h)
)

(defrule pll-pattern-5
	(phase 4)
	(pll-hint ?d ?f&16|17 ?pv ?h)
	(block (id ?id1) (layer 3) (type corner) (status ok))
	(side (id ?id1) (pos ?p1) (side U))	
	(side (id ?id2) (pos ?p2&:(= 3 (distance ?p2 ?p1))) (side U))
	(side (id ?id3) (pos ?p3&:(= 3 (distance ?p1 ?p3))) (side U))	
	(side (id ?id2) (type V1) (side ?s2) (color ?c2))
	(side (id ?id3) (type V1) (side ?s3) (color ?c3))
	(face ?s2 ?c1)
	=>
	(pll-pattern-out ?c1 ?c3 ?d ?f ?pv ?h)
)

(defrule pll-pattern-6
	(phase 4)
	(pll-hint ?d ?f&18|19 ?pv ?h)
	(block (id ?id1) (layer 3) (type corner) (status ok))
	(side (id ?id1) (pos ?p1) (side U))	
	(side (id ?id2) (pos ?p2&:(= 3 (distance ?p2 ?p1))) (side U))
	(side (id ?id3) (pos ?p3&:(= 3 (distance ?p1 ?p3))) (side U))	
	(side (id ?id2) (type V1) (side ?s2) (color ?c2))
	(side (id ?id3) (type V1) (side ?s3) (color ?c3))
	(face ?s2 ?c1)
	=>
	(pll-pattern-out ?c1 ?c3 ?d ?f ?pv ?h)
)