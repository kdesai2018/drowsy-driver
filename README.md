# drowsy-driver
Eye detection system that determines whether a driver is sleeping or not, built for UT Makeathon 2019. Won 1st overall, Best in Workplace Safety


In drowsy.py, you'll find a single script that handles the entire pipeline. Basically, this code
1. Gets drivers face
2. Finds ear (euclidian distance) to tell if eyes are open or not
3. If eyes are closed, increments global timer. If eyes open, it resets the timer and returns to 1
4. If timer hits certain threshold, play wakeup_loop.mp3 repeatedly until user opens eyes. 
5. Once user wakes up, use Google Maps API to navigate user to nearest rest stop.

The entire project is hooked up to an Arduino. The arduino controls blinking LEDs on a wooden steering wheel and checks if the driver is gripping the wheel with both hands. 

Dependencies: VLC player, face-recognition, google-maps
