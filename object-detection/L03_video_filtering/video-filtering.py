# video-filtering.py
# 11.2.2026

# run on ANACONDA_NEURAL_NETWORKS_ENV
import cv2
import numpy as np


def filter_image(img, type_of_kernel="gaussian_3x3"):
    # dictionary of different kernels/filters
    KERNELS = {
    # if numbers increase, becomes more white
    # if numbers decrease, goes darker
   "gaussian_3x3": (1/16) * np.array([
        [1,2,1],
        [2,4,2],
        [1,2,1],
    ], dtype=np.float32),

    "mean_5x5": (1/25) * np.array([
        [1,1,1,1,1],
        [1,1,1,1,1],
        [1,1,1,1,1],
        [1,1,1,1,1],
        [1,1,1,1,1],
    ], dtype=np.float32),

    "sobel_3x3": (1/1) * np.array([
        [1,0,-1],
        [1,0,-2],
        [1,0,-1],
    ], dtype=np.float32),

    "insobel_3x3": (1/1) * np.array([
        [-1,0,1],
        [-2,0,2],
        [-1,0,1],
    ], dtype=np.float32),

    # the large number in middle strengthens the value of the pixel itself
    # while the small numbers around reduce the effect of neighbour pixels
    # combination of: 
    # mean_3x3: 1/9 * [[1,1,1],[1,1,1][1,1,1]]
    # gain_3x3: 2 * [[0,0,0][0,1,0][0,0,0]]
    "sharpen_3x3": np.array([
        [-0.111,-0.111,-0.111],
        [-0.111,1.888,-0.111],
        [-0.111,-0.111,-0.111]
    ]),

    #classic sharpen 3x3
    # very strong middle value with 5
    # neighbours negative, corners 0
    # makes edges emphasized
    "sharpen_classic_3x3": np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    }

    filtered_f32 = cv2.filter2D(img.astype(np.float32), ddepth=cv2.CV_32F, kernel=KERNELS[type_of_kernel])
    filtered_u8 = np.clip(filtered_f32, 0, 255).astype(np.uint8)
    return filtered_u8

def draw_text_top_left(img, text, margin = 10, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.5, thickness=1):
    out = img.copy()

    if out.ndim == 2:
        out = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)
    x = margin
    y = margin

    (t_width, t_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    org = (x, y + t_height)

    # black outline
    cv2.putText(out, text, org, font, font_scale, (0,0,0), thickness+2, cv2.LINE_AA)
    # text itself
    cv2.putText(out, text, org, font, font_scale, (255,255,255), thickness, cv2.LINE_AA)

    return out


def main():
    FILTER_NAMES = ["none", "gaussian_3x3", "mean_5x5", "sobel_3x3", "insobel_3x3", "sharpen_3x3", "sharpen_classic_3x3"]
    # variable for grey or color image
    use_color = True
    #use_filter = False
    filter_index = 0
    # read videocapture into cap variable
    cap = cv2.VideoCapture(0) # 0 = default camera

    # verify camera is open
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    # create a window with cv2
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    window_name = "Live video stream (press q to quit)"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    # during processing video
    while True:
        status_text = "COLOR "

        # frame is image arriving from camera
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not grab frame with cap.read()")
        

        # change to grey or colorful image
        imgShow = frame
        if not use_color:
            imgShow = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            status_text = "GRAYSCALE "

        # change filter mode
        if filter_index > 0:
            imgShow = filter_image(imgShow, FILTER_NAMES[filter_index])

        # write text
        imgShow = draw_text_top_left(imgShow, f'status: {status_text}\n filter: {FILTER_NAMES[filter_index]}')

        # if reading frame was success, show it inside the window
        cv2.imshow(window_name, imgShow)

        # simple key waiter so pressing q ends the while loop
        # waits for one millisecond for keyboard and then quits
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            break
        if key == ord('c') or key == ord('C'):
            use_color = not use_color
        if key == ord('f') or key == ord('F'):
            filter_index = (filter_index+1) % len(FILTER_NAMES)

    # after video has been processed
    cap.release()
    cv2.destroyAllWindows()

    # return
    return
    

# -----------------------------------------
if __name__ == "__main__":
    main()