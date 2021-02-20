from skyfield.api import load
import numpy as np
import redis
import json
class Tracking:
    def __init__(self) -> None:
        self.stations_url = 'https://celestrak.com/NORAD/elements/starlink.txt'
        self.satellites = load.tle_file(self.stations_url)
        self.redis_host = redis.Redis(host='localhost',port=6379,db=0)
 

    def get_pos(self, sat_names):
        for sat in self.satellites:
            if(sat.name in sat_names):
                ts = load.timescale()
                gpo = sat.at(ts.now())
                velocity = gpo.velocity.km_per_s
                position = {
                    "name": sat.name,
                    "p_x": round(gpo.position.km[0],4),
                    "p_y": round(gpo.position.km[1],4),
                    "p_z": round(gpo.position.km[2],4),
                    "v_x": round(velocity[0],4),
                    "v_y": round(velocity[1],4),
                    "v_z": round(velocity[2],4)
                }

                if(np.isnan(gpo.position.km[0])):
                    position["p_x"] = 0.0
                    position["p_y"] = 0.0
                    position["p_z"] = 0.0
                    position["v_x"] = 0.0
                    position["v_y"] = 0.0
                    position["v_z"] = 0.0

                self.redis_host.set(sat.name,json.dumps(position))
                
        