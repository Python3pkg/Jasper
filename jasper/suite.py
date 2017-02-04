from jasper.utility import cyan, red


class Suite(object):

    def __init__(self, *features):
        self.features = features
        self.successes = []
        self.failures = []
        self.passed = True

    @property
    def num_features_passed(self):
        return len(self.successes)

    @property
    def num_features_failed(self):
        return len(self.failures)

    @property
    def num_scenarios_passed(self):
        return sum([feature.num_scenarios_passed for feature in self.features])

    @property
    def num_scenarios_failed(self):
        return sum([feature.num_scenarios_failed for feature in self.features])

    def __str__(self):
        feature_color = cyan if self.passed else red
        formatted_string = feature_color('='*150 + '\n')

        for feature in self.successes:
            formatted_string += cyan('='*150 + '\n')
            formatted_string += f'{feature}\n'
            formatted_string += cyan('=' * 150 + '\n')

        for feature in self.failures:
            formatted_string += red('=' * 150 + '\n')
            formatted_string += f'{feature}\n'
            formatted_string += red('=' * 150 + '\n')

        formatted_string += feature_color(
            f'{self.num_features_passed} Features passed, {self.num_features_failed} failed.\n'
            f'{self.num_scenarios_passed} Scenarios passed, {self.num_scenarios_failed} failed\n'
        )
        formatted_string += feature_color('='*150)

        return formatted_string

    def run(self):
        for feature in self.features:
            feature.run()

            if feature.passed:
                self.successes.append(feature)
            else:
                self.failures.append(feature)
                self.passed = False
