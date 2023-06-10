from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_generate_gabriel_uniform() -> None:
    response = client.post(
        "/generate",
        content="""{
        "l1_pops": 3,
        "l2_pops": 15,
        "pop_regions": 9,
        "core_node_scaling_threshold": 7,
        "random_core_nodes": 1,
        "random_core_node_connections": 1,
        "random_distribution": "uniform",
        "topology": "gabriel"
    }""",
    )
    assert response.status_code == 200


def test_generate_gabriel_normal() -> None:
    response = client.post(
        "/generate",
        content="""{
        "l1_pops": 3,
        "l2_pops": 15,
        "pop_regions": 9,
        "core_node_scaling_threshold": 7,
        "random_core_nodes": 1,
        "random_core_node_connections": 1,
        "random_distribution": "normal",
        "topology": "gabriel"
    }""",
    )
    assert response.status_code == 200


def test_generate_ring_uniform() -> None:
    response = client.post(
        "/generate",
        content="""{
        "l1_pops": 3,
        "l2_pops": 15,
        "pop_regions": 9,
        "core_node_scaling_threshold": 7,
        "random_core_nodes": 1,
        "random_core_node_connections": 1,
        "random_distribution": "uniform",
        "topology": "ring"
    }""",
    )
    assert response.status_code == 200


def test_generate_ring_normal() -> None:
    response = client.post(
        "/generate",
        content="""{
        "l1_pops": 3,
        "l2_pops": 15,
        "pop_regions": 9,
        "core_node_scaling_threshold": 7,
        "random_core_nodes": 1,
        "random_core_node_connections": 1,
        "random_distribution": "normal",
        "topology": "ring"
    }""",
    )
    assert response.status_code == 200


def test_generate_throws_error_too_much_pop_regions() -> None:
    response = client.post(
        "/generate",
        content="""{
        "l1_pops": 3,
        "l2_pops": 15,
        "pop_regions": 20,
        "core_node_scaling_threshold": 7,
        "random_core_nodes": 1,
        "random_core_node_connections": 1,
        "topology": "gabriel"
    }""",
    )
    assert response.status_code == 400


def test_generate_throws_error_edges_exceed_full_mesh() -> None:
    response = client.post(
        "/generate",
        content="""{
        "l1_pops": 3,
        "l2_pops": 15,
        "pop_regions": 9,
        "core_node_scaling_threshold": 7,
        "random_core_nodes": 1,
        "random_core_node_connections": 1000,
        "topology": "gabriel"
    }""",
    )
    assert response.status_code == 400
