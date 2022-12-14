import numpy as np

# Import libEnsemble items for this test
from libensemble.libE import libE
from libensemble.sim_funcs.one_d_func import one_d_example as sim_f
from libensemble.gen_funcs.sampling import latin_hypercube_sample as gen_f
from libensemble.tools import parse_args, save_libE_output, add_unique_random_streams

if __name__ == "__main__":

    nworkers, is_manager, libE_specs, _ = parse_args()
    libE_specs["save_every_k_gens"] = 300
    libE_specs["safe_mode"] = False

    sim_specs = {
        "sim_f": sim_f,
        "in": ["x"],
        "out": [("f", float)],
    }

    gen_specs = {
        "gen_f": gen_f,
        "out": [("x", float, (1,))],
        "user": {
            "gen_batch_size": 500,
            "lb": np.array([-3]),
            "ub": np.array([3]),
        },
    }

    persis_info = add_unique_random_streams({}, nworkers + 1, seed=1234)

    exit_criteria = {"gen_max": 501}

    # Perform the run
    H, persis_info, flag = libE(sim_specs, gen_specs, exit_criteria, persis_info, libE_specs=libE_specs)

    if is_manager:
        assert len(H) >= 501
        print("\nlibEnsemble with random sampling has generated enough points")
        save_libE_output(H, persis_info, __file__, nworkers)
