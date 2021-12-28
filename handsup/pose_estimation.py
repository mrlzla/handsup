import sys

sys.path.append('CenterNet/src')
sys.path.append('CenterNet/src/lib')

from detectors.detector_factory import detector_factory
from opts import opts as pe_opts

import numpy as np

class PoseEstimation:
    def __init__(self, opts):
        self.opts = opts
        self.model_path = opts.pose_estimation_model_path
        self.task = opts.center_net_task
        self.detector_class = detector_factory[self.task]
        self.threshold = opts.pose_estimation_threshold

        pe_opt = pe_opts().init('{} --load_model {}'.format(self.task, self.model_path).split(' '))
        pe_opt.debug = 1

        self.detector = self.detector_class(pe_opt)
    
    def init_detector(self, size):
        self.detector.run(np.zeros(shape=(size[1], size[0], 3), dtype=np.uint8))

    def process(self, img):
        res = self.detector.run(img)
        if len(res['results']) > 0:
            res['results'] = [item for item in res['results'][1] if item[4] > self.threshold]
        return res