import yfinance as yf
from tkinter import *
from tkcalendar import *
from datetime import datetime
from pandastable import Table
import mplfinance as mpf

class Stock_data:

	def __init__(self):
		'''set main window'''
		self.mainWindow = Tk()
		self.mainWindow.title('Stock History Data')
		self.mainWindow.geometry()

		'''set labels and buttons to input parametres'''
		#Company name
		self.smblLabel = Label(self.mainWindow, text="Company name")
		self.smblLabel.grid(row=0, column=0)
		self.smblBox = Entry(self.mainWindow, width=30)
		self.smblBox.grid(row=0, column=1, columnspan=2, pady=5, padx=5)

		#Date range
		self.timerangeLabel = Label(self.mainWindow, text="Set the date range")
		self.timerangeLabel.grid(row=1, column=0)

		#From date / to date variables (today is default)
		self.fromDate = str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(datetime.now().day)
		self.toDate = str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(datetime.now().day)

		#From date / to date buttons and labels
		self.fromDateButton = Button(self.mainWindow, text="from", width=10, command=self.set_from)
		self.fromDateButton.grid(row=1, column=1)
		self.fromDateLabel = Label(self.mainWindow, text="")
		self.fromDateLabel.grid(row=2, column=1, pady=5)

		self.toDateButton = Button(self.mainWindow, text="to", width=10, command=self.set_to)
		self.toDateButton.grid(row=1, column=2)
		self.toDateLabel = Label(self.mainWindow, text="")
		self.toDateLabel.grid(row=2, column=2, pady=5)

		#Submit parameters
		self.submitButton = Button(self.mainWindow, text="Submit", command=self.download_data)
		self.submitButton.grid(row=3, column=1, pady=5)


	def run(self):
		self.mainWindow.mainloop()


	def download_data(self):
		# getting stock data
		stock = yf.Ticker(self.smblBox.get())
		hist = stock.history(start=self.fromDate, end=self.toDate)
		hist["Date"] = hist.index

		# create new window
		histWindow = Tk()
		histWindow.title(self.smblBox.get())

		frame = Frame(histWindow)
		frame.pack()

		# create table (pandastable.Table(tk.frame))
		table = Table(frame, dataframe=hist[["Date", "Open", "High", "Low", "Close"]])
		table.show()
		
		chartButton = Button(histWindow, text="Show chart", command = lambda: self.show_chart(hist)).pack()

		histWindow.mainloop()
	
	
	def show_chart(self, df):
		"""Shows stock data as candleistick chart"""
		mpf.plot(df, type="candle")


	def set_date(conf):
		"""Opens new window with calendar"""

		def wrapper(self):

			self.cal = Tk()
			self.cal.title("")

			today = datetime.now()
			self.calendar = Calendar(self.cal, date_pattern='y-mm-dd', selectmode="day", year=today.year, month=today.month, day=today.day)
			self.calendar.pack()

			confirmButton = Button(self.cal, text="Confirm", command = lambda: conf(self))
			confirmButton.pack()

			self.cal.mainloop()

		return wrapper

	@set_date
	def set_from(self):
		"""gets set in calendar window date"""

		self.fromDate = self.calendar.get_date()
		self.fromDateLabel = Label(self.mainWindow, text=self.calendar.get_date())
		self.fromDateLabel.grid(row=2, column=1, pady=10)
		self.cal.destroy()

	@set_date
	def set_to(self):
		"""gets set in calendar window date"""

		self.toDate = self.calendar.get_date()
		self.toDateLabel = Label(self.mainWindow, text=self.calendar.get_date())
		self.toDateLabel.grid(row=2, column=2, pady=10)
		self.cal.destroy()

if __name__ == "__main__":
	s = Stock_data()
	s.run()