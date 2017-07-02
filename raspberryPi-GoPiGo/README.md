
# Raspberry Pi : GoPiGo

<p align="center">
  <img src="/img/raspberry-pi-logo.png" height="150"/>
  <img src="/img/plus.png" height="80">
  <img src="/img/opencv-logo.png" height="150">
</p>


<br>


## Object Detection  
### Stop sign classifier
[  **OpenCV** Haar Cascade classifier via Picamera  ]

* GoPiGo can accurately recognize a `STOP` sign from various angles and distances.

<p align="center">
  <img src="/raspberryPi-GoPiGo/img/STOP-near.png" height="300">
  <img src="/raspberryPi-GoPiGo/img/STOP-far.png" height="300">
  <img src="/raspberryPi-GoPiGo/img/STOP-sideview.png" height="300">
</p>

<br>

#### _Interesting observation_

* GoPiGo tries to classify the `DO NOT ENTER` and `WRONG WAY` as a `STOP` sign.

>If one thinks about the separate traffic sign categories that exist today, this should not seem strange. Each group of signs share a common coloration and shape. The purpose behind this decision, of course, is to instill an intuition in us at a young age how to appropriately respond to traffic signs as we encounter them.

>In this case, the Haar Cascade classifier is "picking up" the commonality of colors in red and white lettering (i.e. feature) which is essentially communicating the same message to us, "Hey, STOP".   

<p align="center">
  <img src="/raspberryPi-GoPiGo/img/STOP-DoNotEnter.png" height="300">
  <img src="/raspberryPi-GoPiGo/img/DoNotEnter-WrongWay.png" height="300">
</p>
