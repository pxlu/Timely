class UserProfile:

    def __init__(self, uid=-1, name="", keywords={}, severity=-1, confidence=[]):
        self.uid = uid
        self.name = name
        self.keywords = keywords
        self.severity = severity
        self.confidence = confidence

    def __str__(self):
        return "UserID: {}\nUsername: {}\nKeywords: {}\nSeverity: {}\nDisorders: {}".format(
            self.userid, self.username, self.keywords, self.severity, self.confidence)

class Disorder:

	def __init__(self, name="", disid=-1, symptoms=[], base_rate=-1):
		self.name = name
		self.id = disid
		self.symptoms = symptoms
        self.base_rate = base_rate

	def __str__(self):
		return "{} is a mental health disorder described in the DSM-5. It has symptoms of {}.".format(
			self.name, self.symptoms)
		