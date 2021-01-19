# Supporting functions
import numpy as np
import pandas as pd


def find_nodes(face, df):
    # Finds the nodes involved in any simplex (face)
    nodes = []
    for cell in face:
        nodes.append(df[df["cell_id"]==cell]["nodes"].item())
    return np.unique(nodes)

def create_fake_fsc_df(n_nodes, n_simps, max_dim):
    # For creating a fake data frame with appropriate headings.

    node_data = np.arange(n_nodes)
    cell_id = np.arange(n_nodes)
    node_dim = np.zeros(n_nodes)
    node_nodes = [[i] for i in np.arange(n_nodes)]
    node_weight = np.random.rand(n_nodes)
    node_faces = [[] for i in np.arange(n_nodes)]

    fsc_df = pd.DataFrame({"cell_id": cell_id, "dim": node_dim, "nodes": node_nodes, "weight": 5+node_weight,
                          "faces": node_faces})


    for dim in np.arange(1,max_dim+1):

        dim_m1_df = fsc_df[fsc_df["dim"] == dim-1]
        temp_df = pd.DataFrame({"cell_id": np.arange(np.sum(n_simps[:dim]),np.sum(n_simps[:(dim+1)])),
                                "dim": dim*np.ones(n_simps[dim]),
                                "weight": (max_dim-dim)+np.random.rand(n_simps[dim]),
                                "faces": [np.random.choice(dim_m1_df.cell_id, dim+1) for i in np.arange(n_simps[dim])]})
        if dim == 1:
            temp_df["nodes"] = temp_df.faces
        else:
            temp_df["nodes"] = [np.random.choice(fsc_df[fsc_df.dim==0].cell_id, dim+1) for i in np.arange(n_simps[dim])]
    #         temp_df["nodes"] = temp_df["faces"].apply(find_nodes, df = dim_m1_df) Explodes for high dim.

        fsc_df = pd.concat([fsc_df, temp_df])

    print(f'Created df with length {len(fsc_df)}. Expected {sum(n_simps)}.')
    return fsc_df

