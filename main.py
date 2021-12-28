import argparse
import os
import sys

from handsup.stream_processor import StreamProcessor

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--stream_list', required=True,
                             help='path to list of streams')
    parser.add_argument('--pose_estimation_model_path', default='models/multi_pose_dla_3x.pth',
                             help='path to pose estimation model')
    parser.add_argument('--center_net_task', default='multi_pose')
    parser.add_argument('--show_video', action='store_true')
    parser.add_argument('--logdir', default='log',
                             help='path to log dir')
    

    opt = parser.parse_args()

    with open(opt.stream_list) as f:
        stream_paths = [x for x in f.read().split("\n") if x.startswith("rtsp")]
    
    stream_processor = StreamProcessor(stream_paths, opt)

    stream_processor.run()
        

    
