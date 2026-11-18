
import subprocess
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CARPETA = Path(__file__).resolve().parent
ARCHIVO = CARPETA / "main.py"

class Recargador(FileSystemEventHandler):
    def __init__(self):
        self.proceso = None
        self.reiniciar()

    def reiniciar(self):
        if self.proceso is not None:
            self.proceso.terminate()
            try:
                self.proceso.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proceso.kill()
                self.proceso.wait()

        print("Iniciando osito virtual...")
        self.proceso = subprocess.Popen(
            [sys.executable, str(ARCHIVO)],
            cwd=CARPETA
        )

    def on_modified(self, evento):
        if not evento.is_directory and Path(evento.src_path).resolve() == ARCHIVO:
            print("Cambios detectados. Reiniciando...")
            self.reiniciar()

recargador = Recargador()
observador = Observer()
observador.schedule(recargador, str(CARPETA), recursive=False)
observador.start()

try:
    while True:
        observador.join(timeout=1)
except KeyboardInterrupt:
    pass
finally:
    observador.stop()
    observador.join()
    if recargador.proceso is not None:
        recargador.proceso.terminate()
        recargador.proceso.wait()
