from flask import Flask, render_template, Response
from picamera import PiCamera
import time

print("Coded by Alexander Usov - Deonik")
print("Copyright 2023 © Alexander Usov")

app = Flask(__name__)

# Erstellen Sie eine Instanz der Kamera
camera = PiCamera()


def generate_frames():
    while True:
        # Legen Sie die Auflösung und andere Kameraeinstellungen fest
        camera.resolution = (640, 480)
        camera.rotation = 180

        # Erstellen Sie einen Speicherpuffer für das Bild
        frame = bytearray()

        # Nehmen Sie ein Bild auf und speichern Sie es im Speicherpuffer
        camera.capture(frame, 'jpeg')

        # Geben Sie das Bild im MJPEG-Format zurück
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytes(frame) + b'\r\n\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
