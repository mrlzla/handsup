import os
import time
import json
import uuid
import queue

import cv2
import numpy as np

from .pose_estimation import PoseEstimation
from .handsup_classification import HandsupClassification

class Alg:
    def __init__(self, opts, size, queue):
        self.queue = queue
        self.size = size
        self.pose_estimation = PoseEstimation(opts)
        self.pose_estimation.init_detector(size)

        self.handsup_classification = HandsupClassification()

        self.logdir = os.path.join(opts.logdir, uuid.uuid4().hex)
        os.makedirs(opts.logdir, exist_ok=True)
        os.makedirs(self.logdir)

        self.pose_log = os.path.join(self.logdir, 'pe.txt')
        self.execute()
    
    def fix_rect(self, coords):
        x1 = int(max(min(coords[0], self.size[0] - 1), 0))
        y1 = int(max(min(coords[1], self.size[1] - 1), 0))
        x2 = int(max(min(coords[2], self.size[0] - 1), 0))
        y2 = int(max(min(coords[3], self.size[1] - 1), 0))
        return [x1, y1, x2, y2]
    
    def write_logs(self, pose_data, labels):
        with open(self.pose_log, "a") as f:
            f.write(json.dumps(pose_data['results']) + '\n\n')
        
        result_poses = pose_data['results']
        result_frame = pose_data["multi_pose"]
        
        for index, label in enumerate(labels):
            if label == 1:
                x1, y1, x2, y2 = self.fix_rect(result_poses[index][:4])
                res_rect = result_frame[y1:y2, x1:x2]
                cv2.imwrite(os.path.join(self.logdir, f"{int(time.time())}_{index}.jpg"), res_rect)
    
    def process(self, frame):
        pose_data = self.pose_estimation.process(frame)
        labels = self.handsup_classification.process(pose_data['results'])
        self.write_logs(pose_data, labels)
    
    def execute(self):
        while True:
            try:
                frame = self.queue.get()
                self.process(frame)
            except queue.Empty:
                pass

            self.queue.task_done()