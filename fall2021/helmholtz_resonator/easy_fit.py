from scipy.optimize import curve_fit
import numpy as np


def straight_line(x, A, B):
    return A*x + B


def main():
    x = [0, 2, 4] # fill with your values
    y = [0, 2, 4] # fill with your values

    popt, pcov = curve_fit(straight_line, x, y)

    A = popt[0]
    s_A = np.sqrt(np.diag(pcov))[0]

    print("Slope = {} +/- {}".format(A, s_A))


if __name__ == "__main__":
    main()
