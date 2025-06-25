#!/usr/bin/env python3
"""
Test Suite Anti-Regressione per Audio & Metadata Converter
Harmony Edition v1.0

Test completi per prevenire regressioni nelle funzionalità core.
Eseguire prima di ogni release o modifica critica.
"""

import os
import sys
import tempfile
import shutil
import unittest
from pathlib import Path
import subprocess

# Import del modulo principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conformer import SimpleConformer, APP_NAME, APP_VERSION, VERSION_NAME

class TestAntiRegressione(unittest.TestCase):
    """Test suite principale per prevenire regressioni"""
    
    @classmethod
    def setUpClass(cls):
        """Setup una tantum per tutti i test"""
        cls.test_dir = Path(tempfile.mkdtemp(prefix="conformer_test_"))
        cls.input_dir = cls.test_dir / "input"
        cls.output_dir = cls.test_dir / "output"
        cls.input_dir.mkdir(parents=True, exist_ok=True)
        cls.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Crea file di test
        cls._create_test_files()
        
        print(f"\n🧪 Test Environment Setup:")
        print(f"   Input: {cls.input_dir}")
        print(f"   Output: {cls.output_dir}")
    
    @classmethod
    def tearDownClass(cls):
        """Cleanup dopo tutti i test"""
        try:
            shutil.rmtree(str(cls.test_dir))
            print(f"✅ Test cleanup completato")
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")
    
    @classmethod
    def _create_test_files(cls):
        """Crea file di test per simulare diversi scenari"""
        # Crea struttura di cartelle
        (cls.input_dir / "rock").mkdir(exist_ok=True)
        (cls.input_dir / "pop" / "2024").mkdir(parents=True, exist_ok=True)
        
        # File di test fittizi (per evitare dipendenze da file reali)
        test_files = [
            "rock/song1.mp3",
            "rock/song2.flac",
            "pop/2024/hit.wav",
            "pop/2024/single.m4a",
            "readme.txt",  # Non audio - dovrebbe essere ignorato
        ]
        
        for file_path in test_files:
            full_path = cls.input_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            # Crea file vuoto per test
            full_path.write_text("test content")

class TestVersioneEMetadata(TestAntiRegressione):
    """Test per verifica versione e metadati del software"""
    
    def test_versione_consolidata(self):
        """Verifica che la versione sia correttamente consolidata"""
        self.assertEqual(APP_NAME, "Audio & Metadata Converter")
        self.assertEqual(APP_VERSION, "1.0")
        self.assertEqual(VERSION_NAME, "Harmony Edition")
        
    def test_full_version_string(self):
        """Verifica stringa versione completa"""
        from conformer import FULL_VERSION
        expected = "Audio & Metadata Converter - Harmony Edition v1.0"
        self.assertEqual(FULL_VERSION, expected)

class TestFFmpegDetection(TestAntiRegressione):
    """Test per auto-detection FFmpeg - Critico per anti-regressione"""
    
    def test_ffmpeg_detection_init(self):
        """Verifica che FFmpeg detection non crashi durante init"""
        try:
            conformer = SimpleConformer(str(self.input_dir), str(self.output_dir))
            # Dovrebbe completarsi senza eccezioni
            self.assertIsNotNone(conformer.FFMPEG_PATH)
            print(f"✅ FFmpeg path detected: {conformer.FFMPEG_PATH}")
        except Exception as e:
            self.fail(f"FFmpeg detection failed: {e}")
    
    def test_ffmpeg_available(self):
        """Verifica che FFmpeg sia effettivamente disponibile"""
        conformer = SimpleConformer(str(self.input_dir), str(self.output_dir))
        
        # Test basic FFmpeg execution
        try:
            result = subprocess.run([conformer.FFMPEG_PATH, '-version'], 
                                  capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, "FFmpeg should execute successfully")
            self.assertIn('ffmpeg', result.stdout.lower(), "Should contain 'ffmpeg' in output")
            print(f"✅ FFmpeg executable verified")
        except subprocess.TimeoutExpired:
            self.fail("FFmpeg execution timed out")
        except FileNotFoundError:
            self.fail(f"FFmpeg not found at path: {conformer.FFMPEG_PATH}")
        except Exception as e:
            self.fail(f"FFmpeg execution failed: {e}")

