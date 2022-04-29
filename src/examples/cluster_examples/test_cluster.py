import sys
from timeit import default_timer as timer


start = timer()

string_test_value = str(sys.argv[1])
int_test_value = int(sys.argv[2])

print("The given input test value is", string_test_value)
print(f"The given integer squared is {int_test_value**2}")

end = timer()
