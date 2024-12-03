from agency.tools.base_tool import ToolResult
from tools import BaseTool

class GenerativeArtTool(BaseTool):
    
    
    def validate_input(self) -> None:
        pass


    async def execute(self) -> None:
        pass



gen_art_tool = GenerativeArtTool(name="gen_art_tool", description="This tool is used when you want to create generative art images.")