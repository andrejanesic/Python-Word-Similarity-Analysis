from scipy.linalg import solve_toeplitz
import numpy as np
import constants


def autocor(signal, k):
    """
    Autocorrelation function.
    """
    if k == 0:
        return np.sum(signal**2)
    else:
        return np.sum(signal[k:]*signal[:-k])


def levinson(w_sig, p):
    """
    Find alpha coefficients alpha_1, ... , alpha_k which minimize the square sum of error
    """
    r_list = [autocor(w_sig, i) for i in range(p)]
    b_list = [autocor(w_sig, i) for i in range(1, p + 1)]
    LPC = solve_toeplitz((r_list, r_list), b_list)
    return LPC


def residual(windowed_signal, p):
    """
    Get prediction, residual signal
    """

    LPC = levinson(windowed_signal, p)
    length = len(windowed_signal)
    prediction = np.zeros((length))
    win_sig = np.pad(windowed_signal, p)[:-p]
    for k in range(length):
        prediction[k] = np.sum(win_sig[k:k+p][::-1]*LPC)
    error = windowed_signal - prediction
    return prediction, error


def prediction(signal, window, p, overlap=0.5):
    """
    Get prediction, residual error for whole signal
    """

    shift = int(len(window)*overlap)
    if len(signal) % shift != 0:
        pad = np.zeros(shift - (len(signal) % shift))
        new_signal = np.append(signal, pad)
    else:
        new_signal = signal
    index = (len(new_signal) // shift) - 1

    whole_prediction = np.zeros((len(new_signal)), dtype=signal.dtype)
    whole_error = np.zeros((len(new_signal)), dtype=signal.dtype)

    for i in range(index):
        try:
            win_sig = new_signal[i*shift:i*shift+len(window)]*window
            prediction, error = residual(win_sig, p)
            whole_prediction[i*shift:i*shift+len(window)] += prediction
            whole_error[i*shift:i*shift+len(window)] += error
        except:
            print(constants.STR_ERR_BAD_LPC_OPERANDS)

    return whole_prediction, whole_error
