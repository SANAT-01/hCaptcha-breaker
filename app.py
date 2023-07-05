import streamlit as st
import numpy as np
import random 
import pickle
import cv2

def format_images(images):
    height = 128
    rgb = np.ones((height*3, height*3, 3))
    bgr = np.ones((height*3, height*3, 3))
    r = []
    lst = []
    for i in range(3):
        for j in range(3):
            rnd = random.randint(0,len(test))
            r.append(rnd)
            rgb[(height*i):(height*(i+1)), height*j:height*(j+1), : ] = cv2.cvtColor(images[rnd], cv2.COLOR_BGR2RGB)
            bgr[(height*i):(height*(i+1)), height*j:height*(j+1), : ] = images[rnd]
            lst.append(images[rnd])
    lst = np.array(lst)
    return bgr, rgb, lst

def return_pos(images_lst, category):
    if images_lst.shape[0] == 0:
        return []
    pred = np.round(Model.predict(images_lst), 2)
    out = []
    for i in pred:
        maxi = np.max(i)
        x = list(np.where(i==maxi))[0][0]
        out.append(x)
    # print(out)
    ans = []
    for id in range(9):
        if cat[out[id]]==category:
            x = id//3
            y = id%3
            ans.append((x,y))
    return ans

def put_box(img, pos):
    width = 128
    height = 128
    img2 = img.copy()
    for x,y in pos:
        startx = y*width
        starty = x*height
        cv2.rectangle(img2, (startx, starty), (startx + width, starty + height), (0.2,0.9,0.01), 4)
    return img2

npzfile = np.load('Preprocessed_test_images.npz')
test, label_test = npzfile['arr_0'], npzfile['arr_1']
pickle_in = open("Best_model.pkl", "rb")  ## rb = READ BYTE
Model = pickle.load(pickle_in)
file = open('Categories.txt')
cat = [x.strip() for x in file.readline()[1:-1].replace("'", "").split(",")]

def main():
    st.header('hCaptcha Breaker !!')
    st.write("hcaptcha were invented to prevent bots from attacking websites. But the ML models \
             are breaking captchas. Thus, stronger captchas are being invented. In this project, we have trained a ML model to break hcaptcha.")
    st.write('Welcome to the hCaptcha breaker system, Where user can randomly select any 9 images \
             and our trained model will try to identify the categories you selected.')
    if 'rgb' not in st.session_state:
        st.session_state.rgb = np.ones((384, 384, 3))
    if 'img_lst' not in st.session_state:
        st.session_state.img_lst = np.array([])
    if 'show_rnd_img' not in st.session_state:
        st.session_state.show_rnd_img = False

    rnd_btn = st.button("Randomize Images")
    if rnd_btn:
        st.session_state.show_rnd_img = rnd_btn
        gr, st.session_state.rgb, st.session_state.img_lst = format_images(test)
        st.image(st.session_state.rgb, caption='Image Caption', use_column_width=False)
    elif st.session_state.show_rnd_img:
        st.image(st.session_state.rgb, caption='Image Caption', use_column_width=False)

    cat_btn = st.selectbox("Select Category", cat).strip()
    sub_btn = st.button("Submit")
    # print(st.session_state.img_lst.shape)
    if sub_btn:
        if not st.session_state.show_rnd_img:
            st.warning('Warning !!')
            st.warning("First select any random images by the clicking the \
                       random image generator button")
            # print('Warning')
        pos = return_pos(st.session_state.img_lst, cat_btn)
        # print(pos)
        marked_image = put_box(st.session_state.rgb, pos)
        st.image(marked_image, caption='Image Caption', use_column_width=False)

if __name__ == '__main__':
    main()