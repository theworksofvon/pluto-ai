from agency.tools.base_tool import ToolResult
from agency.tools import BaseTool

class GenerativeArtTool(BaseTool):
    
    
    def validate_input(self, **kwargs) -> None:
        return True


    async def execute(self, **kwargs) -> None:
        pass



gen_art_tool = GenerativeArtTool(name="gen_art_tool", description="This tool is used when you want to create generative art images.")