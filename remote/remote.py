from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import videoProcess

app = Flask(__name__, template_folder='templates')

# 设置用户名和密码
verify = {}
with open('users.txt') as file:
    for line in file:
        words = line.split(' ')
        verify[words[0]] = words[1]


def generate_frames():
    camera = cv2.VideoCapture(0)  # 0 for built-in webcam
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# 验证用户身份
def check_auth(username, password):
    return username in verify.keys() and password == verify[username]


# 身份验证失败
def unauthorized():
    return Response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return unauthorized()
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='0.0.0.0')

