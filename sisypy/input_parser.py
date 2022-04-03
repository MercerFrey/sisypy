import json
import numpy as np
import matplotlib.pyplot as plt
from smt.sampling_methods import Random

my_dict = {
    "ego" : {
        "x" : {
            "value": 12,
            "min" : 10,
            "max" : 15,
            "step" : 0.5
        },

        "y" : {
            "value" : 35,
            "min" : 20,
            "max" : 50,
            "step" : 2
        },

        "z" : {
            "value" : 35,
            "min" : 1,
            "max" :5
        }
    },
    "other" : {
        "x" : {
            "min" : 3,
            "max" : 65,
            "value": 12,
        },

        "y" : {
            "min" : 10,
            "max" : 100,
            "value" : 35,
        },

        "z" : {
            "value" : 35
        }
    }
}

# with open("my_json", 'w') as f:
#     json.dump(my_dict, f, indent=4)

actor_concrete = dict()

for actor, coordinate in my_dict.items():
    actor_concrete[actor] = []
    actor_values = [] 
    sampled_axises = []
    for axis, abstract_value  in coordinate.items():
        if set(("min", "max")).issubset(abstract_value.keys()):
            sampled_axises.append(axis)            
            actor_values.append([abstract_value["min"], abstract_value["max"]])
    xlimits = np.array(actor_concrete[actor])
    sampling = Random(xlimits=xlimits)
    num = 10
    x = sampling(num)

    print(x)
    print(sampled_axises)
    # print(x.shape)

    # plt.plot(x[:, 0], x[:, 1], "o")
    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.show()
print(actor_concrete)                
