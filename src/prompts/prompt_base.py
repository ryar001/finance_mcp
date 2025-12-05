from typing import overload

class BasePrompt:
    prompt = ""
    @overload
    def get_formatted_prompt(self, **kwargs):
        return self.prompt.format(**kwargs)
        