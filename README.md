# python-mqtt-nvr
A python program to handle recording video feeds from IP cameras that integrates with MQTT for easy automation (Home Assistant for example)

## Usage

 1. Edit `example_config.py` to suit your needs 
	 1. an arbitrary number of cameras can be added
	 2. each camera entry should have a corresponding `outfile` definition
	 3. you should only edit the word immediately before and after the `//` for each outfile definition
 2. Rename `example_config.py` to `config.py`
 3. Create as many folders as cameras in `config.py` where the folder name is the part immediately before the `//` in each outfile definition
 4. Install the requirements using `pip install -r requirements.txt`
 5. Install ffmpeg
 5. Run the script using `python camera.py`
 6. Start recording by sending the payload `record` to the mqtt topic `cameras/nvr/record` and `stop` to the same topic to stop
 
 ## Home Assistant Usage
 In the `configuration.yaml` file for Home Assistant, add a new platform (assuming your mqtt broker is already set up correctly for Home Assistant) as below:
 

     - platform: mqtt
       name: "camera-record"
       state_topic: "cameras/nvr"
       command_topic: "cameras/nvr/record"
       payload_on: "record"
       payload_off: "stop"
       retain: true

This will add a new toggleable switch which you can use to start and stop recording.
