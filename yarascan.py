import os
import yara
from sys import argv
from rich import print
try:
    a = 0
    dir_name = './rules/'
    file_to_scan = argv[1]

    for file in os.listdir(dir_name):
            file_path = dir_name + file

            rules = yara.compile(filepath=file_path)

            matches = rules.match(file_to_scan)


            if matches and a == 0:
                print("\n\n[bold red]       ||>>> Malware Detected <<<||[/bold red]\n\n")
                print(f"[bold red][+][/bold red] the file [bold green]{file_to_scan}[/bold green] matches the [bold cyan]Yara rules[/bold cyan]:")
                a = 1
            if matches:
                for match in matches:
                    print(f"- Rule: [bold yellow]{match.rule}[/bold yellow]")
    if a == 0:
        print("\n\n[bold green]       ||>>> No Malware Detected <<<||[/bold green]\n\n")
except:
    print("[bold red][*]something went wrong![/bold red] \n\n[bold green]python3[/bold green] [bold yellow]scan.py[/bold yellow] [bold cyan]{file to scan}[/bold cyan]")
