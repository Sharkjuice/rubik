(defrule start-up =>
(assert (blk 1 -1 -1 r g w))
(assert (blk 0 -1 1 - g r))
(assert (blk 1 -1 1 y r g))
(assert (blk -1 0 -1 r - w))
(assert (blk -1 0 0 r - -))
(assert (blk 0 -1 -1 - y r))
(assert (blk -1 1 1 o w r))
(assert (blk -1 -1 0 r o -))
(assert (blk 1 1 1 y r o))
(assert (blk 1 0 1 w - g))
(assert (blk 0 0 -1 - - g))
(assert (blk 0 1 -1 - y g))
(assert (blk 0 -1 0 - w -))
(assert (blk 0 0 0 - - -))
(assert (blk 0 1 0 - y -))
(assert (blk 0 1 1 - o w))
(assert (blk 0 0 1 - - o))
(assert (blk 1 1 0 o y -))
(assert (blk -1 1 -1 w g b))
(assert (blk -1 0 1 b - g))
(assert (blk 1 1 -1 g b y))
(assert (blk 1 0 -1 b - w))
(assert (blk 1 0 0 b - -))
(assert (blk -1 1 0 b y -))
(assert (blk -1 -1 1 w b o))
(assert (blk 1 -1 0 b o -))
(assert (blk -1 -1 -1 b o y))

(assert (phase 0)))