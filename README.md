# Car & Bike Selector
A small base for an interactive car selection screen, similar to those seen on car sale websites.
This has been rewritten to instead use a Flask webapp alongside SQLAlchemy ORM. While far more complicated than it needs to be, it was a bit of fun to write and feels great to use. I've also added bikes now.

Both cars and bikes are represented in the database with three tables; Make, Model, [Car only] Badge.
As a tree of models and badges are both entirely dependant on the existence of a single Make, the Make model has been placed as the base class in a joined table inheritance hierarchy that allows derived classes to represent a particular type of vehicle; namely Car and Bike. Below are a few examples of how these classes work.

The provided web form is just that - a web form... With JS and AJAX queries...
Yeah.

My data sets for Cars & Bikes are located in /import/

### Examples
```python

 # Locate a particular vehicle by calling Find upon the Class of the target derived type.
found_vehicles = [
	Car.Find( "Toyota", "Supra", "SZ" ) 	[0],
	Bike.Find( "BMW", "S 1000 R" )			[0]
]

for vehicle in found_vehicles:
	print("{0}, {1}, {2}".format( vehicle[0], vehicle[1], vehicle[2] ))

# Output:
# <Car 122: Toyota>, <Model 1519: Supra>, <Badge 5661: SZ>
# <Bike 149: BMW>, <Model 1938: S 1000 R>, None

```

```python

# Query for all badges by not providing the badge argument.
toyota_supra_badges = Car.Find( "Toyota", "Supra" )
print("# of Supra badges: " + str(len( toyota_supra_badges )))

# Output:
# # of Supra badges: 7

```

```python

# Query base for derived type using an Id.
x = [
	Make.GetById( 149 ),
	Make.GetById( 122 )
]
print("#0: {0}\n#1: {1}" .format( str(x[0]), str(x[1])))

# Output:
# #0: <Bike 149: BMW>
# #1: <Car 122: Toyota>

```

### Packages
* Flask==1.1.2
* Flask-SQLAlchemy==2.4.4
* marshmallow==3.7.1

### Authors
* **Alden Viljoen**