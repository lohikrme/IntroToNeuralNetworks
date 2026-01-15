import numpy as np
import matplotlib.pyplot as plt

# Luodaan yksinkertaista dataa
x = np.arange(0, 10, 1)      # 0,1,2,...,9
y = x ** 2                   # x^2

plt.plot(x, y, marker="o")
plt.title("Testikäyrä: y = x^2")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)

plt.show()
