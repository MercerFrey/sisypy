import carla

from .controller import PurePursuitController


class Hero(object):
    def __init__(self, location, rotation, waypoints, target_speed_km, actor_role):
        self.world = None
        self.actor = None
        self.control = None
        self.controller = None
        self.location = location
        self.rotation = rotation
        self.waypoints = waypoints
        self.target_speed = target_speed_km / 3.6  # km/h to m/s
        self.actor_role = actor_role
        self.tick_count = 0

        #RSS
        self.vehicle_physics = None
        self.restrictor = carla.RssRestrictor()

    def start(self, world):
        self.world = world
        spawn_point = carla.Transform(
            self.location, self.rotation
        )
        self.actor = self.world.spawn_hero("vehicle.audi.tt", spawn_point, role_name = self.actor_role)

        self.controller = PurePursuitController()
        
        self.vehicle_physics = self.world.hero_actor.get_physics_control()
        
        self.world.register_actor_waypoints_to_draw(self.actor, self.waypoints)
        #self.actor.set_autopilot(True, world.args.tm_port)

    def tick(self, clock):
        vehicle_control = carla.VehicleControl()
        throttle, steer = self.controller.get_control(
            self.actor,
            self.waypoints,
            self.target_speed,
            self.world.fixed_delta_seconds,
        )
        vehicle_control.throttle = throttle
        vehicle_control.steer = steer
        
        print("helloo")
        print(self.restrictor)
        if self.restrictor:
            rss_proper_response = self.world.rss_sensor.proper_response if self.world.rss_sensor and self.world.rss_sensor.response_valid else None
            print(rss_proper_response)
        if rss_proper_response:
            vehicle_control = self.restrictor.restrict_vehicle_control(vehicle_control, rss_proper_response, self.world.rss_sensor.ego_dynamics_on_route, self.vehicle_physics)

  

        self.actor.apply_control(vehicle_control)


    def destroy(self):
        """Destroy the hero actor when class instance is destroyed"""
        if self.actor is not None:
            self.actor.destroy()

