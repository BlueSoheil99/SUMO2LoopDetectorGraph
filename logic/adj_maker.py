from logic import utility

import os
import pandas as pd
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


def _get_loops(loop_adr) -> dict:
    loop_xml = utility.readxml(loop_adr)
    loop_dict = dict()
    for elem in loop_xml.iter('inductionLoop'):
        name, lane, pos = elem.get('id'), elem.get('lane'), elem.get('pos')
        name = name[:-2]
        edge = lane[:-2]
        loop_dict.setdefault(name, (edge, pos))
    return loop_dict


def _make_trips(loop_data, trips_adr):
    # Create the root element
    routes = ET.Element('routes')
    # # Create passenger vehicle type
    # new_type = ET.SubElement(routes, 'vType')
    # make_vtype(new_type)
    # Create trip elements
    counter = 0
    for name1, (edge1, pos1) in loop_data.items():
        for name2, (edge2, pos2) in loop_data.items():
            if name1 == name2:
                pass
            else:
                counter += 1
                ID = f'{name1}:{name2}'
                new_trip = ET.SubElement(routes, 'trip')
                new_trip.set('id', ID)
                new_trip.set('depart', str(counter))
                new_trip.set('from', edge1)
                new_trip.set('to', edge2)
                new_trip.set('departPos', pos1)
                new_trip.set('arrivalPos', pos2)

    # Write the XML to a new file
    # tree = ET.ElementTree(routes)  # Create an ElementTree object with the root element
    # Use minidom to pretty-print the XML with spacing
    xml_string = ET.tostring(routes, encoding='utf-8')
    dom = minidom.parseString(xml_string)
    pretty_xml = dom.toprettyxml(indent='  ')
    with open(trips_adr, 'w', encoding='utf-8') as xml_file:
        xml_file.write(pretty_xml)


def _make_routes(net_adr, trips_adr, routes_adr):
    # query = f'duarouter --configuration-file {router_config} --route-files {trips_adr}'
    query = f'duarouter --net-file {net_adr} --route-files {trips_adr} --output-file {routes_adr} --route-length "true"'
    os.system(query)


def get_adjacency_matrix(config_file):
    net_adr, loop_adr, trips_adr, routes_adr = (
        utility.read_yaml(["network_file", "loop_locations", "generated_trips", "distances"], config_file))


    loop_data = _get_loops(loop_adr)
    _make_trips(loop_data, trips_adr)
    _make_routes(net_adr, trips_adr, routes_adr)
    routes_xml = utility.readxml(routes_adr)

    index = list(loop_data.keys())
    columns = list(loop_data.keys())
    adj_mat = pd.DataFrame(0, index=index, columns=columns)
    for route in routes_xml.findall('./vehicle'):
        o,d = route.get('id').split(':')
        dist = route.find('route').get('routeLength')
        adj_mat.loc[o, d] =dist

    return adj_mat



if __name__ == '__main__':
    config_file = "filse/config.duarcfg"
    route_file = "files/trips.rou.xml"
    query = f'duarouter --configuration-file {config_file} --route-files {route_file}'
    os.system(query)