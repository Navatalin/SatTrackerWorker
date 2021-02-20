from datetime import datetime, tzinfo
from skyfield.api import load
from skyfield.positionlib import Geocentric
import numpy as np
#from MQPublisher import MQPublisher
from mqpublish import MqPublish

class Tracking:
    def __init__(self) -> None:
        self.stations_url = 'https://celestrak.com/NORAD/elements/starlink.txt'
        self.satellites = load.tle_file(self.stations_url)
        self.rabbit_mq_url = 'amqp://Worker:workerPassword@localhost:5672/%2F?connection_attempts=3&heartbeat=3600'
 

    def get_pos(self, sat_names, mq):
        for sat in self.satellites:
            if(sat.name in sat_names):
                ts = load.timescale()
                gpo = sat.at(ts.now())
                velocity = gpo.velocity.km_per_s
                #position = [sat.name, gpo.position.km[0], gpo.position.km[1],gpo.position.km[2], velocity[0], velocity[1],velocity[2]]
                position = {
                    "name": sat.name,
                    "p_x": gpo.position.km[0],
                    "p_y": gpo.position.km[1],
                    "p_z": gpo.position.km[2],
                    "v_x": velocity[0],
                    "v_y": velocity[1],
                    "v_z": velocity[2]
                }

                if(np.isnan(gpo.position.km[0])):
                    position["p_x"] = 0.0
                    position["p_y"] = 0.0
                    position["p_z"] = 0.0
                    position["v_x"] = 0.0
                    position["v_y"] = 0.0
                    position["v_z"] = 0.0
                
                
                mq.publish_message(position)
        