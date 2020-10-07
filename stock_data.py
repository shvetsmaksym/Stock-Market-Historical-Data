import yfinance as yf
from tkinter import *
from tkcalendar import *
from datetime import datetime
from pandastable import Table

class Stock_data:

	def __init__(self):
		'''set main window'''
		self.main_window = Tk()
		self.main_window.title('Stock History Data')
		self.main_window.geometry()

		'''set labels and buttons to input parametres'''
		#Company name
		self.smbl_label = Label(self.main_window, text="Company name")
		self.smbl_label.grid(row=0, column=0)
		self.smbl_box = Entry(self.main_window, width=30)
		self.smbl_box.grid(row=0, column=1, columnspan=2, pady=5, padx=5)

		#Date range
		self.trange_label = Label(self.main_window, text="Set the date range")
		self.trange_label.grid(row=1, column=0)

		#From date / to date variables
		self.fd = str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(datetime.now().day)
		self.td = str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(datetime.now().day)

		#From date / to date buttons and labels
		self.from_date = Button(self.main_window, text="from", width=10, command=self.set_from)
		self.from_date.grid(row=1, column=1)
		self.fd_label = Label(self.main_window, text="")
		self.fd_label.grid(row=2, column=1, pady=5)

		self.to_date = Button(self.main_window, text="to", width=10, command=self.set_to)
		self.to_date.grid(row=1, column=2)
		self.td_label = Label(self.main_window, text="")
		self.td_label.grid(row=2, column=2, pady=5)

		#Submit parameters
		self.submit_button = Button(self.main_window, text="Submit", command=self.download_data)
		self.submit_button.grid(row=3, column=1, pady=5)


	def run(self):
		self.main_window.mainloop()


	def download_data(self):
		# getting stock data
		stock = yf.Ticker(self.smbl_box.get())
		hist = stock.history(start=self.fd, end=self.td)

		# create new window
		hist_window = Tk()
		hist_window.title(self.smbl_box.get())

		frame = Frame(hist_window)
		frame.pack()

		# create table (pandastable.Table(tk.frame))
		table = Table(frame)
		# write stock data to the table
		table.model.df = hist
		# update changes in table
		table.redraw()
		table.show()

		chart_button = Button(hist_window, text="Show chart").pack()

		hist_window.mainloop()
	

	def set_date(conf):

		def wrapper(self):

			self.cal = Tk()
			self.cal.title("")

			today = datetime.now()
			self.calendar = Calendar(self.cal, date_pattern='y-mm-dd', selectmode="day", year=today.year, month=today.month, day=today.day)
			self.calendar.pack()

			confirm_button = Button(self.cal, text="Confirm", command = lambda: conf(self))
			confirm_button.pack()

			self.cal.mainloop()

		return wrapper

	@set_date
	def set_from(self):

		self.fd = self.calendar.get_date()
		self.fd_label = Label(self.main_window, text=self.calendar.get_date())
		self.fd_label.grid(row=2, column=1, pady=10)
		self.cal.destroy()

	@set_date
	def set_to(self):

		self.td = self.calendar.get_date()
		self.td_label = Label(self.main_window, text=self.calendar.get_date())
		self.td_label.grid(row=2, column=2, pady=10)
		self.cal.destroy()

if __name__ == "__main__":
	s = Stock_data()
	s.run()