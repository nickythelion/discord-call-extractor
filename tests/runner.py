import unittest as ut

if __name__ == "__main__":

    tests = ut.TestLoader().discover(".")
    print(tests)
    ut.TextTestRunner(verbosity=2).run(tests)
