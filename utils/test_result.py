from dataclasses import dataclass

from sqlalchemy.sql.elements import Tuple

from algorithm.alg_result import AlgResult


@dataclass
class TestResult:
    before_res: dict
    after_res: Tuple
    alg_res: AlgResult

    def __post_init__(self):
        self.groups_usage_before = self.before_res['GROUPS    :']
        self.lecturers_usage_before = self.before_res['LECTURERS :']
        self.rooms_usage_before = self.before_res['ROOMS     :']
        self.lecturers_usage_after = self.after_res[0]['LECTURERS :']
        self.rooms_usage_after = self.after_res[0]['ROOMS     :']
        self.mean_gfv = self.after_res[1]
        self.btw = self.after_res[2].btw
        self.uni = self.after_res[2].uni
        self.wa = self.after_res[2].wa
        self.du = self.after_res[2].du
        self.successes = self.alg_res.successes
        self.failures = self.alg_res.failures
        self.failures_time = self.alg_res.failures_time
        self.successes_time = self.alg_res.successes_time
        self.time = self.alg_res.time

    def __repr__(self):
        return ("groups_usage_before: " + str(self.groups_usage_before) +"\n" +
                "lecturers_usage_before: " + str(self.lecturers_usage_before) +"\n" +
                "rooms_usage_before: " + str(self.rooms_usage_before) +"\n" +
                "lecturers_usage_after: " + str(self.lecturers_usage_after) +"\n" +
                "rooms_usage_after: " + str(self.rooms_usage_after) +"\n" +
                "mean_gfv: " + str(self.mean_gfv) + "\n" +
                "btw: " + str(self.btw) + "\n" +
                "uni: " + str(self.uni) + "\n" +
                "wa: " + str(self.wa) + "\n" +
                "du: " + str(self.du) + "\n" +
                "successes: " + str(self.successes) + "\n" +
                "failures: " + str(self.failures) + "\n" +
                "failures_time: " + str(self.failures_time) + "\n" +
                "successes_time: " + str(self.successes_time))