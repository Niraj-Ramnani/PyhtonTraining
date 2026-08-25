import av

container = av.open("video.mp4")
for frame in container.decode(video=0):
    image = frame.to_image()
    image.save("frame.jpg")
    break

for frame in container.decode(video=0):
    image_array = frame.to_ndarray()
    print(image_array.shape)
    break

# container.close()