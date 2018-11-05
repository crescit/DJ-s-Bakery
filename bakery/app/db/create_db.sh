
dir=$(pwd)

python $dir/create_db/create_schema.py $1

python $dir/create_db/create_categories.py $1

python $dir/create_db/create_products.py $1 $dir/create_db

python $dir/create_db/create_customers.py $1 $dir/create_db

python $dir/create_db/create_employees.py $1 $dir/create_db

python $dir/create_db/create_orders.py $1
