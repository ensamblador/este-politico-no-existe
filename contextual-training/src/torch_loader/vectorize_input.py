from src.utils import MEDIUM


class TrainInput:
	"""
	Use this class to vectorize a triplet of paragraphs in training or evaluation context
	"""

	def __init__(self, COALICION, PARTIDO, SENTIMIENTO, ENTIDADES, HASHTAGS, FRASES, TWEET):
		"""
		:param COALICION: [str] 
		:param PARTIDO: [str]
		:param SENTIMIENTO: [str]
		:param ENTIDADES: [str]
		:param HASHTAGS: [str] 
		:param FRASES: [str]
		:param TWEET: [str] 
		"""
		self.COALICION = COALICION
		self.PARTIDO = PARTIDO
		self.SENTIMIENTO = SENTIMIENTO
		self.ENTIDADES = ENTIDADES
		self.HASHTAGS = HASHTAGS
		self.FRASES = FRASES
		self.TWEET = TWEET

	def to_dict(self):
		return {
			'COALICION': self.COALICION,
			'PARTIDO': self.PARTIDO,
			'SENTIMIENTO': self.SENTIMIENTO,
			'ENTIDADES': self.ENTIDADES,
			'HASHTAGS': self.HASHTAGS,
			'FRASES': self.FRASES,
			'TWEET': self.TWEET
		}

	@classmethod
	def from_dict(cls, dict):
		return cls(
			COALICION=dict['COALICION'],
			PARTIDO=dict['PARTIDO'],
			SENTIMIENTO=dict['SENTIMIENTO'],
			ENTIDADES=dict['ENTIDADES'],
			HASHTAGS=dict['HASHTAGS'],
			FRASES=dict['FRASES'],
			TWEET=dict['TWEET']
		)


class GenerationInput:
	"""
	Use this class to vectorize a context input in Generation context
	"""

	def __init__(self, COALICION=None, PARTIDO=None, SENTIMIENTO=None, ENTIDADES=None,
				 HASHTAGS=None, FRASES=None):
		"""
		:param COALICION: [str] 
		:param PARTIDO: [str]
		:param SENTIMIENTO: [str]
		:param ENTIDADES: [str]
		:param HASHTAGS: [str] 
		:param FRASES: [str]
		"""
		self.COALICION = COALICION if COALICION else ""
		self.PARTIDO = PARTIDO if PARTIDO else ""
		self.SENTIMIENTO = SENTIMIENTO if SENTIMIENTO else "NEUTRAL"
		self.ENTIDADES = ENTIDADES if ENTIDADES else ""
		self.HASHTAGS = HASHTAGS if HASHTAGS else ""
		self.FRASES = FRASES if FRASES else ""
