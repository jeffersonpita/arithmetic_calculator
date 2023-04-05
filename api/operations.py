from api.models import Operation
import requests

def dict_message(response_data=None, error_message:str="") -> dict:
    ''''
    Returns a dict with response_datas or error_messages
    '''
    if error_message!="":
        return {"status":0, "error_message":error_message}
    return {"status":1, "response_data":response_data}

def perform_operation(operation_type:int, operator1:str=None, operator2:str=None) -> dict:
    '''
    Function to perform the operations

    :param operation_type: operation type to be performed
    :param data1: first operator to the operation
    :param data1: second operator to the operation
    '''
    
    # if it's an arithmetic operation, require operator1 and operator2
    if operation_type in Operation.ARITHMETIC_OPERATIONS:
        if operator1=="" or operator2=="" or operator1==None or operator2==None:
            return dict_message(error_message="Operator 1 and Operator 2 are required")
        
        # cast the operators
        try:
            operator1 = float(operator1)
            operator2 = float(operator2)
        except Exception as e:
            return dict_message(error_message="Invalid operator")
    

    # check the operation.type
    if operation_type>6 or operation_type<1:
        return dict_message(error_message="Invalid operation")
    
    try:
        # perform the operations
        if operation_type==1:
            res = operator1 + operator2
        elif operation_type==2:
            res = operator1 - operator2
        elif operation_type==3:
            res = operator1 * operator2
        elif operation_type==4:
            res = operator1 / operator2
        elif operation_type==5:
            res = pow(operator1, operator2)
        elif operation_type==6:
            # perform the external API request
            url = "https://www.random.org/strings/?num=1&len=10&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new"
            response = requests.get(url, headers={'Accept': 'application/json'})
            res = response.content.strip().decode("utf-8")
    except Exception as e:  
        return dict_message(error_message=e)
    
    return dict_message(response_data=res)