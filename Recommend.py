import numpy as np 
import math

def read_file(input_file):
	with open(input_file, 'r') as file:
		return ([l.strip() for l in file])

def str_to_list(input_list):

	output_list = []

	for i in input_list:
		output_list.append(i.split(" "))

	return output_list

def get_value(input_list, row, column):
	
	row_values = input_list[row - 1]

	return row_values[column - 1] 


def build_purchase_history(input_list, ID, for_customers=True):

	purchases = []

	history = []

	if for_customers:

		total_items = int(get_value(input_list, 1, 2))

		for i in input_list[1:]:
			if i[0] == str(ID) and i[1] not in purchases:
				purchases.append(i[1])
		for i in range(0, total_items):
			if str((i + 1)) in purchases:
				history.append(1)
			else:
				history.append(0)
	else:

		total_customers = int(get_value(input_list, 1, 1))

		for i in input_list[1:]:
			if i[1] == str(ID) and i[0] not in purchases:
				purchases.append(i[0])
		for i in range(0, total_customers):
			if str((i + 1)) in purchases:
				history.append(1)
			else:
				history.append(0)


	return history

def build_purchase_history_table(input_list, for_customers=True):

	purchase_history_table = {}

	if for_customers:
		for i in input_list[1:]:
			if i[0] not in purchase_history_table:
				purchase_history_table[i[0]] = build_purchase_history(input_list, i[0])

	else:
		for i in input_list[1:]:
			if i[1] not in purchase_history_table:
				purchase_history_table[i[1]] = build_purchase_history(input_list, i[1], False)

	return purchase_history_table


def get_positive_entries(table):

	total = 0

	for customer, items in table.items():
		for i in items:
			if i == 1:
				total += 1

	return total 




def calculate_angle(vector1, vector2):

	vector1 = np.array(vector1)
	vector2 = np.array(vector2)

	norm1 = np.linalg.norm(vector1)
	norm2 = np.linalg.norm(vector2)

	cos_theta = np.dot(vector1, vector2) / (norm1 * norm2)
	theta = math.degrees(math.acos(cos_theta))

	return '{:.2f}'.format(theta)


def calculate_all_angles(purchase_history_table):

	all_angles = {}

	for key, value in purchase_history_table.items():
		angles = {}
		for key2, value2 in purchase_history_table.items():
			if key != key2:
				angle = calculate_angle(value, value2)
				angles[key2] = angle
		all_angles[key] = angles

	return all_angles

def get_average_angle(all_angles):
	
	angles = []

	for key, value in all_angles.items():

		for key2, value2 in value.items():
			angles.append(float(value2))


	average_angle = sum(angles) / len(angles)

	return '{:.2f}'.format(average_angle)

def get_match(item_ID, table_of_angles, cart):

	item_angles = table_of_angles.get(str(item_ID))

	list_of_angles = []

	for item, angle in item_angles.items():
		if float(angle) < 90 and item not in cart:
			list_of_angles.append(angle)

	if list_of_angles != []:
		minimum_angle = min(list_of_angles)
		for item, angle in item_angles.items():
			if angle == minimum_angle:
				return item, angle
	else:
		return False

def order_list(match_dict):

	match_list = sorted(match_dict, key=lambda x: match_dict[x])

	return match_list


		


def get_recommendation(history, queries):


	history = read_file(history)
	history = str_to_list(history)

	queries = read_file(queries)
	queries_list = str_to_list(queries)


	customer_histories = build_purchase_history_table(history)
	item_histories = build_purchase_history_table(history, False)

	positive_entries = get_positive_entries(customer_histories)
	print("Positive entries: " + str(positive_entries))

	all_angles = calculate_all_angles(item_histories)

	average_angle = get_average_angle(all_angles)
	print("Average angle: " + str(average_angle))

	counter = 0


	for i in queries_list:

		cart = i 
		matches = {}

		print('Shopping cart: ' + str(queries[counter]))

		for j in i:
			match = get_match(j, all_angles, cart)
			if not match:
				print('Item: ' + str(j) + ' no match')
			else:
				print('Item: ' + str(j) + '; match: ' + match[0] + '; angle: ' + match[1])
				matches[match[0]] = match[1]

		recommendation_list = order_list(matches)

		list_to_string = ""

		for i in recommendation_list:
			list_to_string +=( " " + i )

		print("Recommend:" + list_to_string)
		counter += 1
	




get_recommendation('history.txt', 'queries.txt')


