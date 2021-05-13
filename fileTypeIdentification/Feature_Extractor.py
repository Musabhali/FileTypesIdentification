# The following class script is an adaptation 
# from a model that uses LBP to extract features by Adrian Rosebrock

from skimage import feature
import numpy as np

class LBP:
	def __init__(self, n_points, r):
		# store the number of points and r
		self.n_points = n_points
		self.r = r

	def describe(self, image, eps=1e-7):
		# compute the Local Binary Pattern representation
		# of the image, and then use the LBP representation
		# to build the histogram of patterns
		lbp = feature.local_binary_pattern(image, self.n_points,
			self.r, method="uniform")
		(fd, _) = np.histogram(lbp.ravel(),
			bins=np.arange(0, self.n_points + 3),
			range=(0, self.n_points + 2))

		# normalize the histogram
		fd = fd.astype("float")
		fd /= (fd.sum() + eps)

		# return the histogram of Local Binary Patterns
		return fd
	