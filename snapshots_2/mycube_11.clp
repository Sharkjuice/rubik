(defrule start-up =>
(assert (blk -1 -1 1 g w r))
(assert (blk 0 1 -1 - r g))
(assert (blk 1 1 1 y g r))
(assert (blk -1 -1 0 r w -))
(assert (blk -1 0 0 r - -))
(assert (blk 1 0 -1 y - r))
(assert (blk -1 1 -1 w o r))
(assert (blk -1 0 1 o - r))
(assert (blk -1 1 1 r y o))
(assert (blk 0 -1 -1 - w g))
(assert (blk 0 0 -1 - - g))
(assert (blk -1 1 0 g y -))
(assert (blk 0 -1 0 - w -))
(assert (blk 0 0 0 - - -))
(assert (blk 0 1 0 - y -))
(assert (blk 0 -1 1 - w o))
(assert (blk 0 0 1 - - o))
(assert (blk 1 1 0 o y -))
(assert (blk 1 -1 1 w b g))
(assert (blk 0 1 1 - b g))
(assert (blk 1 1 -1 b y g))
(assert (blk 1 -1 0 b w -))
(assert (blk 1 0 0 b - -))
(assert (blk -1 0 -1 y - b))
(assert (blk -1 -1 -1 o b w))
(assert (blk 1 0 1 o - b))
(assert (blk 1 -1 -1 y o b))

(assert (phase 0)))