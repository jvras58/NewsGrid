"""
Script para iniciar todos os workers em background.
"""

import signal
import subprocess
import sys
import time


def start_worker(command):
    """Inicia um worker em background."""
    return subprocess.Popen(command, shell=True)


def main():
    workers = [
        "uv run python -m app.workers.worker_researcher",
        "uv run python -m app.workers.worker_analyst",
    ]

    processes = []

    for worker in workers:
        print(f"Iniciando {worker}...")
        proc = start_worker(worker)
        processes.append((worker, proc))
        time.sleep(1)

    print("Todos os workers iniciados. Pressione Ctrl+C para parar.")

    def stop_workers(signum, frame):
        print("\nParando workers...")
        for name, proc in processes:
            print(f"Parando {name}...")
            proc.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, stop_workers)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_workers(None, None)


if __name__ == "__main__":
    main()
