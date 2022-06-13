# Sisypy

This project contains a multi-container Carla project template for educational purposes.


## Setup the environment

- Ubuntu 20.04 environment (Ubuntu on WSL may work, not recommended)
- Docker (first [install Docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) and then follow [Docker post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/))
- Docker Compose ([install docker-compose](https://docs.docker.com/compose/install/))
- Python 3.8 (comes by default in Ubuntu 20.04)
- Install and upgrade `pip` to the latest version 
- Install `carla` package using `pip install carla==0.9.13`

## Quickstart

Once your environment set up, start Carla server from the project directory using

```
docker-compose up -d 
```

Then write the following command to the terminal from the project directory

```
pip install .
```  

Now you are able to use Sisypy from the terminal 
As a demo you can try following commands

```
sisypy -m Town04
sisypy -p --scenario_type straight
```


and close servers once done using

```
docker-compose down
```

You can see your results with the following command

```
mkdocs serve
```

The documentation at the http://127.0.0.1:8000/ contains the results after the simulation
