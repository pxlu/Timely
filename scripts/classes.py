class UserProfile:

    def __init__(self, userid=-1, username="", keywords={}, severity=-1, confidence=[]):
        self.userid = userid
        self.username = username
        self.keywords = keywords
        self.severity = severity
        self.confidence = confidence

    def __str__(self):
        return "UserID: {}\nUsername: {}\nKeywords: {}\nSeverity: {}\nDisorders: {}".format(
            self.userid, self.username, self.keywords, self.severity, self.confidence)

class Disorder:

	def __init__(self, name="", disid=-1, symptoms=[]):
		self.name = name
		self.id = disid
		self.symptoms = symptoms

	def __str__(self):
		return "{} is a mental health disorder described in the DSM-5. It has symptoms of {}.".format(
			self.name, self.symptoms)
		