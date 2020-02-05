git clone https://github.com/pjreddie/darknet.git
cd darknet && make
cd ..
./darknet/darknet detector train custom_data/detector.data custom_data/cfg/yolov3.cfg custom_data/weights/darknet53.conv.74 > train.log