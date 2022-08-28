import streamlit as st
from bson.json_util import dumps
import pymongo
from pymongo.server_api import ServerApi
st.set_page_config(page_title="AGGVENTURES",initial_sidebar_state="auto")

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
	"""Simple Login App"""
	new_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">AGGVENTURES</p>'

	#st.title("AGGVENTURES")
	st.markdown(new_title, unsafe_allow_html=True)


	menu = ["Home","Login","SignUp"]

	choice = st.sidebar.selectbox("Menu",menu)
	
	if choice == "Home":
		#st.subheader("Home")
		
		st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://cdn.pixabay.com/photo/2016/09/21/04/46/barley-field-1684052_960_720.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))
				
				if st.button(label="Load Data", key="btn_scrape"):
					myclient = pymongo.MongoClient(
						"mongodb+srv://lenin:lenin@cluster0.srbsrvl.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'),connect=False)
					mydb = myclient["aggventures"]
					mycol = mydb["moisture"]
					x = mycol.find()
					st.json(dumps(x))

			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		


		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")



if _name_ == '_main_':
	main()
