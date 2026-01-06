import numpy as np
from src.scoring import compute_defense_scores, main_score, compute_plot_size

def test_defense_scores_basic():
    d = np.array([0.0, 1000.0, 5000.0])
    cnt = np.array([0, 3, 10])
    score_def, score_density = compute_defense_scores(d, cnt)
    assert score_def.shape == d.shape
    assert score_density[0] == 0.0
    assert score_density[2] == 1.0
    s = main_score(score_def, score_density)
    assert np.all(s >= 0.0) and np.all(s <= 1.0)

def test_plot_size_edge_cases():
    scores = np.array([0.5, 0.5, 0.5])
    sizes = compute_plot_size(scores, min_size=10, max_size=50)
    assert sizes.min() >= 10 and sizes.max() <= 50

