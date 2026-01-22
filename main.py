

def workflow_pipeline_unsupervised():

    import os

    from flagx import GatingPipeline

    save_dir = './results/workflow_pipeline_unsupervised'
    os.makedirs(save_dir, exist_ok=True)

    channels = [
        'FS INT', 'SS INT', 'FL1 INT_CD14-FITC', 'FL2 INT_CD19-PE', 'FL3 INT_CD13-ECD', 'FL4 INT_CD33-PC5.5',
        'FL5 INT_CD34-PC7', 'FL6 INT_CD117-APC', 'FL7 INT_CD7-APC700', 'FL8 INT_CD16-APC750', 'FL9 INT_HLA-PB',
        'FL10 INT_CD45-KO'
    ]

    cutoffs = {
        'FS INT': 1000, 'SS INT': 500,
        'FL1 INT_CD14-FITC': 300, 'FL2 INT_CD19-PE': 300, 'FL3 INT_CD13-ECD': 300, 'FL4 INT_CD33-PC5.5': 300,
        'FL5 INT_CD34-PC7': 400, 'FL6 INT_CD117-APC': 400, 'FL7 INT_CD7-APC700': 400, 'FL8 INT_CD16-APC750': 400,
        'FL9 INT_HLA-PB': 100, 'FL10 INT_CD45-KO': 100,
    }

    preprocessing_kwargs = {'flavour': 'log10_w_custom_cutoffs', 'flavour_kwargs': {'cutoffs': cutoffs}}

    som_kwargs = {
        'som_topology': 'planar',
        'som_grid_type': 'rectangular',
        'som_dimensions': (6, 6),
        'neighborhood': 'gaussian',
        'gaussian_neighborhood_sigma': 0.1,
        'initialization': 'pca',
        'n_epochs': 10,
        'verbosity': 3,
    }

    # Initialize the pipeline
    gp = GatingPipeline(
        train_data_file_path='./data/training',
        train_data_file_names=None,
        train_data_file_type=None,
        save_path='./results/workflow_pipeline_unsupervised/gp_output',
        channels=channels,
        label_key=None,  # No labels
        compensate=False,
        channel_names_alignment_kwargs=None,
        relabel_data_kwargs=None,
        preprocessing_kwargs=preprocessing_kwargs,
        downsampling_kwargs={'target_num_events': 100},
        gating_method='som',
        gating_method_kwargs=som_kwargs,
    )

    # Train the underlying ML model
    gp.train()

    # Annotate and export data
    gp.inference(
        data_file_path='./data/testing',
        data_file_names=None,
        sample_wise=False,  # Export all into one file
        gate=False,  # Cannot gate since SOM was trained with unlabeled data
        dim_red_methods=('som', 'umap'),
        dim_red_method_kwargs=(None, {'n_jobs': -1}),
        save_path=save_dir,
        save_filename='annotated_data.fcs',
        val_range=(0, 2**20),
        keep_unscaled=False,
    )

    # Save the pipeline
    gp.save(filepath=save_dir)


def workflow_manual_unsupervised():

    import os

    from flagx.io import FlowDataManager
    from flagx.gating import SomClassifier
    from flagx.io import export_to_fcs








if __name__ == '__main__':

    workflow_pipeline_unsupervised()



    # import os
    # import pandas as pd
    #
    # train_path = './data/training'
    # test_path = './data/test'
    #
    # for fn in os.listdir(train_path):
    #     data = pd.read_csv(os.path.join(train_path, fn))
    #     data_ds = data.sample(n=100, random_state=42)
    #     data_ds.to_csv(os.path.join(test_path, fn), index=False)

    print('done')




