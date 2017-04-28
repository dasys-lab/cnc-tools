import pystache
from os import path

WIFIS = [
    "msl",
    "robo_dev_net",
    "coimbra"
]

def gen_interfaces(robot_type, robot_id, wifi):

    # get template
    template_path = path.join(path.dirname(__file__), "data/network/interfaces_template.mustache")
    f = open(template_path, "r")
    template = f.read()

    data = dict()
    data["ip_end"] = robot_id + 10

    # wifi variable
    if wifi in WIFIS:
        data[wifi] = True
    else:
        return

    # robot varibale
    if robot_type == "player":
        data["player"] = True
    elif robot_type == "goalie":
        data["goalie"] = True
    else:
        return

    # render template
    return pystache.render(template, data)

def update_interfaces(robot_type, robot_id, wifi):
    interfaces = gen_interfaces(robot_type, robot_id, wifi)

    if interfaces == None:
        return
        
    f = open("/etc/network/interfaces_test", "w")
    f.write(interfaces)