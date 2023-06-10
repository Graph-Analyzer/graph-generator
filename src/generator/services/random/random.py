import random
import numpy as np
from numpy.random import Generator
from src.generator.models import RandomDistribution


def create_random_generator(
    seed: int | None = None,
) -> Generator:
    # Legacy support for packages that do not allow generator passing
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed=seed)

    return np.random.default_rng(seed=seed)


def create_random_points(
    points: int,
    random_distribution: RandomDistribution,
    random_generator: Generator,
) -> np.ndarray:
    coordinates: np.ndarray = np.ndarray([])

    match random_distribution:
        case RandomDistribution.Uniform:
            coordinates = random_generator.uniform(
                low=-1,
                high=1,
                size=[points, 2],
            )
        case RandomDistribution.Normal:
            coordinates = random_generator.normal(
                loc=0.0,
                scale=1.0,
                size=[points, 2],
            )

    return coordinates
