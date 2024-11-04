from logic import utility
import pandas as pd

def _get_loops(loop_adr) -> dict:
    loop_xml = utility.readxml(loop_adr)
    loop_dict = dict()
    for elem in loop_xml.iter('inductionLoop'):
        name, lane, pos = elem.get('id'), elem.get('lane'), elem.get('pos')
        name = name[:-2]
        edge = lane[:-2]
        loop_dict.setdefault(name, (edge, pos))
    return loop_dict


def get_flows_and_speeds(config_file):
    loop_output = utility.read_yaml(['loop_output'], config_file)[0]
    loop_output = utility.readxml(loop_output)

    flow_dict = dict()
    speed_dict = dict()

    for observation in loop_output.iter('interval'):
        begin, end = (observation.get('begin')), (observation.get('end'))
        name, nVeh = observation.get('id'), int(observation.get('nVehContrib'))
        # speed = float(observation.get('speed or harmonicMeanSpeed????'))
        name = name[:-2]
        timestep = begin+'-'+end
        if flow_dict.get(name) is None:
            flow_dict[name] = {timestep: nVeh}
        else:
            if flow_dict[name].get(timestep) is None:
                flow_dict[name][timestep] = nVeh
            else:
                flow_dict[name][timestep] += nVeh
    flow_df = pd.DataFrame.from_dict(flow_dict, orient='index')

    return flow_df.T