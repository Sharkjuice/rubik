(defrule start-up =>
(assert (blk 1 -1 -1 g w r))
(assert (blk 1 0 -1 g - r))
(assert (blk -1 -1 -1 g y r))
(assert (blk 0 -1 -1 - w r))
(assert (blk 0 0 -1 - - r))
(assert (blk 0 1 1 - y r))
(assert (blk -1 1 1 o w r))
(assert (blk -1 1 0 r o -))
(assert (blk -1 -1 1 y r o))
(assert (blk 1 -1 0 g w -))
(assert (blk 1 0 0 g - -))
(assert (blk -1 0 1 y - g))
(assert (blk 0 -1 0 - w -))
(assert (blk 0 0 0 - - -))
(assert (blk 0 1 0 - y -))
(assert (blk -1 -1 0 o w -))
(assert (blk -1 0 0 o - -))
(assert (blk -1 0 -1 y - o))
(assert (blk 1 -1 1 g w b))
(assert (blk 1 0 1 g - b))
(assert (blk 1 1 -1 y g b))
(assert (blk 0 -1 1 - w b))
(assert (blk 0 0 1 - - b))
(assert (blk 0 1 -1 - y b))
(assert (blk 1 1 1 b o w))
(assert (blk 1 1 0 b o -))
(assert (blk -1 1 -1 y o b))

(assert (phase 0)))