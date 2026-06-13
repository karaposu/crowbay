# filepath: src/bot/api_client.py

"""HTTP client for the Crowdjump API — the bot's ONLY way to do anything.

The bot owns zero business logic: every rule lives behind these calls.
Tokens are cached in memory per telegram_id; a 401 triggers one re-bridge
and retry, so the bot never stores refresh tokens.
"""

import httpx


class ApiError(Exception):
    """An API response with status >= 400."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"{status_code}: {detail}")


class ApiUnreachable(Exception):
    """The API could not be reached at all."""


class ApiClient:
    def __init__(
        self,
        base_url: str,
        bridge_secret: str,
        transport: httpx.AsyncBaseTransport | None = None,
    ):
        self._bridge_secret = bridge_secret
        self._http = httpx.AsyncClient(base_url=base_url, timeout=15.0, transport=transport)
        self._tokens: dict[int, str] = {}  # telegram_id -> access token

    async def close(self) -> None:
        await self._http.aclose()

    # --- auth plumbing ---------------------------------------------------

    async def _bridge(self, tg_id: int, handle: str | None) -> str:
        try:
            r = await self._http.post(
                "/auth/telegram",
                json={"telegram_id": tg_id, "telegram_handle": handle},
                headers={"X-Bridge-Secret": self._bridge_secret},
            )
        except httpx.HTTPError as e:
            raise ApiUnreachable(str(e)) from None
        if r.status_code != 200:
            raise ApiError(r.status_code, _detail(r))
        token = r.json()["access_token"]
        self._tokens[tg_id] = token
        return token

    async def _request(
        self, method: str, path: str, tg_id: int, handle: str | None = None, **kwargs
    ) -> dict | list:
        token = self._tokens.get(tg_id)
        if token is None:
            token = await self._bridge(tg_id, handle)

        try:
            r = await self._http.request(
                method, path, headers={"Authorization": f"Bearer {token}"}, **kwargs
            )
            if r.status_code == 401:  # expired/stale token: re-bridge once
                token = await self._bridge(tg_id, handle)
                r = await self._http.request(
                    method, path, headers={"Authorization": f"Bearer {token}"}, **kwargs
                )
        except httpx.HTTPError as e:
            raise ApiUnreachable(str(e)) from None

        if r.status_code >= 400:
            raise ApiError(r.status_code, _detail(r))
        return r.json()

    # --- typed surface (mirrors the backbone API) -------------------------

    async def ensure_account(self, tg_id: int, handle: str | None) -> None:
        if tg_id not in self._tokens:
            await self._bridge(tg_id, handle)

    async def me(self, tg_id: int) -> dict:
        return await self._request("GET", "/users/me", tg_id)

    async def launch_task(self, tg_id: int, payload: dict) -> dict:
        return await self._request("POST", "/tasks", tg_id, json=payload)

    async def audience_preview(self, tg_id: int, filters: dict | None) -> dict:
        return await self._request(
            "POST", "/tasks/audience-preview", tg_id, json={"filters": filters}
        )

    async def browse(self, tg_id: int, page: int = 1, size: int = 5, **filters) -> dict:
        params = {"page": page, "size": size}
        params.update({k: v for k, v in filters.items() if v is not None})
        return await self._request("GET", "/tasks", tg_id, params=params)

    async def get_task(self, tg_id: int, task_id: int) -> dict:
        return await self._request("GET", f"/tasks/{task_id}", tg_id)

    async def my_tasks(self, tg_id: int) -> list:
        return await self._request("GET", "/tasks/my", tg_id)

    async def participated(self, tg_id: int) -> list:
        return await self._request("GET", "/tasks/participated", tg_id)

    async def jump(self, tg_id: int, task_id: int) -> dict:
        return await self._request("POST", f"/tasks/{task_id}/jump", tg_id)

    async def forfeit(self, tg_id: int, task_id: int) -> dict:
        return await self._request("POST", f"/tasks/{task_id}/forfeit", tg_id)

    async def task_jumps(self, tg_id: int, task_id: int, status: str | None = None) -> list:
        params = {"status": status} if status else {}
        return await self._request("GET", f"/tasks/{task_id}/jumps", tg_id, params=params)

    async def approve_jump(self, tg_id: int, task_id: int, jump_id: int) -> dict:
        return await self._request("POST", f"/tasks/{task_id}/jumps/{jump_id}/approve", tg_id)

    async def reject_jump(self, tg_id: int, task_id: int, jump_id: int) -> dict:
        return await self._request("POST", f"/tasks/{task_id}/jumps/{jump_id}/reject", tg_id)


def _detail(r: httpx.Response) -> str:
    try:
        detail = r.json().get("detail", r.text)
    except ValueError:
        detail = r.text
    if isinstance(detail, list):  # FastAPI validation errors
        parts = []
        for err in detail:
            loc = ".".join(str(x) for x in err.get("loc", []) if x != "body")
            parts.append(f"{loc}: {err.get('msg', '')}".strip(": "))
        detail = "; ".join(parts)
    return str(detail)
