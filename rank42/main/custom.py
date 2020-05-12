def count_page(number):
	if int(number) <= 100:
		return 1
	page = int(number) / 100
	page = page + 1 if number % (100 * page) != 0 else page
	return page


class RankTier:
	challenger_per = 0.1
	grandmaster_per = 0.2
	master_per = 0.4
	diamond_per = 2.5
	platinum_per = 8.3
	gold_per = 24
	silver_per = 35.2
	bronze_per = 22.3
	iron_per = 7.0

	def __init__(self, number):
		self.challenger = round(number * (self.challenger_per / 100))
		self.grandmaster = round(number * (self.grandmaster_per / 100))
		self.master = round(number * (self.master_per / 100))
		self.diamond = round(number * (self.diamond_per / 100))
		self.platinum = round(number * (self.platinum_per / 100))
		self.gold = round(number * (self.gold_per / 100))
		self.silver = round(number * (self.silver_per / 100))
		self.bronze = round(number * (self.bronze_per / 100))
		self.iron = number - (self.challenger + self.grandmaster + self.master + self.diamond + self.platinum + self.gold + self.silver + self.bronze)

	def return_all(self):
		return self.challenger, self.grandmaster, self.master, self.diamond, self.platinum, self.gold, self.silver, self.bronze, self.iron
