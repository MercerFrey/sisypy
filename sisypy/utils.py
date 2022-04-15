import math
import json


## utils.py name can be changed 

def ttc(this_actor, other_actor):
    
    # TODO needs this statement needs a check 
    if other_actor is None:
        return math.inf

    ### if the second car is moving 
    
    distance = this_actor.get_location().distance(other_actor.get_location())
    
    speed_difference = (calculate_speed(this_actor.get_velocity()) 
                        - calculate_speed(other_actor.get_velocity())
                        )
    try :
        return abs(distance / speed_difference)
    except ZeroDivisionError:
        return math.inf


def calculate_speed(vehicle_velocity):
    return math.sqrt(vehicle_velocity.x**2 + vehicle_velocity.y**2 + vehicle_velocity.z**2)

def snapshot_printer(filename, world):
    with open(filename, 'a') as f:
        world_snapshot = world.get_snapshot()
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
