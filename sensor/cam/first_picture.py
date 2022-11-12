import camera
try:
    camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
except Exception as e:
    camera.deinit()
    camera.init(0, format=camera.JPEG, fb_location=camera.PSRAM)
buf = camera.capture()
with open("first_picture1.jpg", 'wb') as f:
    f.write(buf)
camera.deinit()