import os

from markdown_blocks import markdown_to_html_node, extract_title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        from_path_contents = file.read()
    with open(template_path, 'r') as file:
        template_path_contents = file.read()

    html_content = markdown_to_html_node(from_path_contents).to_html()
    page_title = extract_title(from_path_contents)
    replaced_content = template_path_contents.replace("{{ Content }}", html_content)
    replaced_content_title = replaced_content.replace("{{ Title }}", page_title)

    path = os.path.dirname(dest_path)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(dest_path, 'w') as file:
        file.write(replaced_content_title)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.exists(dir_path_content):
        for item in os.listdir(dir_path_content):
            from_path = os.path.join(dir_path_content, item)
            dest_path = os.path.join(dest_dir_path, item)

            if os.path.isfile(from_path):
                dest_path = dest_path.replace(".md", ".html")
                generate_page(from_path, template_path, dest_path)
            else:
                generate_pages_recursive(from_path, template_path, dest_path)
