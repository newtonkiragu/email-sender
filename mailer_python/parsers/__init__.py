from .simple_parser import SimpleCsvEmailParser
from .students_review_parser import StudentReviewParser

csv_parsers={
    "SimpleParser":SimpleCsvEmailParser,
    "StudentReview":StudentReviewParser,
}