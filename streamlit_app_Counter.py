import streamlit as st
import time
import pandas as pd
import sqlite3 
import hashlib

conn = sqlite3.connect('database.db')
c = conn.cursor()
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

def create_user():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_user(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def main():

	st.title("トレーニング記録アプリ💪")

	#menu = ["ログイン","サインアップ"]
	menu = ["ログイン"]
	choice = st.sidebar.selectbox("メニュー",menu)

	if choice == "ログイン":
		#st.subheader("ログイン画面です")

		username = st.sidebar.text_input("ユーザー名を入力してください")
		password = st.sidebar.text_input("パスワードを入力してください",type='password')

		if st.sidebar.checkbox("ログイン"):
			create_user()
			hashed_pswd = make_hashes(password)
			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("【認証成功】{}さんがログインしました".format(username))
				time.sleep(1)
				
				
				link = '[動画視聴](https://www.youtube.com/watch?v=2ve-gyPA6d0)'

				st.markdown(link, unsafe_allow_html=True)
				st.write('')


				# グラフx軸設定
				check = st.checkbox('エクササイズ完了😊')
				check_2 = st.checkbox('完了取り消し')
				
				#df = pd.DataFrame({'watch': [1],
				#				   'squat': [20],
				#				   'hip lift': [20],
				#				   'hip joint': [32],
				#				   'kcal': [34],
				#				   'min': [4]})

				df = pd.read_csv('pandas_normal.csv', index_col=0)
				#df.to_csv('pandas_normal.csv')

				if check==True and check_2==False:
					df=df.append({'watch': int(df.shape[0]+1), 'squat': int((df.shape[0]+1)*20), 'hip lift': int((df.shape[0]+1)*20),'hip joint': int((df.shape[0]+1)*32),'kcal': int((df.shape[0]+1)*34),'min': int((df.shape[0]+1)*4)}, ignore_index=True)
					st.write(df)
					df.to_csv('pandas_normal.csv')
					if df.shape[0]%10==0:
						time.sleep(1)
						st.balloons()
						st.write(str(df.shape[0])+"回達成！おめでとう🎉🎉🎉🎉🎉")
					
					elif df.shape[0]%5==0:
						st.write(str(df.shape[0])+"回！がんばってるね、えらい🚴")
					
						
					st.write(" ")
					
					

				elif check==False and check_2==True:
					df=df[:-1]
					st.write(df)
					df.to_csv('pandas_normal.csv')
					
				elif check==True and check_2==True:
					st.write('片方だけチェックしてね')

				else:
					st.write('')
					st.write('')
					st.write('')
					st.write('')
					slider=st.slider('あなたの今日の調子は？',0,100,50)
					if slider>=80:
						st.write('元気だね🌞🌞🌞')
					elif 80>slider>=60:
						st.write('平常運転だね🚙')
					elif slider==50:
						st.write('調子は50％')
					else:
						st.write('無理せずゆっくり休んでね😢')



			else:
				st.warning("ユーザー名かパスワードが間違っています")

	
	#elif choice == "サインアップ":
	#	st.subheader("新しいアカウントを作成します")
	#	new_user = st.text_input("ユーザー名を入力してください")
	#	new_password = st.text_input("パスワードを入力してください",type='password')

	#	if st.button("サインアップ"):
	#		create_user()
	#		add_user(new_user,make_hashes(new_password))
	#		st.success("アカウントの作成に成功しました")
	#		st.info("ログイン画面からログインしてください")
	
if __name__ == '__main__':
	main()