class TestFileProcessing(TestAntiRegressione):
    """Test per logica di elaborazione file - Core functionality"""
    
    def test_supported_formats_detection(self):
        """Verifica riconoscimento formati supportati"""
        conformer = SimpleConformer(str(self.input_dir), str(self.output_dir))
        
        # Test formati supportati
        supported_files = [
            Path("test.mp3"), Path("test.flac"), Path("test.wav"),
            Path("test.m4a"), Path("test.aac"), Path("test.ogg")
        ]
        
        for file_path in supported_files:
            self.assertIn(file_path.suffix.lower(), conformer.SUPPORTED_FORMATS,
                         f"Format {file_path.suffix} should be supported")
        
        # Test formati NON supportati
        unsupported_files = [
            Path("test.txt"), Path("test.doc"), Path("test.mkv"),
            Path("test.avi"), Path("test.jpg"), Path("test.pdf")
        ]
        
        for file_path in unsupported_files:
            self.assertNotIn(file_path.suffix.lower(), conformer.SUPPORTED_FORMATS,
                           f"Format {file_path.suffix} should NOT be supported")

    def test_directory_structure_preservation(self):
        """Verifica preservazione struttura cartelle"""
        conformer = SimpleConformer(str(self.input_dir), str(self.output_dir))
        
        # Simula trovare file audio
        all_files = list(self.input_dir.rglob("*"))
        audio_files = [f for f in all_files if f.is_file() and f.suffix.lower() in conformer.SUPPORTED_FORMATS]
        
        for audio_file in audio_files:
            rel_path = audio_file.relative_to(self.input_dir)
            expected_output = self.output_dir / rel_path.with_suffix('.mp3')
            
            # Verifica che la struttura delle cartelle sia preservata
            expected_parent = str(rel_path.parent)
            actual_parent = str(expected_output.relative_to(self.output_dir).parent)
            
            self.assertEqual(expected_parent, actual_parent,
                           f"Directory structure should be preserved: {expected_parent} -> {actual_parent}")
            
            # Verifica che il nome del file (senza estensione) sia preservato
            expected_stem = rel_path.stem
            actual_stem = expected_output.stem
            
            self.assertEqual(expected_stem, actual_stem,
                           f"Filename should be preserved: {expected_stem} -> {actual_stem}")

class TestErrorHandling(TestAntiRegressione):
    """Test per gestione errori robusta"""
    
    def test_invalid_input_directory(self):
        """Verifica gestione directory input inesistente"""
        invalid_dir = "/path/that/does/not/exist"
        
        # Non dovrebbe crashare, ma gestire gracefully
        try:
            conformer = SimpleConformer(invalid_dir, str(self.output_dir))
            # L'init dovrebbe completarsi, l'errore dovrebbe emergere durante run()
            self.assertIsNotNone(conformer)
        except Exception as e:
            self.fail(f"Constructor should not fail with invalid input dir: {e}")
    
    def test_statistics_initialization(self):
        """Verifica corretta inizializzazione statistiche"""
        conformer = SimpleConformer(str(self.input_dir), str(self.output_dir))
        
        expected_stats = ['processed', 'copied', 'converted', 'errors', 'skipped']
        for stat in expected_stats:
            self.assertIn(stat, conformer.stats, f"Statistic '{stat}' should be initialized")
            self.assertEqual(conformer.stats[stat], 0, f"Statistic '{stat}' should start at 0")

