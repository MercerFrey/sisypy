from turtle import distance
import carla
import json

from controller import PurePursuitController


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

        tick_dict = {"scenario_1.json": 155,
                    "scenario_2.json": 80,
                    "scenario_3.json": 110,
                    "scenario_4.json": 100,
                     }

        other_vehicle_location = self.world.world.get_actor(self.actor.id + 1).get_location()

        if ((other_vehicle_location.x > 0 and other_vehicle_location.y <= 33.8)
            or (other_vehicle_location.x < -330 and other_vehicle_location.y < 75)):

            if self.tick_count < tick_dict[self.world.args.scenario]:
                self.tick_count += 1
                ctrl.throttle = throttle
                ctrl.steer = steer
            else:
                # brake
                ctrl.throttle = 0
                ctrl.steer = steer
                ctrl.brake = 1
        else:

            ctrl.throttle = throttle
            ctrl.steer = steer

        self.actor.apply_control(ctrl)
        self.snapshot_printer()


    def destroy(self):
        """Destroy the hero actor when class instance is destroyed"""
        if self.actor is not None:
            self.actor.destroy()

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

    def snapshot_printer(self):
        with open(self.log_filename, 'a') as f:
            world_snapshot = self.world.world.get_snapshot()
            #snapshot_dict = dict()
            snapshot_dict = {
                "id" : world_snapshot.id,
                "timestamp" : world_snapshot.timestamp.elapsed_seconds,
                "actors" : [actor_snapshot.id for actor_snapshot in world_snapshot]
            }
            #for actor_snapshot in world_snapshot: # Get the actor and the snapshot information
                #actual_actor = self.world.world.get_actor(actor_snapshot.id)
                # snapshot_dict[actor_snapshot.id] = {
                #     "name": actor_snapshot.id
                    # "transform" : {
                    #     "location" :  str(actor_snapshot.get_transform().location),
                    #     "rotation" :  str(actor_snapshot.get_transform().rotation),
                    #     },
                    # "velocity" : str(actor_snapshot.get_velocity()),
                    # "angular_velocity" : str(actor_snapshot.get_angular_velocity()),
                    # "acceleration" : str(actor_snapshot.get_acceleration())
             #   }
            json.dump(snapshot_dict, f)
            f.write("\n")