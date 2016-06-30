import json

class UserProfile:

    def __init__(self, uid=-1, name="", keywords={}, severity=-1, confidence=[]):
        self.uid = uid
        self.name = name
        self.keywords = keywords
        self.severity = severity
        self.confidence = confidence

    def __str__(self):
        return "UserID: {}\nUsername: {}\nKeywords: {}\nSeverity: {}\nDisorders: {}".format(
            self.uid, self.name, self.keywords, self.severity, self.confidence)

class Disorder:

    def __init__(self, name="", disid=-1, symptoms=[], base_rate=-1, risk_factors = [], severity=-1):
        self.name = name
        self.id = disid
        self.symptoms = symptoms
        self.base_rate = base_rate
        self.risk_factors = risk_factors
        self.severity = severity

    def __str__(self):
        return "{} is a mental health disorder described in the DSM-5. It has symptoms of {}, with a base rate of {}. Currently, it's severity rating is {}.".format(
			self.name, self.symptoms, self.base_rate, self.severity)
	
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)