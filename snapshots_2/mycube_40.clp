(defrule start-up =>
(assert (blk -1 1 -1 w r g))
(assert (blk 0 1 1 - g r))
(assert (blk 1 1 1 g r y))
(assert (blk 0 -1 -1 - w r))
(assert (blk 0 0 -1 - - r))
(assert (blk -1 0 1 r - y))
(assert (blk 1 -1 -1 w o r))
(assert (blk -1 1 0 o r -))
(assert (blk 1 -1 1 r y o))
(assert (blk 1 -1 0 g w -))
(assert (blk 1 0 0 g - -))
(assert (blk 1 0 1 g - y))
(assert (blk 0 -1 0 - w -))
(assert (blk 0 0 0 - - -))
(assert (blk 0 1 0 - y -))
(assert (blk -1 -1 0 o w -))
(assert (blk -1 0 0 o - -))
(assert (blk -1 0 -1 y - o))
(assert (blk -1 1 1 w b g))
(assert (blk 1 0 -1 g - b))
(assert (blk 1 1 -1 g b y))
(assert (blk 0 -1 1 - w b))
(assert (blk 0 0 1 - - b))
(assert (blk 1 1 0 b y -))
(assert (blk -1 -1 1 b o w))
(assert (blk 0 1 -1 - b o))
(assert (blk -1 -1 -1 o y b))

(assert (phase 0)))