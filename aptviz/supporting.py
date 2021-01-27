# Supporting functions
import numpy as np
import pandas as pd


def find_nodes(face, df):
    # Finds the nodes involved in any simplex (face)
    nodes = []
    for cell in face:
        nodes.append(df[df["cell_id"]==cell]["nodes"].item())
    return nodes

def create_fake_fsc_df(n_nodes, n_simps, max_dim):
    # For creating a fake data frame with appropriate headings.

    cell_id = np.arange(n_nodes)
    node_dim = np.zeros(n_nodes)
    node_nodes = [[i] for i in np.arange(n_nodes)]
    node_weight = np.random.rand(n_nodes)
    node_faces = [[] for i in np.arange(n_nodes)]

    fsc_df = pd.DataFrame({"cell_id": cell_id, "dim": node_dim, "nodes": node_nodes, "weight": max_dim+node_weight,
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
            # temp_df["nodes"] = temp_df["faces"].apply(find_nodes, df = dim_m1_df) # Doesn't work? 

        fsc_df = pd.concat([fsc_df, temp_df])
        fsc_df.dim = fsc_df.dim.astype(int)

        # Calculate rank based on weight
        fsc_df["rank"] = np.argsort(-fsc_df.weight).astype(float)

        # Add random maximal flags
        fsc_df["is_maximal"] = [np.random.randint(0, 2) for i in np.arange(fsc_df.shape[0])]

    print(f'Created df with length {len(fsc_df)}. Expected {sum(n_simps)}.')
    return fsc_df

def create_fake_barcode(fsc_df, n_bars):
    # Creates a fake barcode from a filtered simplicial complex df. For dev use only.
    max_filtration = np.max(fsc_df["rank"])
    max_dim = np.max(fsc_df["dim"])

    bar_id = np.arange(n_bars)
    bar_dim = np.random.randint(0,max_dim,size=n_bars)
    bar_birth = np.random.choice(fsc_df[fsc_df.dim==1]["rank"],n_bars)
    bar_death = np.random.choice(fsc_df[fsc_df.dim==2]["rank"],size = n_bars)
    bar_rep = [np.random.choice(fsc_df[fsc_df.dim==1].cell_id, size=4, replace=False) for k in np.arange(n_bars)]
    # simp_weight = np.random.rand(nSimps)*(simp_dim+1)

    bar_df = pd.DataFrame({"bar_id" : bar_id,
                           "bar_dim" : bar_dim,
                           "bar_birth" : bar_birth,
                           "bar_death" : bar_death,
                           "rep" : bar_rep,
                           "lifetime": bar_death-bar_birth})

    bar_df["bar_dim"] = bar_df["bar_dim"].astype(str)
    return bar_df

