from jinja2 import Environment, FileSystemLoader
from stats.essence_stats import EssenceStats


def generate_html_table(data: EssenceStats, template_dir: str, template_name: str = 'table.html') -> str:
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    return template.render(data={"essence_stats": data})
