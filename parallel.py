from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from time import sleep
 
values = [3,4,5,6,7,8,9]
 
def cube(x):
    #print(f'Cube of {x}:{x*x*x}')
    return x**3
 
 
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=5) as exe:
        futures = [exe.submit(cube, value) for value in values]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        # auto join
        #exe.submit(cube,4)
         
        # Maps the method 'cube' with a list of values.
        #result = exe.map(cube,values)
     
    for r in results:
      print(r)