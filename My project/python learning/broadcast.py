import numpy as np
A=np.array([[1, 2],
            [3, 4]])
B=A.sum(axis=0)
C=A.sum(axis=1)
div1=A/B.reshape(1,2)
div2=A/C.reshape(2,1)
print(div1)
print("\n")
print(div2)