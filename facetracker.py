import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime
import winsound
import threading


class FaceTracker:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        # Updated parameters for better performance and stability
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )
        # Distraction alert settings
        self.distraction_threshold = 3  # seconds before alert
        self.last_distraction_alert = datetime.now()
        self.alert_active = False
        self.alert_thread = None
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
        self.connection_spec = self.mp_drawing.DrawingSpec(thickness=1, color=(255, 0, 0))

        # State tracking
        self.study_time = 0
        self.distracted_time = 0
        self.recovery_time = 0
        self.last_state = None
        self.state_start_time = datetime.now()

    def analyze_face_position(self, frame):
        if frame is None:
            return frame, "error"

        try:
            height, width = frame.shape[:2]
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(frame_rgb)

            if not results.multi_face_landmarks:
                cv2.putText(frame, "No face detected", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                return frame, "absent"

            face_landmarks = results.multi_face_landmarks[0]

            # Get nose and eye points for orientation
            nose_tip = face_landmarks.landmark[4]
            left_eye = face_landmarks.landmark[33]
            right_eye = face_landmarks.landmark[263]

            # Calculate face orientation
            nose_x = nose_tip.x * width
            nose_y = nose_tip.y * height
            left_x = left_eye.x * width
            right_x = right_eye.x * width

            # Draw face mesh with improved visibility
            self.mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=self.drawing_spec,
                connection_drawing_spec=self.connection_spec
            )

            # Analyze face position with adjusted thresholds
            face_center_x = (left_x + right_x) / 2
            horizontal_deviation = abs(face_center_x - width / 2) / (width / 2)
            vertical_deviation = abs(nose_y - height / 2) / (height / 2)

            # Determine study state with more lenient thresholds
            if horizontal_deviation < 0.2 and vertical_deviation < 0.25:
                state = "studying"
                color = (0, 255, 0)  # Green
                self.alert_active = False
            else:
                state = "distracted"
                color = (0, 0, 255)  # Red
                self.check_distraction_alert()

            # Draw status with improved visibility
            cv2.putText(frame, f"State: {state}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            self.update_times(state)
            return frame, state

        except Exception as e:
            print(f"Error in face analysis: {str(e)}")
            return frame, "error"

    def update_times(self, current_state):
        current_time = datetime.now()
        time_diff = (current_time - self.state_start_time).total_seconds()

        if self.last_state == "studying":
            self.study_time += time_diff
        elif self.last_state == "distracted":
            self.distracted_time += time_diff
            self.recovery_time = self.distracted_time
        elif self.last_state in ["absent", "error"]:
            self.distracted_time += time_diff
            self.recovery_time = self.distracted_time

        self.state_start_time = current_time
        self.last_state = current_state

    def check_distraction_alert(self):
        current_time = datetime.now()
        if not self.alert_active and (current_time - self.last_distraction_alert).total_seconds() >= self.distraction_threshold:
            self.alert_active = True
            self.last_distraction_alert = current_time
            if self.alert_thread is None or not self.alert_thread.is_alive():
                self.alert_thread = threading.Thread(target=self.play_alert)
                self.alert_thread.start()

    def play_alert(self, current_state=None):
        # Play a beep sound
        winsound.Beep(1000, 500)  # 1000Hz for 500ms
        # Visual alert will be shown in the frame automatically

        # Time update logic moved to update_times.
        # self.state_start_time and self.last_state are updated in update_times.

    def get_times(self):
        return {
            "study_time": int(self.study_time),
            "distracted_time": int(self.distracted_time),
            "recovery_time": int(self.recovery_time)
        }

    def release(self):
        self.face_mesh.close()


def main():
    # Initialize video capture with error handling
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video capture device")
        return

    tracker = FaceTracker()

    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Error: Failed to read frame")
                break

            frame, state = tracker.analyze_face_position(frame)
            times = tracker.get_times()

            # Display times with improved formatting
            cv2.putText(frame, f"Study Time: {times['study_time']}s", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Distracted Time: {times['distracted_time']}s", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Recovery Time: {times['recovery_time']}s", (10, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow('Face Tracking', frame)
            if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
                break

    except Exception as e:
        print(f"Error in main loop: {str(e)}")

    finally:
        cap.release()
        tracker.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()