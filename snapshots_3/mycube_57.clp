(defrule start-up =>
(assert (blk 1 -1 1 r w g))
(assert (blk 1 0 1 r - g))
(assert (blk -1 1 1 r g y))
(assert (blk 1 -1 0 r w -))
(assert (blk 1 0 0 r - -))
(assert (blk 0 1 -1 - y r))
(assert (blk 1 -1 -1 r w o))
(assert (blk 1 0 -1 r - o))
(assert (blk 1 1 -1 o r y))
(assert (blk 0 -1 1 - w g))
(assert (blk 0 0 1 - - g))
(assert (blk -1 1 0 g y -))
(assert (blk 0 -1 0 - w -))
(assert (blk 0 0 0 - - -))
(assert (blk 0 1 0 - y -))
(assert (blk 0 -1 -1 - w o))
(assert (blk 0 0 -1 - - o))
(assert (blk 1 1 0 o y -))
(assert (blk -1 -1 1 b w g))
(assert (blk -1 0 1 b - g))
(assert (blk -1 1 -1 b g y))
(assert (blk -1 -1 0 b w -))
(assert (blk -1 0 0 b - -))
(assert (blk 0 1 1 - y b))
(assert (blk -1 -1 -1 b w o))
(assert (blk -1 0 -1 b - o))
(assert (blk 1 1 1 o b y))

(assert (phase 0)))