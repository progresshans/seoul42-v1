def count_page(number):
	if number <= 100:
		return 1
	page = number / 100
	page = page + 1 if number % (100 * page) != 0 else page
	return page