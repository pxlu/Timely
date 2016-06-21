class UserProfile:

    def __init__(self, userid=-1, username="", keywords={}, severity=-1, symptoms=[]):
        self.userid = userid
        self.username = username
        self.keywords = keywords
        self.severity = severity
        self.symptoms = symptoms

    def __str__(self):
        return "UserID: {}\nUsername: {}\nKeywords: {}\nSeverity: {}\nSymptoms: {}".format(
            self.userid, self.username, self.keywords, self.severity, self.symptoms)

class Disorder:

	def __init__(self, name="", symptoms=[]):
		self.name = name
		self.symptoms = symptoms

	def __str__(self):
		return "{} is a mental health disorder described in the DSM-5. It has symptoms of {}.".format(
			self.name, self.symptoms)
		