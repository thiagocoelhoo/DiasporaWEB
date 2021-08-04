"""
import asyncio

import cv2

camera = cv2.VideoCapture(0)


async def gen_frames():
    while True:
        _, frame = camera.read()
        
        if frame is None:
            continue
            
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        response = b'--frame\r\nContent-Type:' + frame + b'\r\n'
        yield response


async def main():
    async for frame in  gen_frames():
        print(frame)

asyncio.run(main())
"""

from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)  # use 0 for web camera


def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)



"""
import asyncio
import cv2
from aiohttp import web, MultipartWriter


async def mjpeg_handler(request):
    boundary = "boundarydonotcross"
    response = web.StreamResponse(status=200, reason='OK', headers={
        'Content-Type': 'multipart/x-mixed-replace; '
                        'boundary=--%s' % boundary,
    })
    await response.prepare(request)
    wc = cv2.VideoCapture(0)
    encode_param = (int(cv2.IMWRITE_JPEG_QUALITY), 90)

    while True:
        _, frame = wc.read()
        if frame is None:
            continue
        with MultipartWriter('image/jpeg', boundary=boundary) as mpwriter:
            result, encimg = cv2.imencode('.jpg', frame, encode_param)
            data = encimg.tostring()
            mpwriter.append(data, {
                'Content-Type': 'image/jpeg'
            })
            await mpwriter.write(response, close_boundary=False)
        await response.drain()
    wc.shutdown()
    return response


async def index(request):
    return web.Response(text='<img src="/image"/>', content_type='text/html')


async def start_server(loop, address, port):
    app = web.Application(loop=loop)
    app.router.add_route('GET', "/", index)
    app.router.add_route('GET', "/image", mjpeg_handler)
    return await loop.create_server(app.make_handler(), address, port)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server(loop, '0.0.0.0', 8888))
    print("Server ready!")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Shutting Down!")
        loop.close()
"""