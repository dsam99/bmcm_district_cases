import numpy as np
import scipy.stats as ss


def uniformity_metric(subattributes, judge_dists):
	# could modify if we have time to identify which subattribute is has the min
	if len(judge_dists) == 1:
		return 1,0
	chisquare_results = []
	for s in subattributes:
		observed = []
		for name in judge_dists:
			observed.append(judge_dists[name][s])
		if all(v == 0 for v in observed):
			chisquare_results.append(1)
		else:
			chisquare_results.append(ss.chisquare(observed)[1])
		# print(observed)
	# print(chisquare_results)
	return min(chisquare_results), np.argmin(chisquare_results)


def tv_metric(subattributes, judge_dists):
	'''
	Function to evaluate the score of non-randomness
	using KL divergence between judge dist and global dist
	'''

	judges = list(judge_dists.keys())
	to_return = 0
	big_diffs = []

	for s in subattributes:

		# get over all judges
		n = len(judge_dists)
		p = np.ones(n) / n
		q = np.zeros(n)
		for i, j in enumerate(judges):
			q[i] = judge_dists[j][s]

		total = np.sum(q)

		if total == 0:
			# print(s)
			# q = np.zeros(n)
			continue
		else:
			q /= total

		# compute metric here !!
		to_return += tv(p, q)

		# compute largest differences in prob -> what is contributing most to  non-randomness
		abs_diffs = np.abs(p - q)
		i = np.argmax(abs_diffs)
		big_diffs.append([abs_diffs[i], (s)])

	big_diffs = sorted(big_diffs, key=lambda x: -x[0])
	return to_return, big_diffs

def tv(p, q):
	'''
	Function to compute the total variation distance over two prob distributions
	'''

	return np.max(np.abs(p - q))


def workload_metric(judge_dists):
	'''
	Function to compute a metric based on the even distribution of cases over judges
	'''

	judge_counts = {}
	for j in judge_dists:

		# computing sum of judges
		dist = judge_dists[j]
		feat_dist = dist[list(dist.keys()[0])]

		sum = 0
		for key in feat_dist:
			sum += feat_dist[key]

		judge_counts[j] = sum

	print(judge_counts)
	return judge_counts
