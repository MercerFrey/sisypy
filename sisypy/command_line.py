
import argparse

def main():
    
    argparser = argparse.ArgumentParser(description="run multiple tests with carla simulator")
    scenario_group = argparser.add_mutually_exclusive_group()

    scenario_group.add_argument(
        "-c", 
        "--concrete",
        metavar="concrete_scenario.json",
        default=None,
        help="concrete scenario json",
    )
    scenario_group.add_argument(
        "-a",
        "--abstract",
        metavar="abstract_scenario.json",
        default=None,
        help="abstract scenario",
    )

    # Parse arguments
    args = argparser.parse_args()
    args.description = "Sisypy"

    if args.concrete:
        print(args.concrete)
    elif args.abstract: print(args.abstract)
    else: argparser.print_help()

