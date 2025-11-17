# mtcars data dictionary (as in R)

Source: Base R `datasets::mtcars` (32 rows, 11 numeric variables). In R the car names are row names, not a variable.
Here, the 11 variables are stored in `mtcars.csv` exactly as in R. The companion `mtcars_with_model.csv` adds a `model` column for convenience.

## Variables
- `mpg` — Miles/(US) gallon  
- `cyl` — Number of cylinders  
- `disp` — Displacement (cu. in.)  
- `hp` — Gross horsepower  
- `drat` — Rear axle ratio  
- `wt` — Weight (1000 lbs)  
- `qsec` — 1/4 mile time (seconds)  
- `vs` — Engine (0 = V-shaped, 1 = straight)  
- `am` — Transmission (0 = automatic, 1 = manual)  
- `gear` — Number of forward gears  
- `carb` — Number of carburetors

Notes: R stores the car model names as row names. If you need them as a column, use `mtcars_with_model.csv` or join `mtcars.csv` with `mtcars_models.txt` in order.
