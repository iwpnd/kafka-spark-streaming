from click.testing import CliRunner

from producer import producer


def test_producer_cli_help():
    runner = CliRunner()

    result = runner.invoke(producer.produce, "--help")

    assert result.exit_code == 0
    assert "kafkahost" in result.output
    assert "topic" in result.output
    assert "file" in result.output
