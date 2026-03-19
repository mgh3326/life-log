from importlib import reload

import app.core.config as config_module
import app.mcp_server.main as mcp_main


def test_settings_reads_mcp_port(monkeypatch):
    original_settings = config_module.settings
    monkeypatch.setenv("MCP_PORT", "8101")
    monkeypatch.setenv("MCP_HOST", "0.0.0.0")
    reload(config_module)
    # The reload(config_module) will recreate the 'settings' object
    # using the new environment variables.
    assert config_module.settings.MCP_PORT == 8101
    assert config_module.settings.MCP_HOST == "0.0.0.0"
    # Restore original settings to avoid test pollution
    config_module.settings = original_settings


def test_mcp_main_uses_configured_host_and_port(monkeypatch):
    # This is a bit tricky to test without actually running the server.
    # The plan suggests: monkeypatch.setattr(mcp_main.mcp, "run", lambda **kwargs: kwargs)
    # But mcp.run is called in main().

    captured_args = {}

    def mock_run(**kwargs):
        captured_args.update(kwargs)

    monkeypatch.setattr(mcp_main.mcp, "run", mock_run)
    monkeypatch.setattr(mcp_main.settings, "MCP_HOST", "0.0.0.0")
    monkeypatch.setattr(mcp_main.settings, "MCP_PORT", 8101)

    mcp_main.main()

    assert captured_args["host"] == "0.0.0.0"
    assert captured_args["port"] == 8101
    assert captured_args["transport"] == "streamable-http"
