from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_gexf() -> None:
    response = client.post(
        "/convert?file_format=gexf",
        content="""
        {
           "nodes":[
              {
                 "node_id":"0_1",
                 "attributes":{
                    "pop_region":"0",
                    "node_type":"core",
                    "coordinate_x":0.4671831947233605,
                    "coordinate_y":0.36467550076790156
                 }
              },
              {
                 "node_id":"0_2",
                 "attributes":{
                    "pop_region":"0",
                    "node_type":"core",
                    "coordinate_x":0.4771831947233605,
                    "coordinate_y":0.36467550076790156
                 }
              }
           ],
           "edges":[
              {
                 "node_from":"0_1",
                 "node_to":"0_2",
                 "attributes":{
                    "weight":1.0,
                    "edge_type":"core_to_core"
                 }
              }
           ]
        }""",
    )
    assert response.status_code == 200


def test_graphml() -> None:
    response = client.post(
        "/convert?file_format=graphml",
        content="""
        {
           "nodes":[
              {
                 "node_id":"0_1",
                 "attributes":{
                    "pop_region":"0",
                    "node_type":"core",
                    "coordinate_x":0.4671831947233605,
                    "coordinate_y":0.36467550076790156
                 }
              },
              {
                 "node_id":"0_2",
                 "attributes":{
                    "pop_region":"0",
                    "node_type":"core",
                    "coordinate_x":0.4771831947233605,
                    "coordinate_y":0.36467550076790156
                 }
              }
           ],
           "edges":[
              {
                 "node_from":"0_1",
                 "node_to":"0_2",
                 "attributes":{
                    "weight":1.0,
                    "edge_type":"core_to_core"
                 }
              }
           ]
        }""",
    )
    assert response.status_code == 200


def test_generate_throws_error_input_validation_body() -> None:
    response = client.post(
        "/convert?file_format=gexf",
        content="""
        {
           "nodes":[
              {
                 "attributes":{
                    "pop_region":"0",
                    "node_type":"core",
                    "coordinate_x":0.4671831947233605,
                    "coordinate_y":0.36467550076790156
                 }
              },
              {
                 "node_id":"0_2",
                 "attributes":{
                    "pop_region":"0",
                    "node_type":"core",
                    "coordinate_x":0.4771831947233605,
                    "coordinate_y":0.36467550076790156
                 }
              }
           ],
           "edges":[
              {
                 "node_from":"0_1",
                 "node_to":"0_2",
                 "attributes":{
                    "weight":1.0,
                    "edge_type":"core_to_core"
                 }
              }
           ]
        }""",
    )
    assert response.status_code == 422


def test_generate_throws_error_input_validation_parameter_missing() -> None:
    response = client.post(
        "/convert",
        content="""
        {
           "nodes":[
              {
                 "node_id":"0_1",
                 "attributes":{
                    "pop_region":"0",
                    "node_type":"core",
                    "coordinate_x":0.4671831947233605,
                    "coordinate_y":0.36467550076790156
                 }
              },
              {
                 "node_id":"0_2",
                 "attributes":{
                    "pop_region":"0",
                    "node_type":"core",
                    "coordinate_x":0.4771831947233605,
                    "coordinate_y":0.36467550076790156
                 }
              }
           ],
           "edges":[
              {
                 "node_from":"0_1",
                 "node_to":"0_2",
                 "attributes":{
                    "weight":1.0,
                    "edge_type":"core_to_core"
                 }
              }
           ]
        }""",
    )
    assert response.status_code == 422


def test_generate_throws_error_input_validation_parameter_unknown_type() -> None:
    response = client.post(
        "/convert?file_format=docx",
        content="""
        {
           "nodes":[
              {
                 "node_id":"0_1",
                 "attributes":{
                    "pop_region":"0",
                    "node_type":"core",
                    "coordinate_x":0.4671831947233605,
                    "coordinate_y":0.36467550076790156
                 }
              },
              {
                 "node_id":"0_2",
                 "attributes":{
                    "pop_region":"0",
                    "node_type":"core",
                    "coordinate_x":0.4771831947233605,
                    "coordinate_y":0.36467550076790156
                 }
              }
           ],
           "edges":[
              {
                 "node_from":"0_1",
                 "node_to":"0_2",
                 "attributes":{
                    "weight":1.0,
                    "edge_type":"core_to_core"
                 }
              }
           ]
        }""",
    )
    assert response.status_code == 422
