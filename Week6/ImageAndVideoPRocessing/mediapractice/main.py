import cv2
import mediapipe as mp


# 1. Initialize MediaPipe Hands
def initialize_hands():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    return mp_hands, hands


# 2. Detect hands in a frame
def detect_hands(hands, frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return hands.process(rgb_frame)


# 3. Draw hand landmarks
def draw_landmarks(frame, results, mp_hands):
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )


# 4. Count detected hands
def count_hands(results):
    if results.multi_hand_landmarks:
        return len(results.multi_hand_landmarks)
    return 0


# 5. Main function
def main():
    mp_hands, hands = initialize_hands()

    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        results = detect_hands(hands, frame)
        draw_landmarks(frame, results, mp_hands)

        number_of_hands = count_hands(results)

        cv2.putText(
            frame,
            f"Hands: {number_of_hands}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow("MediaPipe Hand Practice", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    hands.close()


main()