My solution to the find-store problem is a Python 3 script that finds the nearest store as follows:

1) Read in the CSV file.

Using Python's built-in csv module, I read the CSV file line by line. From each line, I created a tuple
of three pieces of information, the full store address, the store latitude, and the store longitude. I stored the
list of tuples that this generated in a class called LocationFinder and implemented functions to carry out the rest
of the task in that class.

2) Find the location of the user.

I needed the latitude and longitude of the current location of the user (or wherever the user searches from),
so I used the geopy module (installed via pip). Geopy offers an API for several geocoding
services, and I used the OpenStreetMap Nominatim service. The API returns an object that contains the latitude
and longitude, so I gathered those and returned them.

3) Determine how far the user is away from each store.

In searching for a way to calculate a human-understandable distance between two (latitude, longitude) coordinate
locations, I came across the Haversine Formula. The formula is designed to calculate the distance between two points
on the surface of the Earth given coordinates, and returns the result in kilometers. I added a function to the class
to calculate this distance. To find all of the store distances, I could then simply iterate through the list I gathered
before and pass in the user's coordinates and the coordinates of each store.

4) Finding the closest store to the user.

In this case, I chose to use a Python PriorityQueue object (essentially a min-heap that accepts (key, value) pairs
with a complete API) and simply added each distance and store address to it, allowing it to do the rest of the work.
Once the list has been iterated through, simply accessing the first element in the PriorityQueue with a get() call
retrieves the closest store in constant time (although each insertion takes up to O(log(n)) time). While this is
certainly computationally more expensive than simply maintaining an extra variable for the closest store name and
distance and checking on each iteration if this current store is closer than the previous closest, I like how clean
and easy it is in the code, in addition to making it really easy to extend to show the nearest 3 (or n) stores.
Furthermore, the number of stores (~1800) is small enough that the difference in code execution time is negligible
from the end user's perspective, and fairly trivial in terms of latency compared to the geocoding lookup.

5) Handle the command line API.

I used the python built-in argparse module to add an ArgumentParser and handle all the various use cases outlined.
By adding a few possible arguments to the ArgumentParser and then adding a handle_request function in my LocationFinder
class, I could pass in any of the specified arguments as parameters, call all the above logic, and then output the
information in the requested format.


To run the code, execute the following in a terminal:

python3 find_store.py --address="218 Hemenway Street Boston" [--units=km|mi] [--output=text|json]

or

python3 find_store.py --zip=94028 [--units=km|mi] [--output=text|json]