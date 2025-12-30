def request_web(
    url: str,
    payload: dict | list[dict] | None = None,
    user_info: tuple[str, str] | None = None,
) -> any:
    from playwright.sync_api import sync_playwright
    import json, os

    headers_file = "auth_header"

    def _local_autherize():
        if os.path.exists(headers_file):
            with open(headers_file, "r") as f:
                return json.load(f)
        else:
            return None
    
    def _authorize(rc: any):  #pw
        username, password = user_info if user_info else ("", "")

        def _capture_route(route):
            if route.request.resource_type in ["fetch", "xhr"]:
                for key in route.request.headers:
                    if "authorization" in key.lower():
                        with open(headers_file, "w") as f:
                            json.dump(route.request.headers, f)
                        rc.header_overrides = route.request.headers    # no use
                        break
            route.continue_()

        # change to the login page of the target website
        rc.route("**/*", _capture_route)

        with pw.chromium.launch(channel="chrome", headless=False) as browser:
            context = browser.new_context()
            page = context.new_page()
            page.goto()
            context.route("**/*, _capture_route)
            page.goto()
            page.unroute("**/*")

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
        try:
            while True:
                header = _local_autherize()
                try:
                    return _request_once()
                except PermissionError:
                    _authorize(rc)
        finally:
            rc.dispose()

#data = [i for d in request_web(url, mp, user_info) for i in d["result"]["results"]]


