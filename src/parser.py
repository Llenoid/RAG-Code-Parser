class CParser:
    def __init__(self) -> None:
        self.chunks: list[str] = []
        self.current_chunk: list[str] = []
        self.brace_depth: int = 0
        self.in_function: bool = False

        self.in_string = False
        self.in_comment = False
        self.is_multiline_comment = False

    def parse_string(self, chunk: str) -> list[str]:
        # print(f"\n{'Char':<5} | {'Depth':<5} | {'String':<7} | {'Comment':<7} | {'Multi':<7}")
        print("-" * 50)

        self.chunks = []
        self.current_chunk = []
        self.brace_depth = 0
        self.in_function = False
        self.in_string = False
        self.in_comment = False
        self.is_multiline_comment = False
        i = 0
        while i < len(chunk):
            char = chunk[i]
            # peek at next char (increment) if it exists
            next_char = chunk[i + 1] if i + 1 < len(chunk) else ""

            if not self.in_comment:
                self.current_chunk.append(char)

            if self.in_string:
                if char == '"' and chunk[i-1] != "\\":
                    self.in_string = False
            elif self.in_comment:
                if self.is_multiline_comment:
                    if char == "*" and next_char == "/":
                        self.in_comment = False
                        self.is_multiline_comment = False
                        i += 1 # Skip the /
                elif char == "\n":
                    self.in_comment = False
            else:
                if char == '"':
                    self.in_string = True
                elif char == '/' and next_char == '/':
                    self.in_comment = True
                elif char == '/' and next_char == '*':
                    self.in_comment = True
                    self.is_multiline_comment = True
                    i += 1 # Skip the * in /* */
                elif char == "{":
                    self.brace_depth += 1
                    self.in_function = True
                elif char == "}":
                    self.brace_depth -= 1
                    if self.in_function and self.brace_depth == 0:
                        self.chunks.append("".join(self.current_chunk))
                        self.current_chunk = []
                        self.in_function = False
            i += 1
            # debug_char = repr(char)
            # print(f"{debug_char:<5} | {self.brace_depth:<5} | {str(self.in_string):<7} | {str(self.in_comment):<7}")

        return self.chunks
