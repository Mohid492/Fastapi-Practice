import pytest
def add(x,y):
    return x + y

def sub(x,y):
    return x - y

def test_add():
    print("Testing")
    assert add(3,5)==8

def test_subtract():
    assert sub(5,3) == 2

@pytest.mark.parametrize("num1,num2,expected",[
    (3,5,8),  # Corrected expected value
    (10,20,30),
])
def test_add_another(num1,num2,expected):
    print("Testing")
    assert add(num1,num2)==expected