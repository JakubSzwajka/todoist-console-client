import unittest
import logging
import os

def test():
    logging.basicConfig(
        filename=f"{os.path.dirname(os.path.realpath(__file__))}/test/logs/test_logs.log",
        level=logging.WARNING,
        format="%(asctime)s: %(name)s: %(message)s",
    )

    tests = unittest.TestLoader().discover("test/", pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == "__main__":
    test()
