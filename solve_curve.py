import json
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution


BOUNDS = [(0, 50), (-0.05, 0.05), (0, 100)]
T_MIN, T_MAX = 6, 60


def load_points():
    return np.loadtxt("xy_data.csv", delimiter=",", skiprows=1)


def inverse_residuals(params, points):
    theta_degrees, M, X = params
    theta = np.radians(theta_degrees)
    x, y = points.T
    cosine, sine = np.cos(theta), np.sin(theta)

    t_hat = (x - X) * cosine + (y - 42) * sine
    q_hat = -(x - X) * sine + (y - 42) * cosine
    q_predicted = np.exp(M * t_hat) * np.sin(0.3 * t_hat)
    return t_hat, q_hat - q_predicted


def objective(params, points):
    t_hat, residuals = inverse_residuals(params, points)
    outside = np.maximum(T_MIN - t_hat, 0) + np.maximum(t_hat - T_MAX, 0)
    return np.mean(np.abs(residuals)) + 100 * np.mean(outside)


def fit(points):
    result = differential_evolution(
        objective, BOUNDS, args=(points,), seed=0
    )
    return result.x


def main():
    points = load_points()
    theta_degrees, M, X = fit(points)
    _, residuals = inverse_residuals((theta_degrees, M, X), points)

    result = {
        "theta_degrees": float(theta_degrees),
        "M": float(M),
        "X": float(X),
        "l1_loss": float(np.mean(np.abs(residuals))),
    }
    Path("result.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
