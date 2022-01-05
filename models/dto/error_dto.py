class ErrorDto:
    def __init__(self, msg: str, code: int = 400):
        self.msg = msg
        self.code = code

    def to_request(self) -> tuple[dict, int]:
        return {"msg": self.msg}, self.code
