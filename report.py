from statistics import Statistics
import yaml
import io

class ReportBase:
    def __init__(self, statistics, title="", initial_content=""):
        self.title = title
        self.content = io.StringIO(initial_content)
        self.records = []
        self.statistics = statistics

    def build(self) -> (str, str):
        raise NotImplementedError

    def setTitle(self, title:str):
        self.title = title

    def appendContent(self, content: str):
        self.content.append(content)

class TextReport(ReportBase):
    def build(self) -> (str, str):
        ratio = f"{self.statistics.total_success}/{self.statistics.total_failure+self.statistics.total_success}"
        self.title = "预约全部成功" if self.statistics.total_failure == 0 else "预约失败"
        self.title += f"({ratio})"
        yaml.dump(self.statistics, self.content, encoding='utf-8', allow_unicode=True)
        return self.title, self.content.getvalue()