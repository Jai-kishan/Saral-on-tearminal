import requests
import json
import os

saral_url=("http://saral.navgurukul.org/api/courses")
def request(url,f_write):
	response=requests.get(url)
	with open(f"{f_write}.json","wb") as file:
		file.write(response.content)
	return response.json()

#Here we are creating empty list for stroring courses exercise ID
course_id_list=[]

def read_file(f_read):
	with open(f'{f_read}',"r") as file:
		data_read=file.read()
		data_load=json.loads(data_read)
	return(data_load)

def courses():
	data_load=read_file("courses.json")
	available_courses=data_load['availableCourses']
	for index in range(len(available_courses)):
		courses=available_courses[index]
		course_name=courses['name']
		courses_id=courses['id']
		print(index+1,courses_id,course_name)
		course_id_list.append(courses_id)

def select_course():
	user_input=int(input("\n\nselect your course list number:- "))
	select_id=course_id_list[user_input-1]
	# print (f"\t\nAapne jo course {user_input} select kiya hai us course ki ID {select_id} hai")
	return select_id

def read_exercise():
	data_load=read_file(f"{exercise_path}.json")
	exercise_data=data_load['data']
	slug=[]
	for i in range(len(exercise_data)):
		exercise_name=exercise_data[i]['name']
		exercise_slug=exercise_data[i]['slug']
		parent_exercise=exercise_data[i]['parentExerciseId']
		chile_exercise=exercise_data[i]['childExercises']
		print(i+1,exercise_name)
		slug.append(exercise_slug)

		for j in range(len(chile_exercise)):
			chile_exercise_name=chile_exercise[j]['name']
			chile_exercise_slug=chile_exercise[j]['slug']
			print("\t*"+str(chile_exercise_name))
			slug.append(chile_exercise_slug)

#The most common way to check for the existence of a file in Python is using the  
#exists() and isfile() methods from the os.path module in the standard library.
if os.path.exists("./courses.json"):
	courses()
	exercises_id=select_course()
	exercise_path=(f"request_data/Courses_Exercise/exercise_{exercises_id}")
	print(exercise_path)
	if os.path.exists(f"{exercise_path}.json"):
		read_exercise()
	else:
		request(f"{saral_url}/{exercises_id}/exercises",exercise_path) #make a new URL for retrive the data from the Server
		read_exercise() # through this function we fetch the data from API such as (parentExercise, childExercise, course slug etc)
else:
	request(saral_url,"courses")
	courses() #
	select_course()
