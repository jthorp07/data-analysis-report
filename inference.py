from scipy.stats import shapiro, ttest_ind_from_stats as ttest, mannwhitneyu
from essay_stats import IntegerStat, FloatStat, BatchManager, EssayBatchStats
from time import time
import json

MAX_SAMPLE_SIZE = 1000

def are_distributions_normal(one: IntegerStat|FloatStat, two: IntegerStat|FloatStat):
    return shapiro(one.counts)[1] > 0.05 and shapiro(two.counts)[1] > 0.05


def conduct_t_test(one: IntegerStat|FloatStat, two: IntegerStat|FloatStat, alpha: float = 0.01):
    _, pval = ttest(one.get_average(), one.get_std_dev(), one.num_counts,
                    two.get_average(), two.get_std_dev(), two.num_counts,
                    False)
    reject = "yes" if pval < alpha else "no"
    return { "p-value": pval, "reject-null": reject, "test-type": "2 Sample T-Test"}


def conduct_mann_whitney_u(one: IntegerStat|FloatStat, two: IntegerStat|FloatStat, alpha: float = 0.01):
    _, pval = mannwhitneyu(one.counts, two.counts, alternative="two-sided")
    reject = "yes" if pval < alpha else "no"
    return { "p-value": pval, "reject-null": reject, "test-type": "Mann Whitney U" }


def are_different_on_average(one: IntegerStat|FloatStat, two: IntegerStat|FloatStat, alpha: float = 0.01):
    if are_distributions_normal(one, two):
        return conduct_t_test(one, two, alpha)
    else:
        return conduct_mann_whitney_u(one, two, alpha)


def compare_batches(batch_one: BatchManager, batch_two: BatchManager, alpha: float = 0.01):
    one: list[tuple[str,EssayBatchStats]] = batch_one.get_batches()
    two: list[tuple[str,EssayBatchStats]] = batch_two.get_batches()
    results: dict[str, dict[str, tuple[float, bool]]] = {}
    start = time()
    for i in range(len(one)):
        test_name: str = one[i][0]
        one_data: EssayBatchStats = one[i][1].get_random_sample(MAX_SAMPLE_SIZE)
        two_data: EssayBatchStats = two[i][1].get_random_sample(MAX_SAMPLE_SIZE)
        results[test_name] = {}
        results[test_name]["word_counts"] = are_different_on_average(one_data.word_counts,
                                                                     two_data.word_counts,
                                                                     alpha)
        results[test_name]["unique_word_counts"] = are_different_on_average(one_data.unique_word_counts,
                                                                            two_data.unique_word_counts,
                                                                            alpha)
        results[test_name]["punctuation_counts"] = are_different_on_average(one_data.punc_counts,
                                                                            two_data.punc_counts,
                                                                            alpha)
        results[test_name]["rarity_scores"] = are_different_on_average(one_data.rarity_scores,
                                                                       two_data.rarity_scores,
                                                                       alpha)
        results[test_name]["average_sentence_lengths"] = are_different_on_average(one_data.sentence_lengths,
                                                                                  two_data.sentence_lengths,
                                                                                  alpha)
        results[test_name]["punctuations_per_word"] = are_different_on_average(one_data.ppw_ratios,
                                                                               two_data.ppw_ratios,
                                                                               alpha)
        results[test_name]["lexical_diversities"] = are_different_on_average(one_data.lexical_diversities,
                                                                             two_data.lexical_diversities,
                                                                             alpha)
    end = time()
    print(f"Inference took {end - start} seconds")
    with open("data/inference_results.json", "w", encoding="utf-8") as results_file:
        json.dump(results, results_file, ensure_ascii=False, indent=2)

