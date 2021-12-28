import os
import time
import json
import queue

from .pose_estimation import PoseEstimation
from .handsup_classification import HandsupClassification

class Alg:
    def __init__(self, opts, size, queue):
        self.queue = queue
        self.pose_estimation = PoseEstimation(opts)
        self.pose_estimation.init_detector(size[0], size[1])

        self.handsup_classification = HandsupClassification()

        self.logdir = os.path.join(opts.logdir, str(time.time()))
        os.makedirs(opts.logdir, exist_ok=True)
        os.makedirs(self.logdir)

        self.pose_log = os.path.join(self.logdir, 'pe.txt')
        self.execute()
    
    def write_logs(self, result):
        with open(self.pose_log, "a") as f:
            f.write(json.dumps(result['results']))
    
    def process(self, frame):
        keypoints = self.pose_estimation.process(frame)
        label = self.handsup_classification.process(keypoints)
        self.write_logs(keypoints)
    
    def execute(self):
        while True:
            try:
                frame = self.queue.get()
                self.process(frame)
            except queue.Empty:
                pass

            self.queue.task_done()