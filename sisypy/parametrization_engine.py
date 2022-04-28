from smt.sampling_methods import Random
import numpy as np
import matplotlib.pyplot as plt
import json
import argparse

# pick sample_size samples with the limits specified
def sample_with_limits(xlimits, sample_size):
    sampling = Random(xlimits=xlimits)
    return sampling(sample_size)

    
def plot(ego_speed, v1_speed, v2_speed):
    
    fig, axs = plt.subplots(1, 3)

    axs[0].plot(ego_speed, v1_speed, "o")
    axs[0].set(xlabel="ego_speed", ylabel="v1_speed")

    axs[1].plot(ego_speed, v2_speed, "o")
    axs[1].set(xlabel="ego_speed", ylabel="v2_speed")

    axs[2].plot(v1_speed, v2_speed, "o")
    axs[2].set(xlabel="v1_speed", ylabel="v2_speed")

    for ax in axs:
        ax.yaxis.tick_right()

    plt.tight_layout()
    plt.show()

# read scenario_1.json and collects the min max values
def read_scenario(filename):
    with open(filename, 'r') as f:
        scenario = json.load(f)

    xlimits = np.array([])
    for _, attributes in scenario.items():
        
        temp = [attributes["controller"]["target_speed"]["min"]
            , attributes["controller"]["target_speed"]["max"]]
        
        if xlimits.size == 0:
            xlimits = np.append(xlimits, temp)
        else:
            xlimits = np.vstack((xlimits, temp))
    
    return scenario, xlimits


def write_to_json(new_scenario, filename):
    with open(filename, 'w') as f:
        json.dump(new_scenario, f, indent=4)


def write_scenario_speeds(scenario, speed_list, dir_path):
    for i in range(len(speed_list)):
        scenario["hero"]["controller"]["target_speed"]["value"] = speed_list[i][0]
        scenario["other1"]["controller"]["target_speed"]["value"] = speed_list[i][1]
        scenario["other2"]["controller"]["target_speed"]["value"] = speed_list[i][2]

        write_to_json(scenario, "{}par_scenario_{}.json".format(dir_path, i))

def main():
    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        "--filename",
        metavar="f",
        default="examples/scenario_1.json",
        help="scenario file that will be parameterized",
    )

    args = argparser.parse_args()

    scenario, xlimits = read_scenario(args.filename)
    samples = sample_with_limits(xlimits, 25)

    ego_speed = samples[:, 0]
    v1_speed = samples[:, 1]
    v2_speed = samples[:, 2]
    
    plot(ego_speed, v1_speed, v2_speed)
    write_scenario_speeds(scenario, samples, "examples/par/")
    
main()