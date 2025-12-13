from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="../templates")


def render_template(name, **kwargs):
    return templates.TemplateResponse(name, kwargs)
