# test_tf_numpy.py
import sys
print("python:", sys.version)
import numpy as np
print("numpy:", np.__version__)
import tensorflow as tf
print("tensorflow:", tf.__version__)
print("tf test:", tf.constant([1.0,2.0]) + 1.0)
