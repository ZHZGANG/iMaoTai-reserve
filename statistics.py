
class UserResult:
    def __init__(self, name, success=0, failure=0):
        self.success = success
        self.failure = failure
        self.name = name
        self.text_results = []
    def add_success(self, count=1, *reasons):
        self.success += count
        self.text_results.extend(reasons)
    def add_failure(self, count=1, *reasons):
        self.failure += count
        self.text_results.extend(reasons)
    def __str__(self) -> str:
        return f"{self.name}: {self.success}/{self.failure+self.success}"
    def __repr__(self) -> str:
        return f"{self.name}: {self.success}/{self.failure+self.success}"

class Statistics:
    def __init__(self, **users):
        self.details = {}
        self.details.update(users)
        self.total_success = 0
        self.total_failure = 0
        for user in users:
            self.total_success += users[user].success
            self.total_failure += users[user].failure
    def update(self, result: UserResult):
        if result.name not in self.details:
            self.details[result.name] = result
        else:
            self.details[result.name].add_success(result.success)
            self.details[result.name].add_failure(result.failure)
        self.total_success += result.success
        self.total_failure += result.failure