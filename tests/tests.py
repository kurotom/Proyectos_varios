import unittest
import os
import shutil

from auto_update_mods.AutoUpdateClass import AutoUpdate


class AutoUpdateTestCase(unittest.TestCase):
    def setUp(self):
        self.auto = AutoUpdate()

    def test_check_key(self):
        self.assertEqual(self.auto.checkKey("asd"), False)

    def test_run_without_key(self):
        self.auto.key = None
        self.assertRaises(ValueError, lambda: self.auto.search())

    def test_save_mod(self):
        ruta = self.auto.save("fichero", "contenido".encode('utf8'))
        booleano = os.path.exists(os.path.abspath(ruta))
        self.assertTrue(booleano)
        shutil.rmtree('mods')
