import numpy as np 
import math



def read_file(input_file): #read the input file into a list
	with open(input_file, 'r') as file:
		return ([l.strip() for l in file])

def str_to_list(input_list): #coverts each line from the list into a list of the individual numbers that were seperated by whitespace

	output_list = []

	for i in input_list:
		output_list.append(i.split(" "))

	return output_list

def get_value(input_list, row, column): #function to get a particular value based on the row and column its in. Used to get total customers, total items etc
	
	row_values = input_list[row - 1]

	return row_values[column - 1] 


def build_purchase_history(input_list, ID, for_customers=True): #builds purchase history vector for an individual customer or item

	purchases = [] #creates empty list for purchases

	history = [] #creates empty list for purchase history vector

	if for_customers: 

		total_items = int(get_value(input_list, 1, 2)) #gets the total number of items from first line in document

		for i in input_list[1:]: #skips first line of the document
			if i[0] == str(ID) and i[1] not in purchases: #searches document for customer and checks item not already in purchase list
				purchases.append(i[1]) #adds item to a list of customers purchases
		
		for i in range(0, total_items): #goes through items, if customer bought the item appends 1, if not appends 0
			if str((i + 1)) in purchases:
				history.append(1)
			else:
				history.append(0)
	else:

		total_customers = int(get_value(input_list, 1, 1)) #gets total number of customers from first line in the document

		for i in input_list[1:]:
			if i[1] == str(ID) and i[0] not in purchases: #scans document for item and checks checks customer not already in list of customers that have bought the item
				purchases.append(i[0]) #adds customer to list of customers who purchased the item
		
		for i in range(0, total_customers): #goes through customer ID's, if customer bought the item appends 1, else appends 0
			if str((i + 1)) in purchases:
				history.append(1)
			else:
				history.append(0)


	return history

def build_purchase_history_table(input_list, for_customers=True): #Builds purchase history table as a dictionary with the key being the customer/item ID and the value being a vector of their purchase history

	purchase_history_table = {} #creates empty dict

	if for_customers: 
		for i in input_list[1:]:
			if i[0] not in purchase_history_table: #check if customer is already in table 
				purchase_history_table[i[0]] = build_purchase_history(input_list, i[0]) #append dict with new entry, key is customer ID, value is purchase history vector

	else:
		for i in input_list[1:]:
			if i[1] not in purchase_history_table: #check if item already in table
				purchase_history_table[i[1]] = build_purchase_history(input_list, i[1], False) #append dict with new entry, key is item ID, value is purchase history vector

	return purchase_history_table


def get_positive_entries(table): #counts total number of positive entries in purchase history table 

	total = 0

	for customer, items in table.items():
		for i in items:
			if i == 1:
				total += 1

	return total 




def calculate_angle(vector1, vector2): #calculates angle between two purchase history vectors 

	vector1 = np.array(vector1) #convert from normal arrays to numpy arrays
	vector2 = np.array(vector2)

	norm1 = np.linalg.norm(vector1) #get norm of each vector
	norm2 = np.linalg.norm(vector2)

	cos_theta = np.dot(vector1, vector2) / (norm1 * norm2) #dot product of the two vectors divided by the procuct of their norms gives us cos theta
	theta = math.degrees(math.acos(cos_theta)) #arc-cos of this value gives us the angle between the two vectors

	return '{:.2f}'.format(theta) #formats angle to two decimal places


def calculate_all_angles(purchase_history_table): #builds dictionary of angles between every pair of items

	all_angles = {} #initialise empty dictionary

	for key, value in purchase_history_table.items():
		angles = {} #intialise empty dictionary for subitems and their angle with main item
		for key2, value2 in purchase_history_table.items():
			if key != key2: #makes sure item doesnt try and find angle with itself 
				angle = calculate_angle(value, value2)
				angles[key2] = angle #adds subitem and its relative angle to a dictionary of angles
		all_angles[key] = angles #then adds this dictionary as a value to the main dictionary

	return all_angles #returns full table of all possible comparisons

def get_average_angle(all_angles):
	
	angles = [] #initialise empty list

	for key, value in all_angles.items():
		for key2, value2 in value.items(): #adds all angles from table to list
			angles.append(float(value2))


	average_angle = sum(angles) / len(angles) #divide total of all angles by the number of angles to get the average

	return '{:.2f}'.format(average_angle) #returns angle to 2 decimal places

def get_match(item_ID, table_of_angles, cart): #takes an item and finds a match from the table that isn't already in the cart

	item_angles = table_of_angles.get(str(item_ID)) #returns the dictionary of angles for a particular item

	list_of_angles = [] #initialise empty list

	for item, angle in item_angles.items():
		if float(angle) < 90 and item not in cart: #if angle is less than 90 and item isnt in cart then item is added to the list
			list_of_angles.append(angle)

	if list_of_angles != []: #checks there is at least one match
		minimum_angle = min(list_of_angles) #finds item with smallest angle compared to item we are working with
		for item, angle in item_angles.items():
			if angle == minimum_angle: #searches through dictionary and finds first item with this minimum angle
				return item, angle #returns the item and the angle
	else:
		return False #function returns 'false' if there are no matches

def order_list(match_dict): #function that takes a dictionary of matches from a cart and orders them by their minimum angle

	match_list = sorted(match_dict, key=lambda x: match_dict[x])

	return match_list


		


def get_recommendation(history, queries): #essentially acts as a 'main' function that calls the other functions and prints necessary outputs


	history = read_file(history)
	history = str_to_list(history) #reads history document and converts it to lists

	queries = read_file(queries) 
	queries_list = str_to_list(queries) #reads queries document and converts it to lists


	customer_histories = build_purchase_history_table(history) #builds customer purchase history table
	item_histories = build_purchase_history_table(history, False) #builds item purchase history table

	positive_entries = get_positive_entries(customer_histories) #gets number of positive entries
	print("Positive entries: " + str(positive_entries)) #prints this number

	all_angles = calculate_all_angles(item_histories) #builds dictionary of angles between every pair of items

	average_angle = get_average_angle(all_angles) #calculates average angle
	print("Average angle: " + str(average_angle)) #prints this value

	

	counter = 0 #initialises a counter to keep track of the row in the queries list


	for i in queries_list: #for loop that goes through all queries in the document and finds matches/recommendations

		cart = i 
		matches = {} #intialise dict for matches that can be parsed into the order_list function

		print('Shopping cart: ' + str(queries[counter])) #prints shopping cart based on row of the document

		for j in i:
			match = get_match(j, all_angles, cart) #gets a match for the particular item
			if not match:
				print('Item: ' + str(j) + ' no match') #prints no match if the match function returns false
			else:
				print('Item: ' + str(j) + '; match: ' + match[0] + '; angle: ' + match[1]) #prints the item, matched item and angle in correct format
				matches[match[0]] = match[1] #adds the matched item to dictionary of matches for this cart

		recommendation_list = order_list(matches) #returns ordered list of recommendations for this cart

		list_to_string = ""

		for i in recommendation_list:
			list_to_string +=( " " + i ) #converts list of recommendations to a string to be outputted

		print("Recommend:" + list_to_string)
		
		counter += 1 #adds one to the counter when we are done with this row
	




get_recommendation('history.txt', 'queries.txt') #calls main function with appropriate files


