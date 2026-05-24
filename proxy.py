import json
import time
import random

from mitmproxy import ctx
from mitmproxy import http


class UniversalProxy:
    def load(self, loader):
        ctx.log.info("UniversalProxy loaded")

    #
    # HTTP Request
    #
    def request(self, flow: http.HTTPFlow):
        return
        req = flow.request

        ctx.log.info(f"[HTTP REQUEST] {req.method} {req.pretty_url}")

        for k, v in req.headers.items():
            ctx.log.debug(f"REQ HEADER {k}: {v}")

    #
    # HTTP Response
    #
    def response(self, flow: http.HTTPFlow):
        return
        resp = flow.response

        ctx.log.info(
            f"[HTTP RESPONSE] "
            f"{flow.request.method} "
            f"{flow.request.pretty_url} "
            f"=> {resp.status_code}"
            f"{resp.content}"
        )

    #
    # WebSocket Start
    #
    def websocket_start(self, flow):
        ctx.log.info(f"[WS CONNECT] {flow.request.pretty_url}")

    #
    # WebSocket Message
    #
    def websocket_message(self, flow):
        msg = flow.websocket.messages[-1]

        if not msg.from_client:
            return

        try:
            text = (
                msg.content.decode("utf8")
                if isinstance(msg.content, bytes)
                else msg.content
            )

            data = json.loads(text)

            cmdstr = data.get("cmd")

            if cmdstr in FILTER_CMD:
                return

            if "hehua" in data:
                HANDLERS["hehua"](data)
                print(f"hehua 存在{data}")

                pass
            elif "leftT" in data and "rank" in data and "progress" in data:
                HANDLERS["run"](data)
                print(f"run 存在{data}")

            elif "birds" in data:
                HANDLERS["bird"](data)
                print(f"bird 存在{data}")

            elif "feishi" in data:
                print(f"feishi 原始{data}")
                HANDLERS["feishi"](data)
                print(f"feishi 存在{data}")

            # elif "finish" in data and "score" in data and "security" in data:
            #     print(f"tangmen 原始{data}")
            #     HANDLERS["tangmen"](data)
            #     print(f"tangmen 存在{data}")

            else:
                print(f"cmd={cmdstr}")
                print(f"new_cmd={cmdstr}")
                print(f"{text}")
                return

            msg.content = json.dumps(
                data, ensure_ascii=False, separators=(",", ":")
            ).encode()

            print(f"modified cmd={cmdstr}")

        except Exception as e:
            print(e)

    #
    # WebSocket End
    #
    def websocket_end(self, flow):
        ctx.log.info(f"[WS CLOSED] {flow.request.pretty_url}")


addons = [UniversalProxy()]


def handle_login(data: map):
    data["ct"] = int(time.time() * 1000)


def handle_heartbeat(data):
    data["ct"] += 10000


def handle_buy(data):
    data["amount"] = 999999


def handle_hehua(data):
    data["hehua"] = [23, 22, 0]


def handle_run(data):
    data["leftT"] = 20
    data["progress"] = 480


def handle_bird(data):
    data["birds"] = "12|15|14|16"
    data["multiple"] = "16|7"


def handle_feishi(data):
    data["feishi"] = "9|9|7"
    data["times"] = 0


def handle_tangmen(data):
    data["score"] = 368


HANDLERS = {
    "hehua": handle_hehua,
    "run": handle_run,
    "bird": handle_bird,
    "feishi": handle_feishi,
    # "tangmen": handle_tangmen,
}

FILTER_CMD = [
    "AG_ECHO",
    "YIDQ8OjI6ISE=",
    "YKzs7LT4iNjdtfXx1ew==",
    "YKzs7Jjk2Ny19cnR/fXg0NiwiKiYuNQ==",
    "SICo+PjA+JSA=",
]
