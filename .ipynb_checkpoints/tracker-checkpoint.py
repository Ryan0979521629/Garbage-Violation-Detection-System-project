from deep_sort.deep_sort.tracker import Tracker as DeepSortTracker
from deep_sort.tools import generate_detections as gdet
from deep_sort.deep_sort import nn_matching
from deep_sort.deep_sort.detection import Detection
import numpy as np


class Tracker:
    tracker = None
    encoder = None
    tracks = None

    def __init__(self):
        max_cosine_distance = 0.8
        nn_budget = None

        encoder_model_filename = 'model_data/mars-small128.pb'

        metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
        self.tracker = DeepSortTracker(metric)
        self.encoder = gdet.create_box_encoder(encoder_model_filename, batch_size=1)

    def update(self, frame, detections,frame_count):

        if len(detections) == 0:
            self.tracker.predict()
            self.tracker.update([],frame,frame_count)  
            self.update_tracks()
            return
        bboxes = np.asarray([d[:-1] for d in detections])
        top = np.asarray([d[1] for d in detections])
        first_frame_central_x=np.asarray([(d[0] + d[2]) / 2 for d in detections])
        first_frame_central_y=np.asarray([(d[1] + d[3]) / 2 for d in detections])
        bboxes[:, 2:] = bboxes[:, 2:] - bboxes[:, 0:2]
        scores = [d[-2] for d in detections]

        features = self.encoder(frame, bboxes)

        dets = []
        for bbox_id, bbox in enumerate(bboxes):
            dets.append(Detection(bbox, scores[bbox_id], features[bbox_id],top[bbox_id],first_frame_central_x[bbox_id],first_frame_central_y[bbox_id]))

        self.tracker.predict()
        self.tracker.update(dets,frame,frame_count)
        self.update_tracks()

    def update_tracks(self):
        tracks = []
        for track in self.tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            bbox = track.to_tlbr()

            id = track.track_id
            first_frame=track.first_frame
            detect=track.is_moving_fast
            first_frame_central_x=track.first_frame_central_x
            first_frame_central_y=track.first_frame_central_y
            tracks.append(Track(id, bbox,first_frame,detect,first_frame_central_x,first_frame_central_y))

        self.tracks = tracks


class Track:
    track_id = None
    bbox = None
    first_frame=None
    detect=False
    first_frame_central_x=None
    first_frame_central_y=None
    def __init__(self, id, bbox,first_frame,detect,first_frame_central_x,first_frame_central_y):
        self.track_id = id
        self.bbox = bbox
        self.first_frame=first_frame
        self.detect=detect
        self.first_frame_central_x=first_frame_central_x
        self.first_frame_central_y=first_frame_central_y