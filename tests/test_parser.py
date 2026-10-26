import unittest
import numpy as np
import os
import tempfile

def parse_nsphere_profile(filepath):
    raw = np.fromfile(filepath, dtype=np.float32)
    if len(raw) % 4 == 0:
        return raw.reshape(-1, 4)
    elif len(raw) % 3 == 0:
        return raw.reshape(-1, 3)
    else:
        raise ValueError("Unknown format")

class TestNSphereParser(unittest.TestCase):
    def test_4_column_float32(self):
        data = np.array([[1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0]], dtype=np.float32)
        with tempfile.NamedTemporaryFile(delete=False) as f:
            data.tofile(f.name)
            filepath = f.name
        try:
            result = parse_nsphere_profile(filepath)
            self.assertEqual(result.shape, (2, 4))
            self.assertEqual(result[0, 0], 1.0)
        finally:
            os.remove(filepath)

if __name__ == '__main__':
    unittest.main()
