#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demonstrates how to compute fft of videos and the compute auto correlation
function with the out-of-memory version of the multitau algorithm.
"""

from cddm.viewer import MultitauViewer
from cddm.video import multiply, normalize_video, crop
from cddm.window import blackman
from cddm.fft import rfft2, normalize_fft
from cddm.multitau import iccorr_multi, normalize_multi, log_merge
from cddm.sim import simple_brownian_video, create_random_times1

#random time according to Eq.7 from the SoftMatter paper
t1, t2 = create_random_times1(1024,n = 16)

#: this creates a brownian motion multi-frame iterator. 
#: each element of the iterator is a tuple holding a single numpy array (frame,)
video = simple_brownian_video(t1,t2, shape = (256+32,256+32))

#: crop video to selected region of interest 
video = crop(video, roi = ((0,256), slice(0,256)))

#: create window for multiplication...
window = blackman((256,256))

#: we must create a video of windows for multiplication
window_video = ((window,window),)*1024

#:perform the actual multiplication
video = multiply(video, window_video)

#: if the intesity of light source flickers you can normalize each frame to the intensity of the frame
#video = normalize_video(video)

#: perform rfft2 and crop results, to take only first kimax and first kjmax wavenumbers.
fft = rfft2(video, kimax =37, kjmax = 37)

#: you can also normalize each frame with respect to the [0,0] component of the fft
#: this it therefore equivalent to  normalize_video
#fft = normalize_fft(fft)

#: now perform auto correlation calculation with default parameters using iterative algorithm
data, bg, var = iccorr_multi(fft, t1, t2, period = 32)

#: inspect the data
viewer = MultitauViewer(scale = True)
viewer.set_data(data, bg, var)
viewer.set_mask(k = 25, angle = 0, sector = 30)
viewer.plot()
viewer.show()

##perform normalization and merge data
#fast, slow = normalize_multi(data, bg, var,  scale = True)
#x,y = log_merge(fast, slow)
#
##: save the normalized data to numpy files
#import numpy as np
#np.save("cross_correlat_multi_live_t.npy",x)
#np.save("cross_correlat_multi_live_data.npy",y)

