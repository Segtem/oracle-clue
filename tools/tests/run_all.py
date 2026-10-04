"""Runner para ejecutar todos los tests del arnés de web y guía bajo tools/tests."""
from pathlib import Path
import sys
import unittest

def main():
    root = Path(__file__).resolve().parent
    suite = unittest.defaultTestLoader.discover(str(root), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    print("=" * 70)
    print("EJECUTANDO ARNÉS DE PRUEBAS DE ORACLE CLUE (WEB Y GUÍA)")
    print("=" * 70)
    result = runner.run(suite)
    if not result.wasSuccessful():
        print(f"\nERRORES DETECTADOS: {len(result.errors)}, FALLOS: {len(result.failures)}")
        sys.exit(1)
    else:
        print("\nTODAS LAS COMPROBACIONES PASARON CORRECTAMENTE.")

if __name__ == "__main__":
    main()
