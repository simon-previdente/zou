from ua_parser import user_agent_parser
from werkzeug.user_agent import UserAgent
from werkzeug.utils import cached_property


class ParsedUserAgent(UserAgent):
    @cached_property
    def _details(self):
        return user_agent_parser.Parse(self.string)

    @property
    def platform(self):
        return self._details["os"]["family"]

    @property
    def browser(self):
        return self._details["user_agent"]["family"]

    @property
    def version(self):
        return ".".join(
            self._details["user_agent"][key]
            for key in ("major", "minor", "patch")
            if self._details["user_agent"][key] is not None
        )
