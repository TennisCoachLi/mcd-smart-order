#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麦麦智能点餐 · 省钱补给助手 —— 麦当劳中国 MCP (mcd-mcp) 命令行客户端

零依赖（仅用 Python 标准库），用于：
  1. 列出麦当劳 MCP 当前可用的全部工具
  2. 直接调用某个工具（传 JSON 参数）
  3. 跑几个内置示例（营养查询 / 领券 / 查积分 / 活动日历）

接入说明：
  - 在 https://open.mcd.cn/mcp 用手机号申请 MCP Token
  - 设置环境变量：
      export MCD_MCP_TOKEN="你的Token"
      export MCD_MCP_URL="https://mcp.mcd.cn"   # 可选，默认即此
  - 注意：每个 Token 限流 600 次/分钟，超了返回 429，请降低频率

用法：
  python mcd_mcp_client.py list                       # 列出全部工具
  python mcd_mcp_client.py call <tool> '<json args>'  # 调用工具
  python mcd_mcp_client.py nutrition                  # 示例：查餐品营养
  python mcd_mcp_client.py coupons                    # 示例：一键领麦麦省券
  python mcd_mcp_client.py account                     # 示例：查我的积分
  python mcd_mcp_client.py calendar                   # 示例：查当月活动
"""

import os
import sys
import json
import urllib.request
import urllib.error

ENDPOINT = os.environ.get("MCD_MCP_URL", "https://mcp.mcd.cn").rstrip("/")
TOKEN = os.environ.get("MCD_MCP_TOKEN", "")
PROTOCOL_VERSION = "2025-06-18"
CLIENT_INFO = {"name": "mcd-smart-order", "version": "1.0.0"}


class McDMCPClient:
    """极简麦当劳 MCP Streamable HTTP 客户端。"""

    def __init__(self, endpoint: str = ENDPOINT, token: str = TOKEN):
        self.endpoint = endpoint
        self.token = token
        self.session_id = None
        self._req_id = 0

    def _next_id(self):
        self._req_id += 1
        return self._req_id

    def _post(self, payload: dict):
        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "MCD-Smart-Order/1.0 (mcd-smart-order)",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id

        req = urllib.request.Request(
            self.endpoint, data=data, headers=headers, method="POST"
        )
        # 默认用标准 urlopen；若设置 MCD_MCP_NO_PROXY=1 则安装无代理 opener 直连
        if os.environ.get("MCD_MCP_NO_PROXY") == "1":
            urllib.request.install_opener(
                urllib.request.build_opener(urllib.request.ProxyHandler({}))
            )
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            code = resp.getcode()
            body = resp.read().decode("utf-8", errors="replace")
            ct = resp.headers.get("Content-Type", "")
            sid = resp.headers.get("Mcp-Session-Id")
            if sid:
                self.session_id = sid
            return code, ct, body, None
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            return e.code, e.headers.get("Content-Type", ""), body, e.reason
        except Exception as e:  # 网络层错误
            return None, "", "", str(e)

    @staticmethod
    def _parse(ct: str, body: str):
        """从 application/json 或 text/event-stream 响应里解析出最后一个 JSON-RPC 对象。"""
        if "text/event-stream" in ct:
            last = None
            for line in body.splitlines():
                line = line.strip()
                if line.startswith("data:"):
                    chunk = line[5:].strip()
                    if chunk:
                        try:
                            last = json.loads(chunk)
                        except json.JSONDecodeError:
                            pass
            return last
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return None

    def initialize(self) -> dict:
        code, ct, body, err = self._post({
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": CLIENT_INFO,
            },
        })
        if code != 200:
            return {"ok": False, "code": code, "error": err or body}
        msg = self._parse(ct, body) or {}
        # 发送 initialized 通知（无需返回）
        try:
            self._post({
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {},
            })
        except Exception:
            pass
        return {"ok": True, "code": code, "serverInfo": msg.get("result", {})}

    def list_tools(self) -> list:
        code, ct, body, err = self._post({
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/list",
            "params": {},
        })
        if code != 200:
            return [{"ok": False, "code": code, "error": err or body}]
        msg = self._parse(ct, body) or {}
        return msg.get("result", {}).get("tools", [])

    def call_tool(self, name: str, arguments: dict) -> dict:
        code, ct, body, err = self._post({
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments or {}},
        })
        if code != 200:
            return {"ok": False, "code": code, "error": err or body}
        return self._parse(ct, body) or {}


def _require_token():
    if not TOKEN:
        print("⚠️  未检测到 MCD_MCP_TOKEN 环境变量。")
        print("    请先到 https://open.mcd.cn/mcp 用手机号申请 Token，然后：")
        print('    export MCD_MCP_TOKEN="你的Token"')
        return False
    return True


def cmd_list():
    c = McDMCPClient()
    init = c.initialize()
    if not init.get("ok"):
        code = init.get("code")
        if code == 403:
            print("⚠️  HTTP 403：未提供鉴权。请先设置环境变量 MCD_MCP_TOKEN")
            print("    （Token 在 https://open.mcd.cn/mcp 用手机号申请）")
        elif code == 401:
            print("⚠️  HTTP 401：鉴权码无效或已过期。请到 open.mcd.cn 重新申请 Token。")
        else:
            print(f"初始化失败（HTTP {code}）：{init.get('error')}")
        return
    tools = c.list_tools()
    if tools and isinstance(tools[0], dict) and not tools[0].get("ok", True):
        print(f"列出工具失败（HTTP {tools[0].get('code')}）：{tools[0].get('error')}")
        return
    print(f"✅ 连接成功，共 {len(tools)} 个工具：\n")
    for t in tools:
        print(f"  • {t.get('name')}: {t.get('description', '')[:60]}")


def cmd_call(tool, args_json):
    if not _require_token():
        return
    c = McDMCPClient()
    c.initialize()
    try:
        args = json.loads(args_json) if args_json else {}
    except json.JSONDecodeError as e:
        print(f"参数不是合法 JSON：{e}")
        return
    res = c.call_tool(tool, args)
    print(json.dumps(res, ensure_ascii=False, indent=2))


def _example(tool, args, label):
    if not _require_token():
        return
    c = McDMCPClient()
    c.initialize()
    print(f"▶ 示例：{label}（调用 {tool}）")
    res = c.call_tool(tool, args)
    print(json.dumps(res, ensure_ascii=False, indent=2))


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    cmd = args[0]
    if cmd == "list":
        cmd_list()
    elif cmd == "call":
        if len(args) < 2:
            print("用法: python mcd_mcp_client.py call <tool> '<json args>'")
            return
        cmd_call(args[1], args[2] if len(args) > 2 else "{}")
    elif cmd == "nutrition":
        _example("list-nutrition-foods", {}, "查餐品营养信息")
    elif cmd == "coupons":
        _example("auto-bind-coupons", {}, "一键领取麦麦省所有可领券")
    elif cmd == "account":
        _example("query-my-account", {}, "查我的积分账户")
    elif cmd == "calendar":
        _example("campaign-calendar", {}, "查当月营销活动日历")
    else:
        print(f"未知命令: {cmd}\n")
        print(__doc__)


if __name__ == "__main__":
    main()
