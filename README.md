# FinancialTradingSystem

There are 3 main folders, each of them reprezenting a service: Authentication, Master Data, Message Queue and Financial Calculations.
The financial calculations service 
-->uses a parallel distributed approach
-->will read a request from the jobs queue, implemented in the Message Queue Service, perform some calculations, using the functions from the timesseries file in the same folder and then send back the result to the results queue, also implemented in the Message Queue Service. 
-->has access to a number P of processors; we used the Message Passing Interface and its implementation OpenMPI
