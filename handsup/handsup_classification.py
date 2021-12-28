class HandsupClassification:
    def __init__(self):
        self.right_shoulder_index = 2*5 + 1 # y coord
        self.left_shoulder_index = 2*6 + 1
        self.right_elbow_index = 2*7 + 1
        self.left_elbow_index = 2*8 + 1

    def process(self, data):
        res = []
        for item in data:
            bbox = item[:4]
            prob = item[4]
            keypoints = item[5:]

            c1 = keypoints[self.right_shoulder_index] > keypoints[self.right_elbow_index ]
            c2 = keypoints[self.left_shoulder_index] > keypoints[self.left_elbow_index ]
            c3 = keypoints[self.right_shoulder_index] > 1.0
            c4 = keypoints[self.left_shoulder_index] > 1.0
            c5 = keypoints[self.right_elbow_index] > 1.0
            c6 = keypoints[self.left_elbow_index] > 1.0

            if c1 and c2 and c3 and c4 and c5 and c6:
                res.append(1)
            else:
                res.append(0)
        return res

