import argparse
import subprocess

from .run_simulation import game_loop, run_simulation

from .parametrization_engine import parametrize

def main():
    
    argparser = argparse.ArgumentParser(description="run multiple tests with carla simulator")
    scenario_group = argparser.add_mutually_exclusive_group()

    scenario_group.add_argument(
        "-c", 
        "--concrete",
        action='store_true',
        help="concrete scenario",
    )

    scenario_group.add_argument(
        "-p",
        "--parametrize",
        action='store_true',
        help="parameterization",
    )

    scenario_group.add_argument(
        "--scenario_type",
        metavar="straight",
        default="straight",
        help="straight or curved",
    )

    scenario_group.add_argument(
        "-m",
        "--map",
        metavar="Town01",
        default=None,
        help="change world map",
    )

    scenario_group.add_argument(
        "-f", 
        "--filename",
        metavar="straigth.json",
        default="examples/scenario_1.json",
        help="filename",
    )

    # Parse arguments
    args = argparser.parse_args()
    args.description = "Sisypy"

    if args.map:
        subprocess.call(f"python sisypy/config.py -m {args.map}", shell=True)    
    elif args.parametrize:
        parametrize(args.scenario_type)
    elif args.concrete:
        # TODO does not work for one single simulation
        game_loop(args.filename)
    else:
        argparser.print_help()