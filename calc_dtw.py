import numpy as np
import matplotlib.pyplot as plt
from dtw import *


def calc_dtw(query, template):
    """
    Uses DTW to calculate distance between template and query.
    """

    # TODO sometimes throws memmory error!
    # Find the best match with the canonical recursion formula
    q_int = np.array(query.values).astype(np.int16)
    t_int = np.array(template.values).astype(np.int16)
    alignment = dtw(q_int, t_int, keep_internals=True)

    # Display the warping curve, i.e. the alignment curve
    alignment.plot(type="threeway")

    # Align and plot with the Rabiner-Juang type VI-c unsmoothed recursion
    dtw(query, template, keep_internals=True,
        step_pattern=rabinerJuangStepPattern(6, "c"))\
        .plot(type="twoway", offset=-2)

    # See the recursion relation, as formula and diagram
    print(rabinerJuangStepPattern(6, "c"))
    rabinerJuangStepPattern(6, "c").plot()

    plt.show()
