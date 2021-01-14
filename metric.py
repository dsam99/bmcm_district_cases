from scipy.stats import entropy

def metric_eval(judge_dists, global_dist):
	'''
	Function to evaluate the score of non-randomness
	normalize KL divergence between judge dist and global dist
	'''

	val = 0

	attr_list = list(global_dist.keys())
	n = len(global_dist)
	p = np.zeros(n) # global dist (using forward KL)
	print(np.sum(p))

	for i, attr in enumerate(attr_list):
		p[i] = global_dist[attr]

	for j in judge_dists:
		q = np.zeros(n) # judge dist

		for i, attr in enumerate(attr_list):
			q[i] = judge_dists[j][attr]
		# check sum to 1
		print(np.sum(q))

		val += entropy(p, q)

	return val