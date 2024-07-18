import click
import subprocess

OLLAMA_CLI_COMMAND = "ollama"


@click.command()
@click.option('--file', '-f', type=click.Path(exists=True), help='Path to the text file.')
@click.argument('text', required=False)
def summarize(file, text):
    """Summarizes the given text or the text from a file using the Ollama CLI."""
    if file:
        # Read content of the file with explicit UTF-8 encoding
        with open(file, 'r', encoding='utf-8') as f:
            input_text = f.read().strip()
    elif text:
        input_text = text.strip()
    else:
        click.echo("Please provide either a text file or text to summarize.")
        return

    try:
        # Run the Ollama CLI command using subprocess.run
        command = [OLLAMA_CLI_COMMAND, 'run', 'qwen2:0.5b']
        process = subprocess.run(command, input=input_text, capture_output=True, text=True, check=True)

        # Print the summary output or error
        if process.returncode == 0:
            click.echo(f"Summary:\n{process.stdout.strip()}")
        else:
            click.echo(f"Error: {process.returncode} - {process.stderr.strip()}")

    except subprocess.CalledProcessError as e:
        click.echo(f"Error executing command: {e}")

    except Exception as e:
        click.echo(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    summarize()
