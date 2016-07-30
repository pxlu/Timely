from Timely.scripts import timely_common
from nltk.stem.snowball import SnowballStemmer

KEYWORDS = timely_common._init_keyword_list()
KEYWORDS_NAMES = timely_common._get_keywords(KEYWORDS)
DISORDERS = timely_common._init_disorder_list()
RESOURCES = timely_common._init_resource_list()

stemmer = SnowballStemmer("english")