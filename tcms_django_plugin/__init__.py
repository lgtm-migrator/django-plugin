# Copyright (c) 2020 Bryan Mutai , <work@bryanmutai.co>

# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html


from django.test.runner import DiscoverRunner
from .result import TestResult, DebugSQLTestResult, PDBDebugResult

# TODO RPC METHOD: <Fault -32601: 'Method not found: "PlanType.create"'>


class TestRunner(DiscoverRunner):
    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(self, pattern=None, top_level=None, verbosity=1,
                 interactive=True, failfast=False, keepdb=False,
                 reverse=False, debug_mode=False, debug_sql=False, parallel=0,
                 tags=None, exclude_tags=None, test_name_patterns=None,
                 pdb=False, buffer=False, **kwargs):
        super().__init__(pattern=pattern, top_level=top_level,
                         verbosity=verbosity, interactive=interactive,
                         failfast=failfast, keepdb=keepdb, reverse=reverse,
                         debug_mode=debug_mode, debug_sql=debug_sql,
                         parallel=parallel, tags=tags, pdb=pdb, buffer=buffer,
                         exclude_tags=exclude_tags,
                         test_name_patterns=test_name_patterns,
                         **kwargs)

    def get_resultclass(self):
        if self.debug_sql:
            return DebugSQLTestResult

        if self.pdb:
            return PDBDebugResult

        return TestResult

    def get_test_runner_kwargs(self):
        return {
            'failfast': self.failfast,
            'resultclass': self.get_resultclass(),
            'verbosity': self.verbosity,
        }

    def run_suite(self, suite, **kwargs):
        kwargs = self.get_test_runner_kwargs()
        runner = self.test_runner(**kwargs)
        results = runner.run(suite)
        return results
