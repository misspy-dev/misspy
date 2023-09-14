from attrdictionary import AttrDict

from ...http import request, request_sync
from ...util import nonecheck


class admin_api:
    def __init__(self, client) -> None:
        self.address = client.__address
        self.i = client.__address

    def abuse_user_reports(
        self,
        limit=10,
        sinceId=None,
        untilId=None,
        state=None,
        reporterOrigin="combined",
        targetUserOrigin="combined",
        forwarded=False,
    ):
        base = {
            "limit": limit,
            "state": state,
            "reporterOrigin": reporterOrigin,
            "targetUserOrigin": targetUserOrigin,
            "forwarded": forwarded,
        }
        if nonecheck(sinceId):
            base["sinceId"] = sinceId
        if nonecheck(untilId):
            base["untilId"] = untilId
        return AttrDict(
            request_sync(self.address, self.i, "admin/abuse-user-reports", base)
        )

    def vacuum(self, full, analyze):
        return AttrDict(
            request_sync(
                self.address, self.i, "admin/vacuum", {"full": full, "analyze": analyze}
            )
        )

    def update_user_note(self, userId, text):
        return AttrDict(
            request_sync(
                self.address, self.i, "admin/vacuum", {"userId": userId, "text": text}
            )
        )
