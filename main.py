from logic.adj_maker import get_adjacency_matrix
from logic import data_extractor


if __name__ == '__main__':
    '''

    '''

    # read config file and related network and files
    config_address = 'config.yaml'

    A = get_adjacency_matrix(config_address)
    A.to_csv('output/adjacency_matrix.csv')
    # df = pd.read_csv('output/adjacency_matrix.csv')

    flows_df = data_extractor.get_flows_and_speeds(config_address)
    flows_df.to_csv('output/nVehicles.csv')
    print('hi!')
