from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from . import config


settings = config.get_settings()
BASE_DIR = settings.base_dir
TEMPLATE_DIR = settings.template_dir

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def render(
    request,
    template_name,
    context={},
    status_code: int = 200,
    cookies: dict = {},
    token={},
):
    ctx = context.copy()
    ctx.update({"request": request})

    t = templates.get_template(template_name)
    html_str = t.render(ctx)

    response = HTMLResponse(html_str, status_code=status_code)

    if len(cookies.keys()) > 0:
        for k, v in cookies.items():
            response.set_cookie(key=k, value=v, httponly=True)

    return response


def redirect(path, cookies: dict = {}, remove_session=False):
    response = RedirectResponse(path, status_code=302)

    for key, val in cookies.items():
        response.set_cookie(key=key, value=val, httponly=True)

    if remove_session:
        response.delete_cookie("session_id")

    return response
