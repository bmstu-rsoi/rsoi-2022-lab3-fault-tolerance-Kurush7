from qr_server.dto_converter import *


@dataclass
class RatingDTO(QRDTO):
    stars: int
