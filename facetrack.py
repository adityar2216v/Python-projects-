import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime


class FaceTracker:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

        # State tracking
        self.study_time = 0
        self.distracted_time = 0
        self.recovery_time = 0
        self.last_state = None
        self.state_start_time = datetime.now()

    def analyze_face_position(self, frame):
        height, width = frame.shape[:2]
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)

        if not results.multi_face_landmarks:
            return frame, "absent"

        face_landmarks = results.multi_face_landmarks[0]

        # Get nose and face points for orientation
        nose_tip = face_landmarks.landmark[4]
        left_eye = face_landmarks.landmark[33]
        right_eye = face_landmarks.landmark[263]

        # Calculate face orientation
        nose_x = nose_tip.x * width
        nose_y = nose_tip.y * height
        left_x = left_eye.x * width
        right_x = right_eye.x * width

        # Draw face mesh
        self.mp_drawing.draw_landmarks(
            frame,
            face_landmarks,
            self.mp_face_mesh.FACEMESH_CONTOURS,
            self.drawing_spec,
            self.drawing_spec
        )

        # Analyze face position
        face_center_x = (left_x + right_x) / 2
        horizontal_deviation = abs(face_center_x - width / 2) / (width / 2)
        vertical_deviation = abs(nose_y - height / 2) / (height / 2)

        # Determine study state
        if horizontal_deviation < 0.15 and vertical_deviation < 0.2:
            state = "studying"
            color = (0, 255, 0)  # Green
        else:
            state = "distracted"
            color = (0, 0, 255)  # Red

        # Draw status indicator
        cv2.putText(frame, f"State: {state}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        self.update_times(state)
        return frame, state

    def update_times(self, current_state):
        current_time = datetime.now()
        time_diff = (current_time - self.state_start_time).total_seconds()

        if self.last_state != current_state:
            if current_state == "studying":
                self.study_time += time_diff
            elif current_state == "distracted":
                self.distracted_time += time_diff
                self.recovery_time = self.distracted_time
            else:  # absent
                self.distracted_time += time_diff
                self.recovery_time = self.distracted_time

            self.state_start_time = current_time
            self.last_state = current_state

    def get_times(self):
        return {
            "study_time": int(self.study_time),
            "distracted_time": int(self.distracted_time),
            "recovery_time": int(self.recovery_time)
        }

    def release(self):
        self.face_mesh.close()


def main():
    cap = cv2.VideoCapture(0)
    tracker = FaceTracker()

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        frame, state = tracker.analyze_face_position(frame)
        times = tracker.get_times()

        # Display times
        cv2.putText(frame, f"Study Time: {times['study_time']}s", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Wasted Time: {times['distracted_time']}s", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Recovery Time: {times['recovery_time']}s", (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow('Face Tracking', frame)
        if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
            break

    cap.release()
    tracker.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()