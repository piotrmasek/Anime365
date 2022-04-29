class Image:
    def __init__(self, post_id, file, ts, anime, diff):
        self.id: str = post_id
        self.file_name: str = file
        self.timestamp: int = ts
        self.anime: str = anime
        self.difficulty: int = diff

    def __str__(self) -> str:
        return f"id: {self.id}, file: {self.file_name}, date: {self.timestamp}, anime: {self.anime}," \
               f" diff: {self.difficulty}"