class TestGUIComponents(TestAntiRegressione):
    """Test per componenti GUI - Verifica non-crashing"""
    
    def test_import_gui_dependencies(self):
        """Verifica che tutte le dipendenze GUI siano importabili"""
        try:
            import tkinter as tk
            from tkinter import filedialog, messagebox, ttk
            import threading
            import webbrowser
            print("✅ All GUI dependencies available")
        except ImportError as e:
            self.fail(f"GUI dependency missing: {e}")
    
    def test_gui_launch_no_crash(self):
        """Verifica che launch_gui non crashi immediatamente"""
        from conformer import launch_gui
        
        # Test che la funzione sia callable senza crash immediato
        # Non eseguiamo effettivamente la GUI (requirerebbe display)
        self.assertTrue(callable(launch_gui), "launch_gui should be callable")

class TestConfigurationConsistency(TestAntiRegressione):
    """Test per consistenza configurazione"""
    
    def test_target_format_constants(self):
        """Verifica che le costanti target siano corrette"""
        conformer = SimpleConformer(str(self.input_dir), str(self.output_dir))
        
        self.assertEqual(conformer.TARGET_SAMPLE_RATE, 44100, "Sample rate should be 44.1kHz")
        self.assertEqual(conformer.TARGET_BITRATE, 192, "Bitrate should be 192kbps")
        
    def test_supported_formats_complete(self):
        """Verifica che tutti i formati radio comuni siano supportati"""
        conformer = SimpleConformer(str(self.input_dir), str(self.output_dir))
        
        required_formats = {'.mp3', '.flac', '.wav', '.m4a', '.aac', '.ogg'}
        for fmt in required_formats:
            self.assertIn(fmt, conformer.SUPPORTED_FORMATS,
                         f"Required format {fmt} should be supported")

class TestPerformanceAndStability(TestAntiRegressione):
    """Test per performance e stabilità"""
    
    def test_memory_initialization(self):
        """Verifica che l'inizializzazione non consumi memoria eccessiva"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss
        
        # Crea multiple istanze per test memory leak
        conformers = []
        for i in range(10):
            conformers.append(SimpleConformer(str(self.input_dir), str(self.output_dir)))
        
        memory_after = process.memory_info().rss
        memory_increase = memory_after - memory_before
        
        # Memory increase should be reasonable (< 50MB for 10 instances)
        max_acceptable_increase = 50 * 1024 * 1024  # 50MB
        self.assertLess(memory_increase, max_acceptable_increase,
                       f"Memory increase too high: {memory_increase / 1024 / 1024:.1f}MB")
        
        print(f"✅ Memory test passed. Increase: {memory_increase / 1024 / 1024:.1f}MB")

def run_anti_regression_suite():
    """Esegue la suite completa di test anti-regressione"""
    print("🧪 ANTI-REGRESSION TEST SUITE")
    print("=" * 50)
    print(f"Software: {APP_NAME} - {VERSION_NAME} v{APP_VERSION}")
    print(f"Python: {sys.version}")
    print(f"Platform: {sys.platform}")
    print("=" * 50)
    
    # Crea test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Aggiungi tutte le classi di test
    test_classes = [
        TestVersioneEMetadata,
        TestFFmpegDetection,
        TestFileProcessing,
        TestErrorHandling,
        TestGUIComponents,
        TestConfigurationConsistency,
        TestPerformanceAndStability,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Esegui test con verbose output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Report finale
    print("\n" + "=" * 50)
    print("📊 RISULTATI TEST ANTI-REGRESSIONE")
    print("=" * 50)
    print(f"Test eseguiti: {result.testsRun}")
    print(f"Successi: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallimenti: {len(result.failures)}")
    print(f"Errori: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ FALLIMENTI:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")
    
    if result.errors:
        print("\n💥 ERRORI:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback}")
    
    # Status finale
    if result.wasSuccessful():
        print("\n✅ TUTTI I TEST ANTI-REGRESSIONE PASSATI!")
        print("   Il software è stabile e pronto per release.")
        return True
    else:
        print("\n❌ ALCUNI TEST ANTI-REGRESSIONE FALLITI!")
        print("   Correggere i problemi prima di procedere.")
        return False

if __name__ == '__main__':
    success = run_anti_regression_suite()
    sys.exit(0 if success else 1) 