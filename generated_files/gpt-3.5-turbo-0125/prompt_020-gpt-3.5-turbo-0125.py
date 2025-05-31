import markdown

class BloggingPlatform:
    def __init__(self):
        self.posts = {}
        self.post_history = []

    def write_post(self, admin_name, post_content):
        html_content = markdown.markdown(post_content)
        self.posts[admin_name] = html_content
        self.post_history.append((admin_name, html_content))

    def render_post(self, admin_name):
        if admin_name in self.posts:
            return self.posts[admin_name]
        else:
            return None

    def show_post_history(self):
        return self.post_history

    def live_preview(self, post_content):
        return markdown.markdown(post_content)


# Example usage
blogging_platform = BloggingPlatform()
blogging_platform.write_post("admin1", "# Hello World!")
print(blogging_platform.render_post("admin1"))
print(blogging_platform.show_post_history())
print(blogging_platform.live_preview("## Markdown Preview"))