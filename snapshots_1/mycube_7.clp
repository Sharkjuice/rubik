(defrule start-up =>
(assert (blk 1 1 -1 g r w))
(assert (blk 1 -1 0 r g -))
(assert (blk -1 1 1 y r g))
(assert (blk 1 0 -1 w - r))
(assert (blk 0 0 -1 - - r))
(assert (blk 0 1 1 - y r))
(assert (blk -1 -1 1 w o r))
(assert (blk 1 0 1 r - o))
(assert (blk 1 1 1 y r o))
(assert (blk -1 -1 0 g w -))
(assert (blk 1 0 0 g - -))
(assert (blk 0 1 -1 - y g))
(assert (blk 0 -1 0 - w -))
(assert (blk 0 0 0 - - -))
(assert (blk 0 1 0 - y -))
(assert (blk 1 1 0 o w -))
(assert (blk -1 0 0 o - -))
(assert (blk -1 0 -1 y - o))
(assert (blk -1 1 -1 b w g))
(assert (blk -1 1 0 b g -))
(assert (blk -1 -1 -1 b y g))
(assert (blk 0 -1 1 - w b))
(assert (blk 0 0 1 - - b))
(assert (blk -1 0 1 y - b))
(assert (blk 1 -1 -1 o w b))
(assert (blk 0 -1 -1 - b o))
(assert (blk 1 -1 1 b o y))

(assert (phase 0)))