from io import BytesIO
from PIL import Image
import time
from mss import mss
from flask import Flask, send_file
from flask_cors import CORS

port = 31245
app = Flask(__name__)
CORS(app)

def grab_screen():
    # Capture entire screen
    with mss() as sct:
        start_time = time.time()
        monitor = sct.monitors[3]
        sct_img = sct.grab(monitor)
        time_elapsed = time.time() - start_time
        print(f"Time Elapsed: {time_elapsed:.2f}s")
        # Convert to PIL/Pillow Image
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

@app.route('/', methods=['GET'])
def grab_endpoint():
    try:
        # Create an image using PIL
        image = grab_screen()
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        return send_file(BytesIO(img_byte_arr), mimetype='image/png')
    except Exception as e:
        print(f'Error: {e}')
        return 'Error: ' + str(e), 500

if __name__ == '__main__':
    app.run(port=port, debug=False, host='0.0.0.0')