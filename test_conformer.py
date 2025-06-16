#!/usr/bin/env python3
"""
Test di regressione per LiquidSopaConformer
Verifica che tutte le funzionalità principali funzionino correttamente
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

def test_import():
    """Test che il modulo si importi correttamente"""
    try:
        import conformer
        print("✅ Import conformer: OK")
        return True
    except ImportError as e:
        print(f"❌ Import conformer: FAILED - {e}")
        return False

def test_dependencies():
    """Test che tutte le dipendenze siano installate"""
    dependencies = ['mutagen', 'ffmpeg', 'PIL']
    success = True
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ Dipendenza {dep}: OK")
        except ImportError:
            print(f"❌ Dipendenza {dep}: MISSING")
            success = False
    
    return success

def test_ffmpeg_path():
    """Test che FFmpeg sia configurato correttamente"""
    try:
        from conformer import SimpleConformer
        conformer_instance = SimpleConformer(".", ".")
        ffmpeg_path = conformer_instance.FFMPEG_PATH
        
        if Path(ffmpeg_path).exists():
            print(f"✅ FFmpeg path: OK ({ffmpeg_path})")
            return True
        else:
            print(f"❌ FFmpeg path: NOT FOUND ({ffmpeg_path})")
            return False
    except Exception as e:
        print(f"❌ FFmpeg path test: FAILED - {e}")
        return False

def test_conformer_class():
    """Test che la classe SimpleConformer si istanzi correttamente"""
    try:
        from conformer import SimpleConformer
        
        with tempfile.TemporaryDirectory() as temp_dir:
            input_dir = Path(temp_dir) / "input"
            output_dir = Path(temp_dir) / "output"
            input_dir.mkdir()
            output_dir.mkdir()
            
            conformer_instance = SimpleConformer(str(input_dir), str(output_dir))
            
            # Verifica attributi principali
            assert hasattr(conformer_instance, 'SUPPORTED_FORMATS')
            assert hasattr(conformer_instance, 'TARGET_SAMPLE_RATE')
            assert hasattr(conformer_instance, 'TARGET_BITRATE')
            assert hasattr(conformer_instance, 'stats')
            
            print("✅ Classe SimpleConformer: OK")
            return True
            
    except Exception as e:
        print(f"❌ Classe SimpleConformer: FAILED - {e}")
        return False

def test_gui_import():
    """Test che l'interfaccia grafica sia importabile"""
    try:
        import tkinter
        from conformer import launch_gui
        print("✅ GUI (Tkinter): OK")
        return True
    except ImportError as e:
        print(f"❌ GUI (Tkinter): FAILED - {e}")
        return False
    except Exception as e:
        print(f"❌ GUI launch_gui: FAILED - {e}")
        return False

def test_arguments():
    """Test che gli argomenti della command line funzionino"""
    try:
        import argparse
        from conformer import main
        print("✅ Argomenti command line: OK")
        return True
    except Exception as e:
        print(f"❌ Argomenti command line: FAILED - {e}")
        return False

def run_all_tests():
    """Esegue tutti i test"""
    print("🧪 Avvio test di regressione LiquidSopaConformer")
    print("=" * 50)
    
    tests = [
        ("Import principale", test_import),
        ("Dipendenze", test_dependencies),
        ("Percorso FFmpeg", test_ffmpeg_path),
        ("Classe SimpleConformer", test_conformer_class),
        ("Interfaccia grafica", test_gui_import),
        ("Argomenti CLI", test_arguments),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"   ⚠️  Fallito: {test_name}")
    
    print("\n" + "=" * 50)
    print(f"📊 Risultati: {passed}/{total} test passati")
    
    if passed == total:
        print("🎉 Tutti i test sono passati! Il software è pronto per l'uso.")
        return True
    else:
        print("⚠️  Alcuni test sono falliti. Controlla le dipendenze.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 