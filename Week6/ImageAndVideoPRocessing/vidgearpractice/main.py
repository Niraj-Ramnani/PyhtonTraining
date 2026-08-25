import cv2
from vidgear.gears import CamGear, WriteGear


stream = CamGear(source=0).start()


writer = WriteGear(output="output.mp4")

while True:
    frame = stream.read()
    if frame is None:
        break

    
    writer.write(frame)

    
    cv2.imshow("Webcam Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


stream.stop()
writer.close()
cv2.destroyAllWindows()