
""" name_port_gpio.py
 
    This is a demo python file showing how to take paramaters
    from command line for device name, port, and GPIO.
    All credit goes to https://github.com/toddmedema/echo/
    for making the first working versions of this code.
"""
 
import fauxmo
import logging
import time
import sys
import RPi.GPIO as GPIO ## Import GPIO library
import time
 
from debounce_handler import debounce_handler
 
logging.basicConfig(level=logging.DEBUG)
 
control_pins = [33, 35, 37,31]
elapsed_time = [0.0]*3
state_pins = [False, False, False]

class device_handler(debounce_handler):
	"""Publishes the on/off state requested,
	and the IP address of the Echo making the request.
	"""

	TRIGGERS = {"kitchen": 52000,"living room":51000,"office":53000, "Exit":54000}

	def act(self, client_address, state, name):

		print("State", state, "from client @", client_address)
		# GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
		# GPIO.setup(int(7), GPIO.OUT)   ## Setup GPIO Pin to OUTPUT
		# GPIO.output(int(7), state) ## State is true/false

		if name=="kitchen":
			self.control_gpio(control_pins[0],state)
			if (state_pins[0] == False) and (state == True):
				elapsed_time[0]= time.time()
			elif(state == False):
				self.control_gpio(31,False)
			state_pins[0] = state  
		
		elif name =="living room":
			self.control_gpio(control_pins[1],state)

		elif name =="office":
			self.control_gpio(control_pins[2],state)

		elif name =="Exit":
			for i in control_pins:
				self.control_gpio(i,False)
			quit()

		else:
			print("Device not found!")

		return True

	def control_gpio(self, gp_num, state):
		GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
		GPIO.setup(int(gp_num), GPIO.OUT)   ## Setup GPIO Pin to OUTPUT
		GPIO.output(int(gp_num), state) ## State is true/false
 
if __name__ == "__main__":
	# Startup the fauxmo server
	fauxmo.DEBUG = True
	p = fauxmo.poller()
	u = fauxmo.upnp_broadcast_responder()
	u.init_socket()
	p.add(u)
 
    # Register the device callback as a fauxmo handler
	d = device_handler()
	for i in control_pins:
		d.control_gpio(i,False)
	for trig, port in d.TRIGGERS.items():
		fauxmo.fauxmo(trig, u, p, None, port, d)
 
	# Loop and poll for incoming Echo requests
	logging.debug("Entering fauxmo polling loop")
	#flag = True
	while True:
		try:
			
			# Allow time for a ctrl-c to stop the process
			p.poll(100)
			time.sleep(0.05)
			if(state_pins[0] ==  True) and (time.time() - elapsed_time[0] > 5):
				d.control_gpio(31,True)
			#flag = not flag
		
		except Exception as e:
			logging.critical("Critical exception:"+ e.args  )
			break





