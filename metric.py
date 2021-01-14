from scipy.stats import entropy

def kl_metric(judge_dists, global_dist):
	'''
	Function to evaluate the score of non-randomness
	using KL divergence between judge dist and global dist
	'''

	val = 0

	attr_list = list(global_dist.keys())
	n = len(global_dist)
	p = np.zeros(n) # global dist (using forward KL)
	print(np.sum(p))

	big_diffs = []

	for i, attr in enumerate(attr_list):
		p[i] = global_dist[attr]

	for j in judge_dists:
		q = np.zeros(n) # judge dist

		for i, attr in enumerate(attr_list):
			q[i] = judge_dists[j][attr]
		# check sum to 1
		print(np.sum(q))
		val += entropy(p, q)

		# compute largest differences in prob -> what is contributing most to  non-randomness
		abs_diffs = np.abs(p - q)
		print(abs_diffs)

		for i in abs_diffs:
			big_diffs.append([abs_diffs[i], attr_list])

	big_diffs = sorted(big_diffs, key=lambda x: -x[0])
	return val, big_diffs

def tv_metric(judge_dists, global_dist):
	'''
	Function to evaluate the score of non-randomness
	using total variation between judge dist and global dist
	'''

	val = 0

	attr_list = list(global_dist.keys())
	n = len(global_dist)
	p = np.zeros(n) # global dist (using forward KL)
	print(np.sum(p))

	big_diffs = []

	for i, attr in enumerate(attr_list):
		p[i] = global_dist[attr]

	for j in judge_dists:
		q = np.zeros(n) # judge dist

		for i, attr in enumerate(attr_list):
			q[i] = judge_dists[j][attr]
		# check sum to 1
		print(np.sum(q))
		val += tv(p, q)

		# compute largest differences in prob -> what is contributing most to  non-randomness
		abs_diffs = np.abs(p - q)
		print(abs_diffs)

		for i in abs_diffs:
			big_diffs.append([abs_diffs[i], attr_list])

	big_diffs = sorted(big_diffs, key=lambda x: -x[0])
	return val, big_diffs

def tv(p, q):
	'''
	Function to compute the total variation distance over two prob distributions
	'''

	return np.max(np.abs(p - q))
