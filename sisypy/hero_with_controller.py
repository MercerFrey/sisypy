import carla
import json

from controller import PurePursuitController
import utils

class Hero(object):
    def __init__(self, location, rotation, waypoints, target_speed):
        self.world = None
        self.actor = None
        self.control = None
        self.controller = None
        self.location = location
        self.rotation = rotation
        self.waypoints = waypoints
        self.target_speed = target_speed  # meters per second
        self.tick_count = 0
        self.log_filename = "log.txt"

    def start(self, world):
        self.world = world
        spawn_point = carla.Transform(
            self.location, self.rotation
        )
        self.actor = self.world.spawn_hero("vehicle.audi.tt", spawn_point)

        self.controller = PurePursuitController()

        self.world.register_actor_waypoints_to_draw(self.actor, self.waypoints)
        #self.actor.set_autopilot(True, world.args.tm_port)

    def tick(self, clock):
        ctrl = carla.VehicleControl()
        throttle, steer = self.controller.get_control(
        self.actor,
        self.waypoints,
        self.target_speed,
        self.world.fixed_delta_seconds,
        )

        ctrl.throttle = throttle
        ctrl.steer = steer

        self.actor.apply_control(ctrl)
        



    def destroy(self):
        """Destroy the hero actor when class instance is destroyed"""
        if self.actor is not None:
            self.actor.destroy()

# TODO this can be implemented in the utils.
    def location_printer(self, interval):
        self.tick_count += 1
        if self.tick_count == interval:
            print("""
                {{ 
                    "x": {x},
                    "y": {y},
                    "z": {z}
                }},""".format(x=self.actor.get_location().x, y=self.actor.get_location().y, z=self.actor.get_location().z))
            self.tick_count %= interval
