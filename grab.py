
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from PIL import Image
import time
from mss import mss


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

PORT = 31245

class PILHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Create an image using PIL
        image = grab_screen()
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Write response headers
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.send_header('Content-length', len(img_byte_arr))
        self.send_header('Access-Control-Allow-Origin', '*')  # This line enables CORS
        self.end_headers()

        # Write Image Data
        self.wfile.write(img_byte_arr)

def run(server_class=HTTPServer, handler_class=PILHandler, port=8000):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving at port {port}')
    httpd.serve_forever()
    
run(port=PORT)