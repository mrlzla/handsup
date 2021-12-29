# Handsup


Detect whether there is a person with hands up in the image. The input to the program are one or many RTSP streams.

## Installation

0. Update submodules. 

    ~~~
    git clone --recursive https://github.com/mrlzla/handsup
    cd %workdir
    ~~~
    

1. Create virtualenv:

    ~~~
    virtualenv -p python3.8 venv
    source venv/bin/activate
    ~~~

     
2. Install python requirements:

    ~~~
    pip install -r requirements.txt
    ~~~

3. Install DCNv2 and NMS:

    ~~~
    cd CenterNet/src/lib/models/networks/DCNv2/
    python setup.py build develop
    cd -

    cd CenterNet/src/lib/external
    make
    cd -
    ~~~


4. Change list.txt file to specify rtsp streams
    
    
5. Run program

    ~~~
    python main.py --stream_list list.txt --logdir log
    ~~~


Results should be in log foulder you specified. As the result there are logs of pose estimation result written in pe.txt and frames with person handsup.
