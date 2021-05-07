import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel
from active_learning.problem import ActiveLearningProblem
from active_learning.query_strats.random_sampling import RandomQuery
from active_learning.query_strats.regression import (GreedySelection, MCALSelection, UncertaintySampling)
from sklearn.preprocessing import MinMaxScaler

def active_learning(path, num_to_select, acquisition, target_file_name="indices.csv"):
    # open the .csv file as data
    data = pd.read_csv(path)

    # normalize the data (0-1)
    scaler = MinMaxScaler()
    scaler.fit(data)
    scaled_data = pd.DataFrame(scaler.transform(data), columns=data.columns)

    # separate features from targets
    features = scaled_data.iloc[:, 1:-1]
    targets = scaled_data.iloc[:, -1]

    # find the indices(rows) that have a label/target
    labeled = targets[targets.notnull()].index.tolist()

    # drop all columns that don't have a target
    targetsPure = targets.dropna()
    targetsPure.to_numpy()

    # create the problem statement
    problem = ActiveLearningProblem(points=features.to_numpy(), labeled_ixs=labeled, labels=targetsPure.to_numpy())

    # create the kernel and regression function
    kernel = 1.0 * RBF(length_scale=100.0, length_scale_bounds=(1e-2, 1e3)) \
             + WhiteKernel(noise_level=1, noise_level_bounds=(1e-10, 1e+1))
    regressor = GaussianProcessRegressor(kernel=kernel, alpha=0.0)

    # calculate the next set of indices according to a specific acquisition function for active learning
    if (acquisition == "random"):
        ixs = RandomQuery().select_points(problem, num_to_select)
    elif (acquisition == "greedy"):
        ixs = GreedySelection(model=regressor).select_points(problem, num_to_select)
    elif (acquisition == "mcal"):
        ixs = MCALSelection().select_points(problem, num_to_select)
    elif (acquisition == "uncertainty"):
        ixs = UncertaintySampling(model=regressor).select_points(problem, num_to_select)

    # convert the new indices into its experimental data (unscaled) and save it as a .csv
    data.iloc[ixs, 1:-1].to_csv(target_file_name)