(defrule start-up =>
(assert (blk 1 -1 1 w g r))
(assert (blk 1 1 0 g r -))
(assert (blk -1 1 -1 g r y))
(assert (blk 1 -1 0 r w -))
(assert (blk 1 0 0 r - -))
(assert (blk 0 1 1 - y r))
(assert (blk 1 -1 -1 o r w))
(assert (blk 1 0 1 o - r))
(assert (blk -1 1 1 y o r))
(assert (blk 0 -1 1 - w g))
(assert (blk 0 0 1 - - g))
(assert (blk -1 1 0 g y -))
(assert (blk 0 -1 0 - w -))
(assert (blk 0 0 0 - - -))
(assert (blk 0 1 0 - y -))
(assert (blk 0 -1 -1 - w o))
(assert (blk 0 0 -1 - - o))
(assert (blk 1 0 -1 y - o))
(assert (blk 1 1 1 w g b))
(assert (blk -1 0 1 b - g))
(assert (blk 1 1 -1 b y g))
(assert (blk -1 -1 0 b w -))
(assert (blk -1 0 0 b - -))
(assert (blk 0 1 -1 - y b))
(assert (blk -1 -1 -1 o b w))
(assert (blk -1 0 -1 o - b))
(assert (blk -1 -1 1 o b y))

(assert (phase 0)))