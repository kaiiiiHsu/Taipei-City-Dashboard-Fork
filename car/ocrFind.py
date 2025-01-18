import pyocr
tools = pyocr.get_available_tools()
if len(tools) > 0:
    print(f"Found OCR tool: {tools[0].get_name()}")
else:
    print("No OCR tool found")