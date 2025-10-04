from pathlib import Path
from src.operations import OperationsSet
from tools.init_operations_db import init_db


def test_load_operations_from_yaml(tmp_path):
    repo = Path(__file__).parents[1]
    yaml_path = repo / 'rules' / 'operations.yaml'
    ops = OperationsSet.from_yaml(yaml_path)
    entry = ops.get_by_rule('AWS-001')
    assert entry is not None
    assert round(entry.precision, 2) == round(90 / (90 + 10), 2)
    assert round(entry.recall, 2) == round(90 / (90 + 5), 2)


def test_init_operations_db_and_load(tmp_path):
    repo = Path(__file__).parents[1]
    out_db = tmp_path / 'operations.db'
    yaml_path = repo / 'rules' / 'operations.yaml'
    init_db(yaml_path, out_db)
    ops = OperationsSet.from_sqlite(out_db)
    entry = ops.get_by_rule('GENERIC-BASE64-01')
    assert entry is not None
    assert round(entry.precision, 2) == round(120 / (120 + 80), 2)
