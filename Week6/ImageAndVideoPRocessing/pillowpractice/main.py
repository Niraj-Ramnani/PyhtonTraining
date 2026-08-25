from PIL import Image

image = Image.open("image.png")

resized = image.resize((500, 300))
resized.show()

cropped = image.crop((100, 100, 400, 400))
cropped.show()


rotated = image.rotate(90)
rotated.show()