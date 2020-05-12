def count_page(number):
	if int(number) <= 100:
		return 1
	page = int(number) / 100
	page = page + 1 if number % (100 * page) != 0 else page
	return page


class RankTier:
	challenger_name = "Chanllenger"
	challenger_per = 0.1
	challenger_img = "https://opgg-static.akamaized.net/images/medals/challenger_1.png"
	grandmaster_name = "Grandmaster"
	grandmaster_per = 0.2
	grandmaster_img = "https://opgg-static.akamaized.net/images/medals/grandmaster_1.png"
	master_name = "Master"
	master_per = 0.4
	master_img = "https://opgg-static.akamaized.net/images/medals/master_1.png"
	diamond_name = "Diamond"
	diamond_per = 2.5
	diamond_img = "https://opgg-static.akamaized.net/images/medals/diamond_1.png"
	platinum_name = "Platinum"
	platinum_per = 8.3
	platinum_img = "https://opgg-static.akamaized.net/images/medals/platinum_1.png"
	gold_name = "Gold"
	gold_per = 24
	gold_img = "https://opgg-static.akamaized.net/images/medals/gold_1.png"
	silver_name = "Silver"
	silver_per = 35.2
	silver_img = "https://opgg-static.akamaized.net/images/medals/silver_1.png"
	bronze_name = "Bronze"
	bronze_per = 22.3
	bronze_img = "https://opgg-static.akamaized.net/images/medals/bronze_1.png"
	iron_name = "Iron"
	iron_per = 7.0
	iron_img = "https://opgg-static.akamaized.net/images/medals/iron_1.png"

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

	def set_tier(self, ft_users):
		for i, ft_user in enumerate(ft_users):
			if self.challenger >= i:
				ft_user.tier_name = self.challenger_name
				ft_user.tier_img = self.challenger_img
			elif self.challenger + self.grandmaster >= i:
				ft_user.tier_name = self.grandmaster_name
				ft_user.tier_img = self.grandmaster_img
			elif self.challenger + self.grandmaster + self.master >= i:
				ft_user.tier_name = self.master_name
				ft_user.tier_img = self.master_img
			elif self.challenger + self.grandmaster + self.master + self.diamond >= i:
				ft_user.tier_name = self.diamond_name
				ft_user.tier_img = self.diamond_img
			elif self.challenger + self.grandmaster + self.master + self.diamond + self.platinum >= i:
				ft_user.tier_name = self.platinum_name
				ft_user.tier_img = self.platinum_img
			elif self.challenger + self.grandmaster + self.master + self.diamond + self.platinum + self.gold >= i:
				ft_user.tier_name = self.gold_name
				ft_user.tier_img = self.gold_img
			elif self.challenger + self.grandmaster + self.master + self.diamond + self.platinum + self.gold + self.silver >= i:
				ft_user.tier_name = self.silver_name
				ft_user.tier_img = self.silver_img
			elif self.challenger + self.grandmaster + self.master + self.diamond + self.platinum + self.gold + self.silver + self.bronze >= i:
				ft_user.tier_name = self.bronze_name
				ft_user.tier_img = self.bronze_img
			else:
				ft_user.tier_name = self.iron_name
				ft_user.tier_img = self.iron_img
			ft_user.tier_rank = i + 1
		return ft_users
