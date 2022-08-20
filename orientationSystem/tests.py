from django.test import TestCase
import pickle
import numpy as np
# Create your tests here.
"""model=pickle.load(open('orientationSystem/model/finalized_model.sav','rb+'))
print(model)"""

test= [[0.03134976, 0.03181375, 0.03134654, 0.03134654, 0.03134654 ,0.7612841,
  0.08151276]]


rs = np.around(test[0], decimals=2)
print(rs)