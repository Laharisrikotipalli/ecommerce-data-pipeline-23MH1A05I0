def test_pipeline_orchestrator_runs():
    from scripts.pipeline_orchestrator import main
    assert main() is True
