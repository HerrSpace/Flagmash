import os
import random
import uuid
import json
import operator

import cherrypy
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('flag_app', 'templates'))

state_file = 'state.json'
flags_dir = 'static/flags'
k_factor = 3.0

def state_init():
	if os.path.isfile(state_file):
		with open(state_file, 'r') as f:
			state_json = f.read()
			state = json.loads(state_json)
		return state

	else:
		state = dict()

		for subdir, dirs, files in os.walk(flags_dir):
			for file in files:
				state[file] = 1000

		return state

def state_save(state):
	with open(state_file, 'w') as f:
		state_json = json.dumps(state)
		f.write(state_json)
	return


class Root(object):
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.state = state_init()
		self.games = dict()

		self.debug_template = env.get_template('debug.html')
		self.index_template = env.get_template('index.html')
		self.stats_template = env.get_template('stats.html')		

	def gen_game(self):
		g = dict()
		g["uuid"] = str(uuid.uuid4())
		
		g["o1"] = random.choice(self.state.keys())
		g["o2"] = g["o1"]
		while g["o2"] == g["o1"]:
			g["o2"] = random.choice(self.state.keys())

		self.games[g["uuid"]] = g

		return g

	def play_game(self, game, winner):
		if game not in self.games.keys(): return
		o1 = self.games[game]["o1"]
		o2 = self.games[game]["o2"]

		def elo_expectedA(scoreA, scoreB):
			Ea = 1.0 / (1.0 + 10**((scoreB - scoreA)/400.0) )
			return Ea

		def elo_mod_scores(self, winner):
			o1_offset = elo_expectedA( self.state[o1], self.state[o2] )
			o2_offset = o1_offset -1.0

			if winner == o2:
				o1_offset *= -1
				o2_offset *= -1				

			o1_offset = o1_offset * k_factor
			o2_offset = o2_offset * k_factor

			print(str(self.state[o1]) + " + " + str(o1_offset) + " = " + str(self.state[o1] + o1_offset))
			print(str(self.state[o2]) + " + " + str(o2_offset) + " = " + str(self.state[o2] + o2_offset))

			self.state[o1] += o1_offset
			self.state[o2] += o2_offset


		elo_mod_scores(self, winner)


	def index(self):
		g = self.gen_game()
		return self.index_template.render(o1=g["o1"], o2=g["o2"], game=g["uuid"])

	def index_r(self, game, winner):
		self.play_game(game, winner)
		state_save(self.state)
		return self.index()

	def stats(self):
		sorted_state = sorted(self.state.iteritems(), key=operator.itemgetter(1), reverse=True)
		return self.stats_template.render(flags=sorted_state)	

	def debug(self):
		return self.debug_template.render(ip=self.ip, port=self.port)
