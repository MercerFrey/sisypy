import argparse
import pygame
import carla
import json

from hud import InfoBar
#from .hero import Hero
from world import World
from input_control import InputControl
import hero_with_controller 
import other_with_controller

from color import *
import utils


def game_loop(args):
    """Initialized, Starts and runs all the needed modules for No Rendering Mode"""
    try:

        # Init Pygame
        pygame.init()
        display = pygame.display.set_mode(
            (args.width, args.height), pygame.HWSURFACE | pygame.DOUBLEBUF
        )

        # Place a title to game window
        pygame.display.set_caption(args.description)

        # Show loading screen
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        text_surface = font.render("Rendering map...", True, COLOR_WHITE)
        display.blit(
            text_surface,
            text_surface.get_rect(center=(args.width / 2, args.height / 2)),
        )
        pygame.display.flip()

        # Init
        hud = InfoBar(args.width, args.height)
        input_control = InputControl()
        world = World(args)

        actors = scenario_reader(args.scenario)
        # For each module, assign other modules that are going to be used inside that module
        hud.start(world)
        input_control.start(hud, world)
        world.start(input_control)

        for actor in actors:
            actor.start(world) 

        # Game loop
        clock = pygame.time.Clock()
        while True:
            clock.tick_busy_loop(500)

            # Tick all modules
            world.tick(clock)
            for actor in actors:
                actor.tick(clock)
        
            hud.tick(clock)
            input_control.tick(clock)

            # Render all modules
            display.fill(COLOR_ALUMINIUM_4)
            world.render(display)
            hud.render(display)
            input_control.render(display)

            pygame.display.flip()

            # if logfile specified prints logs to the file
            if args.logfile:
                utils.snapshot_printer(args.logfile, world.world)
                

    except KeyboardInterrupt:
        print("\nCancelled by user. Bye!")

    finally:
         for actor in actors:
            if actor is not None:
                actor.destroy()



def scenario_reader(scenario_file):
    with open(scenario_file, 'r') as f:
        scenario = json.load(f)
    actors = []
    for actor_name, attributes in scenario.items():
        actor_spawn_point_location = carla.Location(**attributes["spawn_point"]["location"])
        actor_spawn_point_rotation = carla.Rotation(**attributes["spawn_point"]["rotation"])
        
        actor_controller = attributes["controller"]
        actor_waypoints = [carla.Location(**point) for point in actor_controller["waypoints"]]
        actor_target_speed = actor_controller["target_speed"]["value"]

        
        actor = None

        if actor_controller["type"] == "hero_with_controller":
            actor = hero_with_controller.Hero(
                location = actor_spawn_point_location,
                rotation = actor_spawn_point_rotation,
                waypoints = actor_waypoints,
                target_speed_km = actor_target_speed
            )
        elif actor_controller["type"] == "other_with_controller":
            actor = other_with_controller.Other(
                location = actor_spawn_point_location,
                rotation = actor_spawn_point_rotation,
                waypoints = actor_waypoints,
                target_speed_km = actor_target_speed
            )
        actors.append(actor)

    return actors

def main():
    """Parses the arguments received from commandline and runs the game loop"""

    # Define arguments that will be received and parsed
    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        "--host",
        metavar="H",
        default="127.0.0.1",
        help="IP of the host server (default: 127.0.0.1)",
    )
    argparser.add_argument(
        "-p",
        "--port",
        metavar="P",
        default=2000,
        type=int,
        help="TCP port to listen to (default: 2000)",
    )
    argparser.add_argument(
        "--tm-port",
        metavar="P",
        default=8000,
        type=int,
        help="Port to communicate with TM (default: 8000)",
    )
    argparser.add_argument(
        "--timeout",
        metavar="X",
        default=2.0,
        type=float,
        help="Timeout duration (default: 2.0s)",
    )
    argparser.add_argument(
        "--res",
        metavar="WIDTHxHEIGHT",
        default="1280x720",
        help="window resolution (default: 1280x720)",
    )
    argparser.add_argument(
        "--filter",
        metavar="PATTERN",
        default="vehicle.audi.*",
        help='actor filter (default: "vehicle.audi.*")',
    )
    argparser.add_argument(
        "--scenario",
        metavar="scenario_1.json",
        default="examples/scenario_1.json",
        help='scenario file',
    )

    argparser.add_argument(
        "--logfile",
        metavar="logs.txt",
        help="in order to print logs into the logfile",
    )


    # Parse arguments
    args = argparser.parse_args()
    args.description = "BounCMPE CarlaSim 2D Visualizer"
    args.width, args.height = [int(x) for x in args.res.split("x")]


    # Run game loop
    game_loop(args)


main()
