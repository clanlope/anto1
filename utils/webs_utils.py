def request_web(
    url: str,
    payload: dict | list[dict] | None = None,
    user_info: tuple[str, str] | None = None,
) -> any:
    from playwright.sync_api import sync_playwright
    import json, os

    headers_file = "auth_header"

    def _authorize(rc: any):
        username, password = user_info if user_info else ("", "")

        def _capture_route(route):
            if route.request.resource_type in ["fetch", "xhr"]:
                for key in route.request.headers:
                    if "authorization" in key.lower():
                        with open(headers_file, "w") as f:
                            json.dump(route.request.headers, f)
                        rc.header_overrides = route.request.headers
                        break
            route.continue_()

        # change to the login page of the target website
        rc.route("**/*", _capture_route)

    def _request_once() -> any:
        def _verify_response(res: any) -> str:
            if res.status == 200:
                try:
                    return res.json()
                except Exception:
                    return res.text()
            elif res.status == 401:
                raise PermissionError("❌ Unauthorized request (401)")
            else:
                raise ValueError(f"❌ Request failed with status {res.status}")

        if payload is None:
            return _verify_response(rc.get(url))
        elif isinstance(payload, list):
            return [_verify_response(rc.post(url, data=pl)) for pl in payload]
        else:
            return _verify_response(rc.post(url, data=payload))

    with sync_playwright() as p:
        rc = p.request.new_context(ignore_https_errors=True, timeout=60_000)

        if os.path.exists(headers_file):
            with open(headers_file, "r") as f:
                rc.header_overrides = json.load(f)
        else:
            _authorize(rc)
        try:
            while True:
                try:
                    return _request_once()
                except PermissionError:
                    _authorize(rc)
        finally:
            rc.dispose()



