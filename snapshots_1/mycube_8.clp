(defrule start-up =>
(assert (blk 1 -1 1 w g r))
(assert (blk 0 -1 -1 - g r))
(assert (blk -1 -1 -1 r g y))
(assert (blk 0 1 -1 - r w))
(assert (blk -1 0 0 r - -))
(assert (blk -1 0 1 y - r))
(assert (blk -1 1 1 w r o))
(assert (blk 1 0 -1 o - r))
(assert (blk -1 1 -1 o y r))
(assert (blk -1 0 -1 g - w))
(assert (blk 0 0 -1 - - g))
(assert (blk 1 0 1 g - y))
(assert (blk 0 -1 0 - w -))
(assert (blk 0 0 0 - - -))
(assert (blk 0 1 0 - y -))
(assert (blk -1 -1 0 w o -))
(assert (blk 0 0 1 - - o))
(assert (blk 0 1 1 - y o))
(assert (blk 1 -1 -1 b w g))
(assert (blk 1 -1 0 g b -))
(assert (blk -1 -1 1 b g y))
(assert (blk -1 1 0 w b -))
(assert (blk 1 0 0 b - -))
(assert (blk 1 1 0 b y -))
(assert (blk 1 1 -1 o b w))
(assert (blk 0 -1 1 - o b))
(assert (blk 1 1 1 y o b))

(assert (phase 0)))