def test_pipeline_orchestrator_runs():
    from scripts.orchestration.run_pipeline import main
    assert main() is True
