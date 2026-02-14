class CParser:
    def __init__(self) -> None:
        self.chunks: list[str] = []
        self.current_chunk: list[str] = []
        self.brace_depth: int = 0
        self.in_function: bool = False

    def parse_string(self, chunk: str) -> list[str]:
        self.chunks = []
        self.current_chunk = []
        self.brace_depth = 0
        self.in_function = False
        for char in chunk:
            self.current_chunk.append(char)
            if char == "{":
                self.brace_depth += 1
                self.in_function = True
            elif char == "}":
                self.brace_depth -= 1
                if self.in_function and self.brace_depth == 0:
                    self.chunks.append("".join(self.current_chunk))
                    self.current_chunk = []
                    self.in_function = False
        return self.chunks
