from enum import Enum
class QuestionLevel(str, Enum):
    BASIC = 'Basic'
    INTERMEDIATE = 'Intermediate'
    ADVANCE = 'Advance'

class KnowledgeLevel(str, Enum):
    Weak = 'Weak'
    INTERMEDIATE = 'Intermediate'
    Expert = 'Expert'
