import sys
## this code professionalizing error handling
# instead of showing raw and messy error message it genreates a custom error message 
#  with line no and error number

def error_message_detail(error,error_detail:sys):# this function generates a message for user/developer
    _,_,exc_tb=error_detail.exc_info()#this is an trackable object-> like file name and line number
    file_name=exc_tb.tb_frame.f_code.co_filename# excat location of file and frame where error occurs

    error_messaage="Error occured in python scrpit name [{0}] line number [{1} error message[{2}]".format(
    file_name,exc_tb.tb_lineno,str(error)
    )
    return error_messaage

class CustomExecption(Exception):
    def __init__(self,error_meassage,error_detail:sys):
        super().__init__(error_meassage)# to intialize the parent class's constructor
        '''Why this matters:
            Enables traceback
            Enables logging
            Enables print(e)'''
        self.error_message=error_message_detail(error_meassage,error_detail=error_detail)

    def __str__(self):
        return self.error_message
   
# sys provides a function (exc_info) to fetch the currently active exception