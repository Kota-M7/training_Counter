import streamlit as st
import time
import pandas as pd
import sqlite3 
import hashlib
import datetime
import plotly.graph_objects as go

dt_now = datetime.datetime.now()
dt_today = datetime.date.today()

#df_w = pd.read_csv('pandas_weight_data.csv', index_col=0)

#if df_w['date'][-1:].values[0] == str(dt_today):
#	print("same")
#	df_w=df_w[:-1]
#	df_w=df_w.append({'date': str(dt_today),'goal': float(40),'weight': float(23)}, ignore_index=True)

#else:
#	df_w=df_w.append({'date': str(dt_today),'goal': float(40),'weight': float(23)}, ignore_index=True)

#df_w.to_csv('pandas_weight_data.csv')


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
	st.write(str(dt_now.year)+'年'+str(dt_now.month)+'月'+str(dt_now.day)+'日')

	#menu = ["ログイン","サインアップ"]
	menu = ["ログイン"]
	choice = st.sidebar.selectbox("メニュー",menu)

	if choice == "ログイン":
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
					st.write(df.tail())
					df.to_csv('pandas_normal.csv')
					if df.shape[0]%100==0:
						time.sleep(1)
						st.balloons()
						st.write(str(df.shape[0])+"回！?！?えらすぎっっ🥰🥰🥰")
					
					elif df.shape[0]%10==0:
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
				
					df_w = pd.read_csv('pandas_weight_data.csv', index_col=0)
					st.title('')
					st.title('体重の変化')
					weight=st.text_input('体重(kg)　例：55.2')
					goal=st.text_input('目標体重(kg)　例：50.2')

					if df_w['date'][-1:].values[0] == str(dt_today):
						df_w=df_w[:-1]
						df_w=df_w.append({'date': str(dt_today),'goal': float(goal),'weight': float(weight)}, ignore_index=True)

					else:
						df_w=df_w.append({'date': str(dt_today),'goal': float(goal),'weight': float(weight)}, ignore_index=True)

					st.write('前回から'+str(format(float(df_w['weight'][-1:].values[0])-float(df_w['weight'][-2:-1].values[0]),'.2f'))+'kgの変化!')
					if float(df_w['weight'][-1:].values[0])-float(df_w['weight'][-2:-1].values[0])<=-0.15:
						st.write('<span style="color:red;background:pink">減ったね！素晴らしい♪</span>',unsafe_allow_html=True)

					st.write('目標達成まであと'+str(format(float(weight)-float(goal),'.2f'))+'kg!')

					fig_w = go.Figure()
					fig_w.add_trace(go.Scatter(x=df_w['date'],
											 y=df_w['weight'],
											 mode='lines',
											 name='体重'))
					fig_w.add_trace(go.Scatter(x=df_w['date'],
											 y=df_w['goal'],
											 mode='lines',
											 name='目標'))

					#fig_w.update_layout(xaxis=dict(range=(datetime.date(2022, 2, 22),datetime.date(2022, 4, 8))))

					st.write(fig_w)


					df_w.to_csv('pandas_weight_data.csv')


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
