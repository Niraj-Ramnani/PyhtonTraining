**OpenCV (Open Source Computer Vision Library)** is a Python library mainly used for:

- Image processing
- Video processing
- Computer vision
- Object detection
- Face detection
- Image manipulation

```
pip install opencv-python
```

| Function | Purpose |
| --- | --- |
| `cv2.imread()` | Read image |
| `cv2.imshow()` | Display image |
| `cv2.resize()` | Resize image |
| `cv2.cvtColor()` | Convert colors |
| `cv2.imwrite()` | Save image |

**Pillow** is a Python library used mainly for **simple image manipulation and image processing**.

### Use cases

- Resize images
- Crop images
- Rotate images
- Add text
- Convert image formats

| Function | Purpose |
| --- | --- |
| `Image.open()` | Open image |
| `resize()` | Resize |
| `crop()` | Crop |
| `rotate()` | Rotate |
| `save()` | Save image |

OpenCV is designed as a **computer vision and machine learning tool**, while Pillow (PIL) is designed as a **general-purpose graphic and image editor**

**PyAV** is a Python library for working with **audio and video files**.

```
pip install av
```

video.mp4

│

├── Video Stream

│ └── Frames

│

├── Audio Stream

│ └── Audio data

│

└── Metadata

| Function/Feature | Purpose |
| --- | --- |
| `av.open()` | Open media |
| `container.decode()` | Decode streams into frames |
| `frame.to_image()` | Convert frame to Pillow image |
| `frame.to_ndarray()` | Convert frame to NumPy array |
| `container.close()` | Close media |

**VidGear** is a Python library that makes **video processing and video streaming easier**.

```
pip install vidgear
```

| Feature | Purpose |
| --- | --- |
| `CamGear` | Capture video |
| `read()` | Read frame |
| `stop()` | Stop stream |
| `VideoGear` | Flexible video capture |
| `WriteGear` | Write/save video |

**MediaPipe** is a framework/library for building applications involving **AI-powered perception**, especially:

- Face detection
- Hand tracking
- Pose detection
- Face landmarks
- Gesture recognition